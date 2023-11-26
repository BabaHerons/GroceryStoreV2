<script lang="ts">
import API from '../api';

export default {
    beforeMount() {
        API.verify_token()
        this.role = localStorage.getItem("role")!
    },
    data: () => {
        return {
            role:""
        }
    }
}
</script>

<template>
    <div v-if="role == 'admin'">
        <p>This is the admin dashboard</p>
    </div>
    <div v-if="role == 'user'">
        <p>This is the user dashboard</p>
    </div>
    <div v-if="role == 'store_admin'">
        <p>This is the Store Admin dashboard</p>
    </div>
</template>