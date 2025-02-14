<template>
    <div class="basket-contents">
      <h2>Your Basket</h2>
      <ul>
        <li v-for="(item, id) in basketItems" :key="id" class="basket-item">
          <img :src="item.product_image_url" alt="Product Image" class="product-image">
          <div class="product-details">
            <h3>{{ item.product_name }}</h3>
            <p class="price">{{ displayPrice(item) }}</p>
            <product-basket-actions :product-id="id" />
          </div>
        </li>
      </ul>
      <p>Total: {{ totalCost | currency }}</p>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useBasketStore } from '@/stores/basket';
  import ProductBasketActions from '@/pages/ProductBasketActions.vue';
  

  export default {
    components: {
      ProductBasketActions
    },
    setup() {
      const basket = useBasketStore();
      const basketItems = computed(() => basket.items);
      const totalCost = computed(() => {
        return Object.values(basket.items).reduce((acc, item) => acc + item.quantity * (item.sale_price || item.rrp_price), 0);
      });
  
      const displayPrice = (item) => {
        if (item.sale_price) return `£${item.sale_price.toFixed(2)} (Sale)`;
        if (item.promo_price) return `£${item.promo_price.toFixed(2)} (Promo)`;
        return `£${item.rrp_price.toFixed(2)}`;
      };
  
      return { basketItems, totalCost, displayPrice };
    },
    filters: {
      currency(value) {
        return `£${value.toFixed(2)}`;
      }
    }
  };
  </script>
  
  <style scoped>
  .basket-contents ul {
    list-style: none;
    padding: 0;
  }
  .basket-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  .product-image {
    width: 50px;
    height: 50px;
    margin-right: 15px;
  }
  .product-details h3 {
    margin: 0;
    font-size: 16px;
  }
  .price {
    font-weight: bold;
    color: #666;
  }
  </style>
  