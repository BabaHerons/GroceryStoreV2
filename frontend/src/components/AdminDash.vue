<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_users()
    },
    data: () => {
        return {
            all_users:[] as any[],
            sm_list:[] as any[],
            user_list:[] as any[]
        }
    },
    methods: {
        get_all_users(){
            API.get_users()
            .then(response => response.json())
            .then(data => {
                let k = data
                console.log(k);

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
        }
    }
}
</script>

<template>
    <div class="container pb-2 ">
        <!-- TABLE FOR STORE/INVENTORY MANAGER -->
        <div class="mt-4 mb-4">
            <h2 class="text-secondary">Store / Inventory Manager</h2>
            <div style="overflow-x:auto;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>User ID</th>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Active</th>
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
            <h2 class="text-secondary">Users</h2>
            <div style="overflow-x:auto;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>User ID</th>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Active</th>
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

        <!-- TABLE FOR USERS -->
        <div class="mt-4 mb-4">
            <h2 class="text-secondary">Category Management</h2>
            <div style="overflow-x:auto;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>User ID</th>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Active</th>
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
</template>