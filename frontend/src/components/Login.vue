<script lang="ts">

import API from "../api.ts";

export default {
    data: function() {
        return {
            email:"",
            password:"",
            token:"",
            global_error:"",
            login:{
                loading:false,
                error:false,
                error_msg:""
            },
            register:{
                toggle:false,
                loading:false,
                error:false,
                error_msg:""
            },
            forgot_password:{
                toggle:false,
                loading:false,
                error:false,
                error_msg:""
            },
        };
    },
    methods: {
        submit() {
            this.login.loading = true

            // JSON DATA TO BE SENT WITH API
            let json_data = {
                email: this.email,
                password:this.password
            }

            // API CALL FOR LOGIN
            API.login(json_data)
            .then(response => {
                this.login.loading = false
                if (response.status != 200){
                    this.login.error = true
                }
                return response.json()
            })
            .then(data => {
                let k = data
                if (this.login.error){
                    this.login.error_msg = k.message
                    setTimeout(() => {
                        this.login.error = false
                    }, 2000);
                } else {
                    localStorage.setItem("token", k.token)
                    localStorage.setItem("role", k.role)
                    localStorage.removeItem("global_error")
                    this.$router.push({path:'/'})
                }
            })
        },
    },
    beforeMount() {
        if (localStorage.getItem("global_error")){
            this.global_error = localStorage.getItem("global_error")!
            setTimeout(() => {
                this.global_error = ""
                localStorage.removeItem("global_error")
            }, 5000);
        }
       if (localStorage.getItem("token")){
        this.$router.push({path:'/'})
       }
    },
}
</script>

<template>
    <!-- LOGIN DIV -->
    <div id="login_form" class="container d-flex flex-column  justify-content-center align-items-center" style="height: 100vh;">
      <div v-if="login.error" class="alert alert-danger" role="alert">
        {{login.error_msg}}
      </div>
      <div v-if="global_error" class="alert alert-danger" role="alert">
        {{global_error}}
      </div>
      <h2 class="mb-4">Groccery App</h2>
      <form class="w-50 border border-primary rounded-2 p-4">
        <h1 class="mb-4">Login</h1>
        <div class="bg-primary w-25 mb-4" style="height:3px"></div>
        <!-- EMAIL INPUT-->
        <div class="form-outline mb-4">
          <label class="form-label" for="email">Email address</label>
          <input type="email" v-model="email" id="email" class="form-control" placeholder="Enter email" />
        </div>
      
        <!-- PASSWORD INPUT -->
        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input type="password" v-model="password" id="password" class="form-control" placeholder="Enter password" />
        </div>
      
        <!-- FORGOT PASSWORD -->
        <div class="row">    
          <div class="col">
            <span class="text-primary text-decoration-underline " style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#forgotPasswordModal">Forgot password?</span>
          </div>
        </div>
      
        <!-- SUBMIT BUTTON -->
        <div class="d-flex flex-row-reverse">
          <button v-if="!login.loading" type="button" v-on:click="submit" class="btn btn-primary btn-block mb-4">Log in</button>
          <button v-else type="button" class="btn btn-outline-primary disabled mb-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
          </button>
        </div>
      
        <!-- REGISTER BUTTON -->
        <div class="text-center">
          <p>Not a member? <span class="text-primary text-decoration-underline " style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#registerModal">Register</span></p>
        </div>
      </form>
      <p>Want to join as a store manager <span class="text-primary text-decoration-underline " style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#registerModal">Register</span></p>
    </div>

    <!-- FORGOT PASSWORD MODAL -->
    <div class="modal fade" id="forgotPasswordModal" tabindex="-1" aria-labelledby="forgotPasswordLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="forgotPasswordLabel">Forgot Pasword</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              ...
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary">Save changes</button>
            </div>
          </div>
        </div>
    </div>

    <!-- REGISTER USER MODAL -->
    <div class="modal fade" id="registerModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="registerLabel">Sign Up</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              ...
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary">Save changes</button>
            </div>
          </div>
        </div>
    </div>
</template>
