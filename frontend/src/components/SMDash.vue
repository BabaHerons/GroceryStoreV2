<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_categories()
        this.get_all_categories_request()
        this.get_all_products()
        this.product.created_by = `${localStorage.getItem("user_id")}`
    },
    mounted() {
        let source = new EventSource("http://localhost:5000/stream")
        source.addEventListener("greeting", (event:any)=>{
            let data = JSON.parse(event.data)
            // console.log(data);
            this.sse.greeting.push(data.message)
            // alert("Message from the server: " + data.message)
        })

        // SSE FOR CATEGORY CHANGE
        const listen_for = `${localStorage.getItem("user_id")}-${localStorage.getItem("user")}`
        source.addEventListener(listen_for, (event:any) => {
            const data = JSON.parse(event.data)
            if (data.message.includes("DECLINED") || data.message.includes("DELETED")){
                this.sse.greeting.push(data.message)
            } else {
                this.sse.category_request.push(data.message)
            }
            this.get_all_categories()
            this.get_all_categories_request()
        })
    },
    data: () => {
        return {
            categories_list:[] as any [],
            requested_categories_list:[] as any [],
            category:{
                loading:false,
                title:"",
                description:"",
                created_by:"",
                created_by_name:""
            },
            request_category:{
                loading:false,
                title:"",
                description:"",
                created_by:"",
                created_by_name:""
            },
            selected_category:{} as any,
            requested_category:{} as any,
            category_change_history_list:[] as any[],
            sse:{
                greeting:[] as any[],
                category_request:[] as any[],
            },
            product_list:[] as any[],
            product:{
                name:"",
                description:"",
                category_id:"Select",
                m_date:"",
                e_date:"",
                stock:0,
                price:0,
                unit:"Choose a unit",
                created_by:""
            },
            selected_product:{} as any,

        }
    },
    methods: {
        string_to_date(date:string){
            let dt = date.slice(6,10) + "-" + date.slice(3,5) + "-" + date.slice(0,2)
            return dt
        },
        get_all_categories(){
            this.categories_list = []
            API.get_categories()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.categories_list = k
            })
        },
        get_all_categories_request(){
            this.requested_categories_list = []
            API.get_categories_request()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.category_change_history_list = k
                for (let i=0; i<k.length; i++){
                    if (k[i].status == "pending"){
                        this.requested_categories_list.push(k[i])
                    }
                }
            })
        },
        submit_category_form(){
            this.category.loading = true
            let json_data = {
                "title": this.category.title,
                "description": this.category.description,
                "created_by": localStorage.getItem("user_id")!,
                "created_by_name": localStorage.getItem("user")!,
            }
            API.post_category(json_data)
            .then(Response => Response.json())
            .then(data => {
                console.log(data)
                this.category.loading = false
                this.get_all_categories()
                this.category.title = ""
                this.category.description = ""
            })
        },
        get_category(id:any){
            this.selected_category = {}
            for (let i=0; i<this.categories_list.length; i++){
                if (this.categories_list[i].id == id){
                    this.selected_category = this.categories_list[i]
                    break
                }
            }
            this.request_category.title = this.selected_category.title
            this.request_category.description = this.selected_category.description
        },
        request_category_edit(request_type:string){
            let json_data = {
                "for_category": this.selected_category.id,
                "title": this.request_category.title,
                "description": this.request_category.description,
                "created_by": localStorage.getItem("user_id")!,
                "created_by_name": localStorage.getItem("user")!,
                "request_type": request_type
            }
            API.post_category_request(json_data)
            .then(Response => Response.json())
            .then(data => {
                let k = data
                this.get_all_categories()
                this.get_all_categories_request()
                console.log(k);
                this.request_category.title = ""
                this.request_category.description = ""
            })
        },
        compare_changes(category_id:any){
            // CURRENT VALUES
            this.get_category(category_id)

            // REQUESTED VALUES
            this.requested_category = {}
            for (let i=0; i<this.requested_categories_list.length; i++){
                if (this.requested_categories_list[i].for_category == category_id){
                    this.requested_category = this.requested_categories_list[i]
                    break
                }
            }
        },
        get_all_products(){
            API.get_all_products()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.product_list = k
                // console.log(this.product_list);
            })
        },
        submit_product_form(){
            console.log(this.product);
            
            API.post_product(this.product)
            .then(Response => Response.json())
            .then(data => {
                let k = data
                console.log(k);
                this.get_all_products()
                if (this.product_list.length > 0){
                    this.product.name = "",
                    this.product.description = "",
                    this.product.category_id = "Select",
                    this.product.m_date = "",
                    this.product.e_date = "",
                    this.product.stock = 0,
                    this.product.price = 0,
                    this.product.unit = "Choose a unit",
                    this.product.created_by = ""
                }
            })
        },
        edit_product(id:any){
            this.selected_product = {}
            for (let i=0; i<this.product_list.length; i++){
                if (this.product_list[i].id == id){
                    this.selected_product = {...this.product_list[i]}
                    this.selected_product.m_date = this.string_to_date(this.product_list[i].m_date)
                    this.selected_product.e_date = this.string_to_date(this.product_list[i].e_date)
                    break
                }
            }
        },
        submit_edit_product(){
            API.put_product(this.selected_product)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.get_all_products()
            })
        },
        delete_product(id:any){
            if (confirm(`Do you want to delete the product with ID: ${id}?`)){
                API.delete_product(id)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.get_all_products()
                })
            }
        }
    }
}
</script>

