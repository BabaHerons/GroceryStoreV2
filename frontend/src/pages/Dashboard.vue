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
        <AdminDashVue />
    </div>
    <div v-if="role == 'user'">
        <UserDashVue />
    </div>
    <div v-if="role == 'store_admin'">
        <SMDashVue />
    </div>
</template>