<template>
    <div class="h3">
      {{ title }}
    </div>
  </template>
  
  <script>
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Budget Page",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
  