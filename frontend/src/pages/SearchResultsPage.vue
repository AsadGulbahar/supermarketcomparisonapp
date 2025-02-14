<!-- <template>
    <div class="search-results-container">
      <h1>Search Results</h1>
      <div v-if="products.length === 0">
        No products found.
      </div>
      <ul class="products-list">
        <li v-for="product in products" :key="product.id" class="product-item">
          <router-link :to="{ name: 'SingleProductPage', params: { id: product.groupProductId } }">
            <div class="product-content">
              <img :src="product.product_image_url" alt="Product Image" class="product-image">
              <div class="product-details">
                <h2>{{ product.product_name }}</h2>
                <p>Weight: {{ product.product_weight }}</p>
                <img :src="getSupermarketImage(product.supermarket_id)" alt="Supermarket" class="supermarket-image">
           
                <div class="price-info">
                  <p>RRP Price: {{ product.rrp_price }}</p>
                  <p v-if="product.sale_price">Sale Price: {{ product.sale_price }}</p>
                </div>
              </div>
            </div>
          </router-link>
        </li>
      </ul>
    </div>
</template> -->

<!-- <template>
  <div class="search-results-container">
    <h1>Search Results</h1>
    <div v-if="products.length === 0">
      No products found.
    </div>
    <ul class="products-list">
      <li v-for="product in products" :key="product.id" class="product-item">
     
        <router-link :to="{ name: 'SingleProductPage', params: { id: product.id } }">
          <div class="product-content">
      
            <img :src="`${process.env.VUE_APP_BACKEND_URL}${product.product_image_url}`" alt="Product Image" class="product-image">
            <div class="product-details">
              <h2>{{ product.product_name }}</h2>
              <p>Weight: {{ product.product_weight }}</p>
              
              <img :src="`${process.env.VUE_APP_BACKEND_URL}${product.supermarket.supermarket_image}`" alt="Supermarket" class="supermarket-image">
              
              <div class="price-info" v-if="product.prices.length > 0">
                <p>RRP Price: £{{ product.prices[0].rrp_price }}</p>
                <p v-if="product.prices[0].sale_price">Sale Price: £{{ product.prices[0].sale_price }}</p>
                <p v-if="product.prices[0].loyalty_card_price">Loyalty Card Price: £{{ product.prices[0].loyalty_card_price }}</p>
              </div>
            </div>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template> -->

<template>
  <div class="container">
    <div class="row">
      <div class="col-md-3 mb-4" v-for="product in products" :key="product.id">
        <div class="card shadow-sm hover-shadow">
          <img :src="product.product_image_url" :alt="product.product_name" class="card-img-top">
          <div class="card-body">
            <h5 class="card-title">{{ product.product_name }}</h5>
            <p class="card-text">
              Weight: {{ product.product_weight }}<br>
              <img :src="product.supermarket.supermarket_image" alt="Supermarket Logo" class="supermarket-image">
            </p>
            <router-link :to="{ name: 'SingleProductPage', params: { id: product.id } }" class="btn btn-primary">View Product</router-link>
            <!-- Basket Actions Component -->
            <ProductBasketActions :product="product" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>




<script>
  import axios from 'axios';
  import { ref, onMounted, watchEffect } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRoute } from 'vue-router';
  import ProductBasketActions from '@/pages/ProductBasketActions.vue';

  export default {
    components: {
      ProductBasketActions
    },
    setup() {
      const products = ref([]);
      const route = useRoute();

      const getSupermarketImage = (supermarketId) => {
        console.log("Image URL:", images[supermarketId]); // Check the URL
        return images[supermarketId];
      };


      onMounted(async () => {
        const query = route.query.query;
        const supermarketId = route.query.supermarket_id;
        console.log(`Fetching data with query: ${query} and supermarketId: ${supermarketId}`);
        // console log to inspect the products array before fetch
        console.log('Initial products array:', products.value);

        try {
          const { data } = await axios.get('/search-results/', {
            params: {
              query: query,
              supermarket_id: supermarketId,
            },
          });
          products.value = data;
          console.log('Data retrieved by frontend below')
          console.log(data)
          console.log('Data saved by frontend below')
          console.log(products.value)
        } catch (error) {
          console.error('Failed to fetch search results:', error);
        }
      });

        // console log within the setup to inspect individual products
        products.value.forEach(product => {
          console.log('Product in products array:', product);
        });

        watchEffect(() => {
          console.log('Products (using watchEffect) reactive update:', products.value);
        });

      return {
        products
      };
    },
  };
</script>
  
<style scoped>
.row {
  display: flex;
  flex-wrap: wrap;
}

.col-md-3 {
  display: flex;
  flex: 1 0 25%; /* Ensures the column takes up exactly 25% and flexes */
  margin-bottom: 16px; /* Keeps consistent spacing */
}

.card {
  display: flex;
  flex-direction: column; /* Stacks card content vertically */
  height: 100%; /* Ensures the card stretches to fill the column */
}

.card-body {
  flex: 1; /* Allows the card body to expand and fill available space */
  display: flex;
  flex-direction: column; /* Additional direction to keep structure */
  justify-content: space-between; /* Distributes space between content and footer */
}

.hover-shadow {
  transition: box-shadow 0.3s ease-in-out;
}

.hover-shadow:hover {
  box-shadow: 0 0 11px rgba(33,33,33,.2);
}

.card-img-top {
  width: 100%;
  height: auto; /* Adjust height automatically based on aspect ratio */
}

.btn {
  margin-top: auto; /* Pushes buttons to the bottom of the card */
}
.supermarket-image {
  width: 100px; /* Fixed width for consistency */
  height: auto; /* Maintain aspect ratio */
  margin-top: 10px; /* Spacing from text */
}
</style>
