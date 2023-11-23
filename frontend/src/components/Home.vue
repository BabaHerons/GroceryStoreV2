<script lang="ts">

export default {
    beforeMount() {
        if (this.$route.path == "/"){
            this.$router.push({path:"/dashboard"})
        }
    }
}
</script>

<template>
    <nav class="container">
        This is the Navigation bar
    </nav>
    <RouterView />
</template>