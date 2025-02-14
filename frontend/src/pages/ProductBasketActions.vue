<template>
  <div class="basket-controls">
    <button v-if="quantity > 1" @click="decreaseQuantity" class="btn btn-success">-</button>
    <button v-else-if="quantity === 1" @click="removeProduct" class="btn btn-danger">x</button>
    <input type="number" v-model="quantity" min="1" class="form-control">
    <button v-if="productAdded" @click="increaseQuantity" class="btn btn-success">+</button>
    <button v-if="quantity === 0" @click="addProduct" class="btn btn-success">Add</button>
  </div>
</template>

<script>
  import { defineComponent, computed, ref } from 'vue';
  import { useBasketStore } from '@/stores/basket';

  export default defineComponent({
    props: {
      product: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const basketStore = useBasketStore();
      const productAdded = ref(false);  // State to track if product has been added

      const quantity = computed({
        get: () => basketStore.getQuantity(props.product.id),
        set: newVal => basketStore.updateQuantity(props.product.id, newVal)
      });

      const addProduct = () => {
        basketStore.addToBasket(props.product, 1);
        productAdded.value = true;  // Set productAdded to true when product is added
      };
      const increaseQuantity = () => quantity.value++;
      const decreaseQuantity = () => quantity.value--;
      const removeProduct = () => {
        basketStore.removeFromBasket(props.product.id);
        productAdded.value = false;  // Reset when product is removed
      };

      return { quantity, addProduct, increaseQuantity, decreaseQuantity, removeProduct, productAdded };
    }
  });
</script>

<style scoped>
  .basket-controls input {
    width: 50px;
    text-align: center;
    display: inline-block;
  }
  .basket-controls button {
    margin: 0 5px;
  }
</style>
