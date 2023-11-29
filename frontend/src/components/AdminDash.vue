<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_users()
        this.get_all_categories()
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
            API.get_categories()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.categories_list = k
                console.log(this.categories_list);
                
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
        patch_category_form(){
            this.patch_category.loading = true
            let json_data = {
                "title": this.patch_category.title,
                "description": this.patch_category.description,
                "created_by": localStorage.getItem("user_id")!,
                "created_by_name": localStorage.getItem("user")!,
            }
            API.patch_category(json_data)
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
        }
    }
}
</script>

<template>
    <div class="container pb-2 ">
        <!-- TABLE FOR STORE/INVENTORY MANAGER -->
        <div class="mt-4 mb-4">
            <h2 class="text-secondary border-bottom border-black">Store / Inventory Manager</h2>
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
                                    <span class="badge rounded-pill text-bg-warning" v-on:click="activate_manager(sm.id)" style="cursor: pointer;">Activate Manager</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TABLE FOR USERS -->
        <div class="mt-4 mb-4">
            <h2 class="text-secondary border-bottom border-black">Users</h2>
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

        <!-- TABLE FOR CATEGORY -->
        <div class="mt-4 mb-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">Category Management</h2>
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
                                    <!-- <span class="badge rounded-pill text-bg-danger">Inactive</span> <br> -->
                                    <span class="badge rounded-pill text-bg-info" style="cursor: pointer;">Approve</span>
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
                                <div class="badge text-bg-danger m-1 " style="cursor: pointer;">
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
                    <button type="button" v-on:click="patch_category_form" class="btn btn-primary btn-block" data-bs-dismiss="modal">Submit</button>                    
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
    </div>
</template>