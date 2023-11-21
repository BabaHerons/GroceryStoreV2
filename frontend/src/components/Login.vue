<template>
    <div class="container d-flex flex-column  justify-content-center align-items-center" style="height: 100vh;">
      <h2 class="mb-4">Groccery App</h2>
      <form class="w-50 border border-primary rounded-2 p-4">
        <h1 class="mb-4">Login</h1>
        <div class="bg-primary w-25 mb-4" style="height:3px"></div>
        <!-- EMAIL INPUT-->
        <div class="form-outline mb-4">
          <label class="form-label" for="email">Email address</label>
          <input type="email" id="email" class="form-control" />
        </div>
      
        <!-- PASSWORD INPUT -->
        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input type="password" id="password" class="form-control" />
        </div>
      
        <!-- FORGOT PASSWORD -->
        <div class="row">    
          <div class="col">
            <a href="#!">Forgot password?</a>
          </div>
        </div>
      
        <!-- SUBMIT BUTTON -->
        <div class="d-flex flex-row-reverse">
          <button type="button" class="btn btn-outline-primary btn-block mb-4">Sign in</button>
        </div>
      
        <!-- REGISTER BUTTON -->
        <div class="text-center">
          <p>Not a member? <a href="#!">Register</a></p>
        </div>
      </form>
    </div>
  </template>
  