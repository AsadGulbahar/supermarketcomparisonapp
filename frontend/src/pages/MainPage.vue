<template>
  <div class="h1">
    {{ title }}
  </div>
</template>

<script>
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Main Page",
            }
        }
    })
</script>

<style scoped>
</style>
