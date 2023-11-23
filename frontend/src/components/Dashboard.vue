<script lang="ts">
import API from "../api.ts";

export default {
    beforeMount() {
        API.verify_token()
    },
}
</script>

<template>
    <p>Hello</p>
</template>