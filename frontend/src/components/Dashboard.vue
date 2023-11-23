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
    <p>This is the dashboard</p>
</template>