<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_categories()
        this.get_all_categories_request()
        this.get_all_products()
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
        }
    },
    methods: {
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
                console.log(this.product_list);
            })
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