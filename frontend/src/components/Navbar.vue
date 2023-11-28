<script lang="ts">
export default {
    data: () => {
        return {
            name:""
        }
    },
    methods: {
        logout(){
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            localStorage.removeItem("user")
            this.$router.push({path:'/login'})
        }
    },
    beforeMount(){
        this.name = localStorage.getItem("user")!
    }
}
</script>

<template>
    <nav class="d-flex container justify-content-between pt-2 pb-2 ">
        <span class="fs-3 fw-bold">{{ name }}</span>
        <button class="btn btn-danger" v-on:click="logout">Log Out</button>
    </nav>
</template>