<template>
    <div class="container pb-2 ">
        <!-- FOR DISPLAYING ANY NOTIFICATION -->
        <div>
            <div v-for="msg in sse.greeting" class="alert alert-warning alert-dismissible fade show" role="alert">
                <strong>{{ msg }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            <div v-for="msg in sse.category_request" class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>{{ msg }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>

        <!-- TABLE FOR CATEGORY -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Category Management</h2>
                <button class="btn btn-outline-primary mb-2" data-bs-toggle="modal" data-bs-target="#historyRequestCategoryModal">View Request History</button>
                <button class="btn btn-outline-primary mb-2" data-bs-toggle="modal" data-bs-target="#addCategoryModal">Add Category</button>
            </div>
            <div style="overflow-x:auto;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>Category ID</th>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Status</th>
                            <!-- <th>Created By</th> -->
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="cat in categories_list">
                            <td>
                                {{ categories_list.indexOf(cat) + 1 }}
                            </td>
                            <td>{{cat.id}}</td>
                            <td>{{cat.title}}</td>
                            <td>{{cat.description}}</td>
                            <td>
                                <span v-if="cat.is_active">
                                    <span class="badge rounded-pill text-bg-success">Active</span>
                                </span>
                                <span v-else class="badge rounded-pill text-bg-warning">Pending...</span>
                            </td>
                            <!-- <td>{{cat.created_by + '-' + cat.created_by_name}}</td> -->
                            <td>
                                <div v-if="cat.is_active">
                                    <div v-if="!cat.request_status" v-on:click="get_category(cat.id)" class="badge text-bg-primary m-1" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#editCategoryModal">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                        </svg>
                                    </div>
                                    <div v-else>
                                        <span class="badge rounded-pill text-bg-info" v-on:click="compare_changes(cat.id)" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#viewRequestCategoryModal">View details of request</span>
                                    </div>
                                </div>
                                <div v-else>
                                    <span>Admin approval needed</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TABLE FOR PRODUCT MANAGEMENT -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Product Management</h2>
                <button class="btn btn-outline-primary mb-2" data-bs-toggle="modal" data-bs-target="#addProductModal">Add Product</button>
            </div>
            <div style="overflow-x:auto;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>Product ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Category</th>
                            <th>Manufacture Date</th>
                            <th>Expiry Date</th>
                            <th>Stock</th>
                            <th>Price</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in product_list">
                            <td>
                                {{ product_list.indexOf(product) + 1 }}
                            </td>
                            <td>{{product.id}}</td>
                            <td>{{product.name}}</td>
                            <td>{{product.description}}</td>
                            <td>{{product.category}}</td>
                            <td>{{product.m_date}}</td>
                            <td>{{product.e_date}}</td>
                            <td>{{product.stock}} {{ product.unit }}</td>
                            <td>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                    <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                </svg>
                                <span>{{product.price}} / {{ product.unit }}</span>
                            </td>
                            <td>
                                <div class="badge text-bg-primary m-1" style="cursor: pointer;" v-on:click="edit_product(product.id)" data-bs-toggle="modal" data-bs-target="#editProductModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                    </svg>
                                </div>
                                <div class="badge text-bg-danger m-1 " style="cursor: pointer;" v-on:click="delete_product(product.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                    </svg>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ADD CATEGORY MODAL -->
        <div class="modal fade" id="addCategoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Create New Category</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                <!-- ADD CATEGORY FORM -->
                <form class=" rounded-2 p-4">
                    <!-- TITLE INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_title">Title</label>
                    <input type="text" v-model="category.title" id="cat_title" class="form-control" placeholder="Enter Title" />
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="category.description" id="cat_desc" class="form-control" placeholder="Enter Description" />
                    </div>  
                </form>

                <!-- OTP INPUT -->
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <div v-if="!category.loading">
                    <button type="button" v-on:click="submit_category_form" class="btn btn-primary btn-block" data-bs-dismiss="modal">Submit</button>                    
                </div>
                <button v-else type="button" class="btn btn-outline-primary disabled mb-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </button>
                </div>
            </div>
            </div>
        </div>

        <!-- ADD PRODUCT MODAL -->
        <div class="modal fade" id="addProductModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Add New Product</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                <!-- ADD CATEGORY FORM -->
                <form class=" rounded-2 p-4">
                    <!-- NAME INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_title">Name</label>
                    <input type="text" v-model="product.name" id="cat_title" class="form-control" placeholder="Enter Product Name" />
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="product.description" id="cat_desc" class="form-control" placeholder="Enter Description" />
                    </div>

                    <!-- DEPARTMENT INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="department">Select Category</label>
                    <select name="department" id="department" v-model="product.category_id" class="form-control">
                        <option placeholder="Select a category" selected disabled>Select</option>
                        <option v-for="cat in categories_list" :value = cat.id >{{ cat.title }}</option>
                    </select>
                    </div>  

                    <!-- MANUFACTURE & EXPIRY DATE -->
                    <div class="d-flex justify-content-between ">
                        <!-- MANUFACTURE DATE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Manufacture Date</label>
                        <input type="date" v-model="product.m_date" id="cat_desc" class="form-control" />
                        </div>
                        
                        <!-- EXPIRY DATE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Expiry Date</label>
                        <input type="date" v-model="product.e_date" id="cat_desc" class="form-control" />
                        </div>
                    </div>

                    <!-- STOCK & PRICE -->
                    <div class="d-flex justify-content-between gap-2">
                        <!-- STOCK INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Stock</label>
                        <input type="number" v-model="product.stock" id="cat_desc" class="form-control" />
                        </div>
                        
                        <!-- PRICE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Price / Unit</label>
                        <input type="number" v-model="product.price" id="cat_desc" class="form-control" />
                        </div>

                        <!-- DEPARTMENT INPUT-->
                        <div class="form-outline mb-4 w-100">
                            <label class="form-label" for="unit">Unit</label>
                            <select name="unit" id="unit" v-model="product.unit" class="form-control">
                                <option placeholder="Select a unit" selected disabled>Choose a unit</option>
                                <option value="dozen" >Dozen</option>
                                <option value="kg" >Kg</option>
                                <option value="litre" >Litre</option>
                            </select>
                        </div>
                    </div>
                    
                </form>

                <!-- OTP INPUT -->
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <div v-if="!category.loading">
                    <button type="button" v-on:click="submit_product_form" class="btn btn-primary btn-block" data-bs-dismiss="modal">Submit</button>                    
                </div>
                <button v-else type="button" class="btn btn-outline-primary disabled mb-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </button>
                </div>
            </div>
            </div>
        </div>

        <!-- EDIT PRODUCT MODAL -->
        <div class="modal fade" id="editProductModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Edit Product</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                <!-- ADD CATEGORY FORM -->
                <form class=" rounded-2 p-4">
                    <!-- NAME INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_title">Name</label>
                    <input type="text" v-model="selected_product.name" id="cat_title" class="form-control" placeholder="Enter Product Name" />
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="selected_product.description" id="cat_desc" class="form-control" placeholder="Enter Description" />
                    </div>

                    <!-- DEPARTMENT INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="department">Select Category</label>
                    <select name="department" id="department" v-model="selected_product.category_id" class="form-control">
                        <option placeholder="Select a category" selected disabled>Select</option>
                        <option v-for="cat in categories_list" :value = cat.id >{{ cat.title }}</option>
                    </select>
                    </div>  

                    <!-- MANUFACTURE & EXPIRY DATE -->
                    <div class="d-flex justify-content-between ">
                        <!-- MANUFACTURE DATE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Manufacture Date</label>
                        <input type="date" v-model="selected_product.m_date" id="cat_desc" class="form-control" />
                        </div>
                        
                        <!-- EXPIRY DATE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Expiry Date</label>
                        <input type="date" v-model="selected_product.e_date" id="cat_desc" class="form-control" />
                        </div>
                    </div>

                    <!-- STOCK & PRICE -->
                    <div class="d-flex justify-content-between gap-2">
                        <!-- STOCK INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Stock</label>
                        <input type="number" v-model="selected_product.stock" id="cat_desc" class="form-control" />
                        </div>
                        
                        <!-- PRICE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Price / Unit</label>
                        <input type="number" v-model="selected_product.price" id="cat_desc" class="form-control" />
                        </div>

                        <!-- DEPARTMENT INPUT-->
                        <div class="form-outline mb-4 w-100">
                            <label class="form-label" for="unit">Unit</label>
                            <select name="unit" id="unit" v-model="selected_product.unit" class="form-control">
                                <option placeholder="Select a unit" selected disabled>Choose a unit</option>
                                <option value="dozen" >Dozen</option>
                                <option value="kg" >Kg</option>
                                <option value="litre" >Litre</option>
                            </select>
                        </div>
                    </div>
                    
                </form>

                <!-- OTP INPUT -->
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" v-on:click="submit_edit_product" class="btn btn-primary btn-block" data-bs-dismiss="modal">Submit</button>
                </div>
            </div>
            </div>
        </div>

        <!-- REQUEST EDIT CATEGORY MODAL -->
        <div class="modal fade" id="editCategoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Edit Category</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- ADD CATEGORY FORM -->
                    <form class=" rounded-2 p-4">
                        <!-- TITLE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_title">Title</label>
                        <input type="text" v-model="request_category.title" id="cat_title" class="form-control" placeholder="Enter Title" />
                        </div>

                        <!-- DESCRIPTION INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Description</label>
                        <input type="text" v-model="request_category.description" id="cat_desc" class="form-control" placeholder="Enter Description" />
                        </div>  
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" v-on:click="request_category_edit('delete')" class="btn btn-danger" data-bs-dismiss="modal">Request Delete</button>
                    <button type="button" v-on:click="request_category_edit('edit')" class="btn btn-primary btn-block" data-bs-dismiss="modal">Request Edit</button>
                </div>
            </div>
            </div>
        </div>

        <!-- VIEW REQUEST CATEGORY MODAL -->
        <div class="modal fade" id="viewRequestCategoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Details of request</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                <!-- ADD CATEGORY FORM -->
                <form class=" rounded-2 p-4 border border-2 border-danger mb-4">
                    <h4>Current Values</h4>
                    <!-- TITLE INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_title">Title</label>
                    <input type="text" v-model="selected_category.title" id="cat_title" class="form-control  border-2 border-danger" placeholder="Enter Title" disabled/>
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="selected_category.description" id="cat_desc" class="form-control border border-2 border-danger" placeholder="Enter Description" disabled/>
                    </div>  
                </form>
                <form class=" rounded-2 p-4 border border-2 border-success ">
                    <h4>Requested Values</h4>
                    <!-- TITLE INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_title">Title</label>
                    <input type="text" v-model="requested_category.title" id="cat_title" class="form-control border border-2 border-success" placeholder="Enter Title" disabled/>
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="requested_category.description" id="cat_desc" class="form-control border border-2 border-success" placeholder="Enter Description" disabled/>
                    </div>  
                </form>
                </div>
            </div>
            </div>
        </div>

        <!-- CATEGORY REQUEST HISTORY MODAL -->
        <div class="modal fade" id="historyRequestCategoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="registerLabel">Category Change Request History</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div style="overflow-x:auto;">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>S.No.</th>
                                    <th>Request ID</th>
                                    <th>Title</th>
                                    <th>Description</th>
                                    <th>Status</th>
                                    <th>Created By</th>
                                    <th>For Category(ID)</th>
                                    <th>Request Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="cat in category_change_history_list">
                                    <td>
                                        {{ category_change_history_list.indexOf(cat) + 1 }}
                                    </td>
                                    <td>{{cat.id}}</td>
                                    <td>{{cat.title}}</td>
                                    <td>{{cat.description}}</td>
                                    <td>
                                        <span v-if="cat.status == 'approved'" class="badge rounded-pill text-bg-primary">Approved</span>
                                        <span v-if="cat.status == 'pending'" class="badge rounded-pill text-bg-warning">Pending..</span>
                                        <span v-if="cat.status == 'declined'" class="badge rounded-pill text-bg-danger">Declined</span> <br>
                                    </td>
                                    <td>{{cat.created_by + '-' + cat.created_by_name}}</td>
                                    <td>{{cat.for_category}}</td>
                                    <td class="fw-semibold text-uppercase">
                                        <span v-if="cat.request_type == 'edit'" class="text-primary">{{cat.request_type}}</span>
                                        <span v-else class="text-danger">{{cat.request_type}}</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>