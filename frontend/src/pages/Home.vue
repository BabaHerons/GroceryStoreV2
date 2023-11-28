<script lang="ts">
import API from '../api';

export default {
    beforeMount() {
        API.verify_token()
        if (this.$route.path == "/"){
            this.$router.push({path:"/dashboard"})
        }
    }
}
</script>

<template>
    <NavbarVue />
    <RouterView />
</template>