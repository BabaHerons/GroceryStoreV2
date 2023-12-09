<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_users()
        this.get_all_categories()
        this.get_pending_category()
        this.get_all_products()
        this.get_all_orders()
        this.get_monthly_sales_report()
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
        source.addEventListener("cat_req", (event:any) => {
            const data = JSON.parse(event.data)
            this.sse.category_request.push(data.message)
            this.get_pending_category()
            this.get_all_categories()
        })
    },
    data: () => {
        return {
            all_users:[] as any[],
            sm_list:[] as any[],
            user_list:[] as any[],
            categories_list:[] as any [],
            category:{
                loading:false,
                title:"",
                description:"",
                created_by:"",
                created_by_name:""
            },
            patch_category:{
                loading:false,
                title:"",
                description:"",
                created_by:"",
                created_by_name:""
            },
            selected_category:{} as any,
            pending_category_list:[] as any[],
            pending_category:{} as any,
            category_change_history_list:[] as any[],
            sse:{
                greeting:[] as any[],
                category_request:[] as any[],
                new_category:[] as any[],
            },
            product_list:[] as any[],
            order_history:[] as any[],
            order_details:{} as any,
            total_earning:0,
            sr_product:"",
            sr_category:"",
        }
    },
    methods: {
        get_all_users(){
            API.get_users()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.all_users = []
                this.sm_list = []
                this.user_list = []

                this.all_users = k
                for (let i=0; i < k.length; i++){
                    if (k[i].role == "user"){
                        this.user_list.push(k[i])
                    } else {
                        if (k[i].role == "admin"){}
                        else{
                            this.sm_list.push(k[i])
                        }
                    }
                }
            })
        },
        activate_manager(user_id:any){
            let json_data = {
                "user_id":user_id,
                "is_active": true
            }
            
            let status_code = 0
            API.activate_manager(json_data)
            .then(response => {
                status_code = response.status
                return response.json()
            })
            .then(data => {
                let k = data
                console.log(k)
                if (status_code == 200){
                    this.get_all_users()
                }
            })
        },
        get_all_categories(){
            this.categories_list = []
            API.get_categories()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.categories_list = k
                // console.log(this.categories_list);
                
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
                let k = data
                this.category.loading = false
                this.get_all_categories()
                console.log(k);
                this.category.title = ""
                this.category.description = ""
            })
        },
        put_category_form(){
            this.patch_category.loading = true
            let json_data = {
                "category_id": this.selected_category.id,
                "title": this.patch_category.title,
                "description": this.patch_category.description,
                "created_by": localStorage.getItem("user_id")!,
                "created_by_name": localStorage.getItem("user")!,
            }
            API.put_category(json_data)
            .then(Response => Response.json())
            .then(data => {
                let k = data
                this.patch_category.loading = false
                this.get_all_categories()
                console.log(k);
                this.patch_category.title = ""
                this.patch_category.description = ""
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
            this.patch_category.title = this.selected_category.title
            this.patch_category.description = this.selected_category.description
        },
        approve_category(id:any){
            API.patch_category_approve(id)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                this.get_all_categories()
            })
        },
        delete_category(id:any, title:any){
            if (confirm(`Do you want to delete the category with ID-Title: ${id}-${title} ?`)){
                API.delete_category(id)
                .then(Response => Response.json())
                .then(data => {
                    console.log(data);
                    this.get_all_categories()
                })
            }            
        },
        get_pending_category(){
            this.pending_category_list = []
            API.get_categories_request()
            .then(Response => Response.json())
            .then(data => {
                let k = data
                this.category_change_history_list = k
                for (let i=0; i<k.length; i++){
                    if (k[i].status == "pending"){
                        this.pending_category_list.push(k[i])
                    }
                }
            })
        },
        compare_changes(category_id:any){
            // CURRENT VALUES
            this.get_category(category_id)

            // REQUESTED VALUES
            this.pending_category = {}
            for (let i=0; i<this.pending_category_list.length; i++){
                if (this.pending_category_list[i].for_category == category_id){
                    this.pending_category = this.pending_category_list[i]
                    break
                }
            }            
        },
        respond_cat_change_request(response:any){
            this.pending_category.status = response
            if (this.pending_category.request_type == "edit"){
                API.patch_category_request(this.pending_category)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.get_all_categories()
                    this.get_pending_category()
                })
            } else {
                let json_data = {
                    "id":this.pending_category.id,
                    "status":"",
                    "for_category":this.pending_category.for_category
                    }
                if (response == "approved"){
                    if (confirm("Proceed with delete?")){
                        json_data.status = "approved"
                    }
                } else {
                    json_data.status = "declined"
                }
                API.delete_category_request(json_data)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.get_all_categories()
                    this.get_pending_category()
                })
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
        get_all_orders(){
            this.order_history = []
            API.get_orders()
            .then(response => response.json())
            .then(data => {
                this.order_history = data
                
                this.total_earning = 0
                for (let i=0; i<this.order_history.length; i++){
                    this.total_earning += Number(this.order_history[i].amount)
                }
            })
        },
        get_order_details(order_id:any){
            this.order_details = {}
            for (let i=0; i<this.order_history.length; i++){
                if (this.order_history[i].id == order_id){
                    this.order_details = this.order_history[i]
                    break
                }
            }
        },
        export_product_list(){
            API.export_products_csv()
            .then(resp => resp.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(url => {
                window.open(url, '_blank');
                URL.revokeObjectURL(url);
            });
        },
        get_monthly_sales_report(){
            // FOR PRODUCTS
            API.monthly_sales_report_products()
            .then(resp => resp.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(url => {
                this.sr_product = url
            });

            // FOR CATEGORY
            API.monthly_sales_report_category()
            .then(resp => resp.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(url => {
                this.sr_category = url
            });
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
            <div v-for="msg in sse.category_request" class="alert alert-info alert-dismissible fade show" role="alert">
                <strong>{{ msg }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>
        
        <!-- TABLE FOR PENDING CATEGORY -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Pending Category Requests</h2>
                <button class="btn btn-primary mb-2" data-bs-toggle="modal" data-bs-target="#historyRequestCategoryModal">View Request History</button>
            </div>
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
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="pending_category_list.length > 0">
                        <tr v-for="cat in pending_category_list">
                            <td>
                                {{ pending_category_list.indexOf(cat) + 1 }}
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
                            <td>
                                <span class="badge rounded-pill text-bg-secondary" style="cursor: pointer;" v-on:click="compare_changes(cat.for_category)" data-bs-toggle="modal" data-bs-target="#viewRequestCategoryModal">Respond</span>
                            </td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="100" class="text-center text-primary fw-bold"><span>No Pending Requests.</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TABLE FOR STORE/INVENTORY MANAGER -->
        <div class="mt-4 mb-4">
            <h2 class="text-secondary border-bottom border-black">Store / Inventory Manager</h2>
            <!-- ACCORDIAN FOR STORE/INVENTORY MANAGER -->
            <div class="accordion mt-4 mb-4" id="accordionPanelsStayOpenExample">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <h1 class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelSM" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                        Store/Inventory Manager Table
                    </h1>
                </h2>
                <div id="panelSM" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <div style="overflow-x:auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>S.No.</th>
                                        <th>User ID</th>
                                        <th>Full Name</th>
                                        <th>Email</th>
                                        <th>Role</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="sm in sm_list">
                                        <td>
                                            {{ sm_list.indexOf(sm) + 1 }}
                                        </td>
                                        <td>{{sm.id}}</td>
                                        <td>{{sm.full_name}}</td>
                                        <td>{{sm.email}}</td>
                                        <td>{{sm.role}}</td>
                                        <td>
                                            <span v-if="sm.is_active">
                                                <span class="badge rounded-pill text-bg-success">Active</span>
                                            </span>
                                            <div v-else>
                                                <span class="badge rounded-pill text-bg-danger">Inactive</span> <br>
                                                <span class="badge rounded-pill text-bg-secondary" v-on:click="activate_manager(sm.id)" style="cursor: pointer;">Activate Manager</span>
                                            </div>
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

        <!-- TABLE FOR CATEGORY MANAGEMENT-->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Category Management</h2>
                <button class="btn btn-primary mb-2" data-bs-toggle="modal" data-bs-target="#addCategoryModal">Add Category</button>
            </div>
            <!-- ACCORDIAN FOR CATEGPRU MANAGEMENT -->
            <div class="accordion mt-4 mb-4" id="accordionPanelsStayOpenExample">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <h1 class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelCategoryManagement" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                    Category Management Table
                    </h1>
                </h2>
                <div id="panelCategoryManagement" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <div style="overflow-x:auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>S.No.</th>
                                        <th>Category ID</th>
                                        <th>Title</th>
                                        <th>Description</th>
                                        <th>Status</th>
                                        <th>Created By</th>
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
                                            <div v-else>
                                                <span class="badge rounded-pill text-bg-warning">Pending...</span> <br>
                                            </div>
                                        </td>
                                        <td>{{cat.created_by + '-' + cat.created_by_name}}</td>
                                        <td v-if="cat.is_active">
                                            <div class="badge text-bg-primary m-1" style="cursor: pointer;" v-on:click="get_category(cat.id)" data-bs-toggle="modal" data-bs-target="#editCategoryModal">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                                </svg>
                                            </div>
                                            <div class="badge text-bg-danger m-1 " v-on:click="delete_category(cat.id, cat.title)" style="cursor: pointer;">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                                </svg>
                                            </div>
                                        </td>
                                        <td v-else>
                                            <span v-on:click="approve_category(cat.id)" class="badge rounded-pill text-bg-secondary" style="cursor: pointer;">Approve</span>
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

        <!-- TABLE FOR USERS -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Users</h2>
                <button class="btn btn-primary mb-2" data-bs-toggle="modal" data-bs-target="#orderHistoryModal">Order History</button>
            </div>
            <!-- ACCORDIAN FOR ALL USERS -->
            <div class="accordion mt-4 mb-4" id="accordionPanelsStayOpenExample">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <h1 class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelUserList" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                    Users Table
                    </h1>
                </h2>
                <div id="panelUserList" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <div style="overflow-x:auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>S.No.</th>
                                        <th>User ID</th>
                                        <th>Full Name</th>
                                        <th>Email</th>
                                        <th>Role</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in user_list">
                                        <td>
                                            {{ user_list.indexOf(user) + 1 }}
                                        </td>
                                        <td>{{user.id}}</td>
                                        <td>{{user.full_name}}</td>
                                        <td>{{user.email}}</td>
                                        <td>{{user.role}}</td>
                                        <td>
                                            <span v-if="user.is_active">
                                                <span class="badge rounded-pill text-bg-success">Active</span>
                                            </span>
                                            <span v-else class="badge rounded-pill text-bg-danger">Inactive</span>
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

        <!-- TABLE FOR PRODUCTS -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Products List</h2>
                <button class="btn btn-primary mb-2" v-on:click="export_product_list">Export Product List</button>

            </div>
            <!-- ACCORDIAN FOR ALL ORDERS -->
            <div class="accordion mt-4 mb-4" id="accordionPanelsStayOpenExample">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <h1 class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelProductList" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                    Product List
                    </h1>
                </h2>
                <div id="panelProductList" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <div style="overflow-x:auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>S.No.</th>
                                        <th>Product ID</th>
                                        <th>Category</th>
                                        <th>Name</th>
                                        <th>Description</th>
                                        <th>Manufacture Date</th>
                                        <th>Expiry Date</th>
                                        <th>Stock</th>
                                        <th>Price</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="product in product_list">
                                        <td>
                                            {{ product_list.indexOf(product) + 1 }}
                                        </td>
                                        <td>{{product.id}}</td>
                                        <td class="text-info">{{product.category}}</td>
                                        <td class="text-primary fw-semibold ">{{product.name}}</td>
                                        <td>{{product.description}}</td>
                                        <td>{{product.m_date}}</td>
                                        <td>{{product.e_date}}</td>
                                        <td>{{product.stock}} {{ product.unit }}</td>
                                        <td>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                                <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                            </svg>
                                            <span>{{product.price}} / {{ product.unit }}</span>
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

        <!-- MONTHLY SALES REPORT -->
        <div class="mt-5 mb-4">
            <div class="d-flex justify-content-center border-bottom border-black">
                <h2 class="text-secondary">Monthly Sales Report</h2>
            </div>
            <!-- ACCORDIAN FOR ALL ORDERS -->
            <div class="accordion mt-4 mb-4" id="accordionPanelsStayOpenExample">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <h1 class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelMonthlyReportList" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                    Monthly Report
                    </h1>
                </h2>
                <div id="panelMonthlyReportList" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <div class="d-flex flex-column mt-5">
                            <div class="d-flex flex-column">
                                <h3 class="text-center">Products-Wise</h3>
                                <img v-bind:src="sr_product" alt="Products Monthly Sales Report">
                            </div>
                            <div class="d-flex flex-column mt-5 ">
                                <h3 class="text-center mt-5">Category-Wise</h3>
                                <img v-bind:src="sr_category" alt="Products Monthly Sales Report">
                            </div>
                        </div>
                    </div>
                </div>
                </div>
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

        <!-- EDIT CATEGORY MODAL -->
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
                    <input type="text" v-model="patch_category.title" id="cat_title" class="form-control" placeholder="Enter Title" />
                    </div>

                    <!-- DESCRIPTION INPUT-->
                    <div class="form-outline mb-4">
                    <label class="form-label" for="cat_desc">Description</label>
                    <input type="text" v-model="patch_category.description" id="cat_desc" class="form-control" placeholder="Enter Description" />
                    </div>  
                </form>

                <!-- OTP INPUT -->
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <div v-if="!patch_category.loading">
                    <button type="button" v-on:click="put_category_form" class="btn btn-primary btn-block" data-bs-dismiss="modal">Submit</button>                    
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

        <!-- VIEW REQUEST CATEGORY MODAL -->
        <div class="modal fade" id="viewRequestCategoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="registerLabel">Details of request</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- CURRENT VALUES -->
                    <form class=" rounded-2 p-4 border border-2 border-danger mb-4">
                        <h4 v-if="pending_category.request_type == 'edit'">Current Values</h4>
                        <h4 v-else>Delete Current Values</h4>
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

                    <!-- REQUESTED VALUES -->
                    <form v-if="pending_category.request_type == 'edit'" class=" rounded-2 p-4 border border-2 border-success ">
                        <h4>Requested Values</h4>
                        <!-- TITLE INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_title">Title</label>
                        <input type="text" v-model="pending_category.title" id="cat_title" class="form-control border border-2 border-success" placeholder="Enter Title" disabled/>
                        </div>

                        <!-- DESCRIPTION INPUT-->
                        <div class="form-outline mb-4">
                        <label class="form-label" for="cat_desc">Description</label>
                        <input type="text" v-model="pending_category.description" id="cat_desc" class="form-control border border-2 border-success" placeholder="Enter Description" disabled/>
                        </div>  
                    </form>
                </div>
                <div class="modal-footer">
                    <button data-bs-dismiss="modal" class="btn btn-danger" v-on:click="respond_cat_change_request('declined')">Decline</button>
                    <button data-bs-dismiss="modal" class="btn btn-primary" v-on:click="respond_cat_change_request('approved')">Approve</button>
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

        <!-- ORDER HISTORY MODAL -->
        <div class="modal fade" id="orderHistoryModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="registerLabel">Order History</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div style="overflow-x:auto;">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Order ID</th>
                                    <th>Date</th>
                                    <th>Amount</th>
                                    <th>User</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="cat in order_history">
                                    <td>{{cat.id}}</td>
                                    <td>{{cat.date}}</td>
                                    <td>
                                        <div class="d-flex align-items-center ">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                                <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                            </svg><span>{{cat.amount}}</span>
                                        </div>
                                    </td>
                                    <td>{{ cat.user_id }}-{{ cat.user_full_name }}</td>
                                    <td>
                                        <button class="btn btn-warning" v-on:click="get_order_details(cat.id)" data-bs-toggle="modal" data-bs-target="#orderDetailsModal">More</button>
                                    </td>                                    
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <div class="d-flex">Total Earnings:
                        <div class="d-flex align-items-center text-success fw-bold">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                            </svg><span>{{ total_earning }}</span>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>

        <!-- ORDER DETAILS MODAL -->
        <div class="modal fade" id="orderDetailsModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="registerLabel">Order Details</h1>
                    <button type="button" class="btn-close" data-bs-toggle="modal" data-bs-target="#orderHistoryModal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="d-flex flex-wrap justify-content-center">
                        <div v-for="product in order_details.products">
                            <div class="card m-2 shadow-sm" style="width: 18rem;">
                                <div class="card-body">
                                  <!-- PRODUCT NAME -->
                                  <span class="text-secondary">{{ product.category }}</span>
                                  <h5 class="card-title">{{ product.name }}</h5>
                                  <span>{{ product.product_id }}</span>

                                  <!-- PRICE & QUANTITY DETAILS -->
                                  <div class="mt-2 mb-2 fw-semibold d-flex justify-content-between ">
                                    <!-- PRICE OF PRODUCT -->
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                            <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                        </svg>
                                        <span>{{ product.price }} / {{ product.unit }}</span>
                                    </div>
                                    <div>
                                        <label for="quantity">Quantity</label> &nbsp;
                                        <input style="width: 50px;" type="number" v-model="product.quantity" name="quantity" id="quantity" disabled>
                                    </div>
                                  </div>
                                
                                  <!-- ITEM TOTAL & DELETE BUTTON -->
                                  <div class="d-flex justify-content-between fw-semibold mt-4">
                                    <div class="text-primary">
                                        <span>Total:</span>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                            <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                        </svg>
                                        <span>{{ product.item_total }}</span>
                                    </div>
                                  </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer d-flex justify-content-between ">
                    <p>Order ID: <span class="fw-semibold">{{ order_details.id }}</span></p>
                    <p>Order Total: 
                        <span class="text-primary fw-bold ">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                            </svg> {{ order_details.amount }}
                        </span>
                    </p>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>