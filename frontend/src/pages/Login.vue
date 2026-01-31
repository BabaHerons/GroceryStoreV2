<script lang="ts">

import API from "../api";

export default {
    data: function() {
        return {
            email:"",
            password:"",
            sm_full_name:"",
            sm_email:"",
            sm_password:"",
            sm_otp:"",
            fp_email:"",
            fp_otp:"",
            new_password:"",
            full_name:"",
            signUp_email:"",
            signUp_password:"",
            token:"",
            otp:"",
            global_error:"",
            login_page_success:"",
            login:{
                loading:false,
                error:false,
                error_msg:""
            },
            register:{
                loading:false,
                view_otp:false,
                error:false,
                error_msg:""
            },
            sm_register:{
                loading:false,
                view_otp:false,
                error:false,
                error_msg:""
            },
            forgot_password:{
              loading:false,
              view_otp:false,
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
                    localStorage.setItem("user", k.full_name)
                    localStorage.setItem("user_id", k.user_id)
                    localStorage.removeItem("global_error")
                    this.$router.push({path:'/'})
                }
            })
        },
        submit_signup_form(){
          if (this.full_name == "" || this.signUp_email == "" || this.signUp_password == ""){}
          else {
            this.register.loading = true
            let json_data = {
              "full_name":this.full_name,
              "email":this.signUp_email,
              "password":this.signUp_password,
              "role":"user"
            }
  
            // API CALL FOR SIGN UP
            API.sign_up(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.register.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.register.error){
                console.log(k.message)
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.register.view_otp = true
                this.register.loading = false
                console.log("Sign Up Data:", k)
              }
            })
          }
        },
        signUp() {
          if (this.otp == ""){}
          else {
            let json_data = {"otp":this.otp}
            API.sign_up_otp(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.register.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.register.error){
                console.log(k.message)
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.register.view_otp = false
                this.register.loading = false
                console.log("Sign Up Data:", k)
                this.login_page_success = "Sign Up Successfull."
                setTimeout(() => {
                    this.login_page_success = ""
                }, 3500);
              }
            })
          }
        },
        submit_sm_signup_form(){
          if (this.sm_email == "" || this.sm_full_name == "" || this.sm_password == ""){}
          else {
            this.sm_register.loading = true
            let json_data = {
              "full_name":this.sm_full_name,
              "email":this.sm_email,
              "password":this.sm_password,
              "role":"store_admin"
            }
  
            // API CALL FOR SIGN UP
            API.sign_up(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.sm_register.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.sm_register.error){
                console.log(k.message)
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.sm_register.view_otp = true
                this.sm_register.loading = false
                console.log("Sign Up Data:", k)
              }
            })
          }
        },
        sm_signUp() {
          if (this.sm_otp == ""){}
          else {
            let json_data = {"otp":this.sm_otp}
            API.sign_up_otp(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.sm_register.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.sm_register.error){
                console.log(k.message)
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.sm_register.view_otp = false
                this.sm_register.loading = false
                this.login_page_success = "Sign Up Successfull."
                setTimeout(() => {
                    this.login_page_success = ""
                }, 3500);
              }
            })
          }
        },
        submit_email(){
          if (this.fp_email == ""){}
          else {
            this.forgot_password.loading = true
            const json_data = {"email":this.fp_email}

            // API CALL FOR SIGN UP
            API.send_fp_email(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.forgot_password.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.forgot_password.error){
                console.log(k.message)
                this.forgot_password.loading = false
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.forgot_password.view_otp = true
                this.forgot_password.loading = false
              }
            })
          }
        },
        submit_new_password(){
          if (this.fp_otp == "" || this.new_password == ""){}
          else {
            let json_data = {"otp":this.fp_otp, "email":this.fp_email, "password":this.new_password}
            API.send_fp_otp_pass(json_data)
            .then(Response => {
              let response = Response
              if (response.status != 200){
                this.forgot_password.error = true
              }
              return response.json()
            })
            .then(data => {
              let k = data
              if (this.forgot_password.error){
                console.log(k.message)
                this.global_error = k.message
                setTimeout(() => {
                    this.global_error = ""
                }, 3500);
              } else {
                this.forgot_password.view_otp = false
                this.forgot_password.loading = false
                this.login_page_success = "Sign Up Successfull."
                setTimeout(() => {
                    this.login_page_success = ""
                }, 3500);
              }
            })
          }
        }
    },
    beforeMount() {
      // ERROR ON LOGIN PAGE
      if (localStorage.getItem("global_error")){
          this.global_error = localStorage.getItem("global_error")!
          setTimeout(() => {
              this.global_error = ""
              localStorage.removeItem("global_error")
          }, 5000);
      }

      // CHECKING IF TOKEN EXISTS
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
      <div v-if="login_page_success" class="alert alert-success" role="alert">
        {{login_page_success}}
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
      <p>Want to join as a store manager? <span class="text-primary text-decoration-underline " style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#registerSMModal">Register</span></p>
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
              <!-- FORGOT PASSWORD EMAIL FORM -->
              <form v-if="!forgot_password.view_otp" class=" rounded-2 p-4">
                <!-- EMAIL INPUT-->
                <div class="form-outline mb-4">
                  <label class="form-label" for="email">Email address</label>
                  <input type="email" v-model="fp_email" id="email" class="form-control" placeholder="Enter email" />
                </div>                
              </form>
              
              <!-- New Password & OTP -->
              <form v-else>
                <!-- OTP INPUT -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="otp">OTP</label>
                  <input type="number" v-model="fp_otp" id="otp" class="form-control" placeholder="Enter otp" />
                </div>
                
                <!-- PASSWORD INPUT -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="password">Password</label>
                  <input type="password" v-model="new_password" id="password" class="form-control" placeholder="Enter password" />
                </div>  
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" v-on:click="() => {forgot_password.view_otp = false}">Close</button>
              <div v-if="!forgot_password.loading">
                <button v-if="!forgot_password.view_otp" type="button" v-on:click="submit_email" class="btn btn-primary btn-block">Submit</button>
                <button v-else data-bs-dismiss="modal" type="button" v-on:click="submit_new_password" class="btn btn-primary btn-block">Update Password</button>
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

    <!-- REGISTER USER MODAL -->
    <div class="modal fade" id="registerModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="registerLabel">Sign Up</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <!-- SIGN UP FORM -->
              <form v-if="!register.view_otp" class=" rounded-2 p-4">
                <!-- FULL NAME INPUT-->
                <div class="form-outline mb-4">
                  <label class="form-label" for="full_name">Full Name</label>
                  <input type="text" v-model="full_name" id="full_name" class="form-control" placeholder="Enter full name" />
                </div>

                <!-- EMAIL INPUT-->
                <div class="form-outline mb-4">
                  <label class="form-label" for="email">Email address</label>
                  <input type="email" v-model="signUp_email" id="email" class="form-control" placeholder="Enter email" />
                </div>
                
                <!-- PASSWORD INPUT -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="password">Password</label>
                  <input type="password" v-model="signUp_password" id="password" class="form-control" placeholder="Enter password" />
                </div>  
              </form>

              <!-- OTP INPUT -->
              <form v-else>
                <div class="form-outline mb-4">
                  <label class="form-label" for="otp">OTP</label>
                  <input type="number" v-model="otp" id="otp" class="form-control" placeholder="Enter otp" />
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" v-on:click="() => {register.view_otp = false}">Close</button>
              <div v-if="!register.loading">
                <button v-if="!register.view_otp" type="button" v-on:click="submit_signup_form" class="btn btn-primary btn-block">Submit</button>
                <button v-else data-bs-dismiss="modal" type="button" v-on:click="signUp" class="btn btn-primary btn-block">Sign Up</button>
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
    
    <!-- REGISTER STORE MANAGER MODAL -->
    <div class="modal fade" id="registerSMModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="registerLabel">Sign Up Store Manager</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <!-- SIGN UP FORM -->
              <form v-if="!sm_register.view_otp" class=" rounded-2 p-4">
                <!-- FULL NAME INPUT-->
                <div class="form-outline mb-4">
                  <label class="form-label" for="full_name">Full Name</label>
                  <input type="text" v-model="sm_full_name" id="full_name" class="form-control" placeholder="Enter full name"/>
                </div>

                <!-- EMAIL INPUT-->
                <div class="form-outline mb-4">
                  <label class="form-label" for="email">Email address</label>
                  <input type="email" v-model="sm_email" id="email" class="form-control" placeholder="Enter email" />
                </div>
                
                <!-- PASSWORD INPUT -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="password">Password</label>
                  <input type="password" v-model="sm_password" id="password" class="form-control" placeholder="Enter password" />
                </div>  
              </form>

              <!-- OTP INPUT -->
              <form v-else>
                <div class="form-outline mb-4">
                  <label class="form-label" for="otp">OTP</label>
                  <input type="number" v-model="sm_otp" id="otp" class="form-control" placeholder="Enter otp" />
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" v-on:click="() => {sm_register.view_otp = false}">Close</button>
              <div v-if="!sm_register.loading">
                <button v-if="!sm_register.view_otp" type="button" v-on:click="submit_sm_signup_form" class="btn btn-primary btn-block">Submit</button>
                <button v-else data-bs-dismiss="modal" type="button" v-on:click="sm_signUp" class="btn btn-primary btn-block">Sign Up</button>
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
</template>
