<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <div class="product-details">
          <h1 class="fw-bold">{{ groupProductData.common_product_name || 'Product Details' }}</h1>
          <h2>{{ selectedProduct.product_name }}</h2>
          <p>Weight: {{ selectedProduct.product_weight }}</p>
        </div>
        <img :src="selectedProduct.product_image_url" alt="Product Image" class="product-image img-fluid">
      </div>
      
      <div class="col-md-6">
        <table class="table table-hover styled-table">
          <thead>
            <tr>
              <th>Supermarket</th>
              <th>Link</th>
              <th>RRP</th>
              <th>Sale Price</th>
              <th>Loyalty Card Price</th>
              <th>Price per Weight</th>
              <th>Promo</th>
              <th>Loyalty Card Deal</th>
              <th>Date/Time Updated</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in groupProductData.products" :key="product.id" @click="selectProduct(product)">
              <td><img :src="product.supermarket.supermarket_image" alt="Supermarket Logo" class="supermarket-image"></td>
              <td><a :href="product.product_url" target="_blank">Link</a></td>
              <td :class="{ 'text-decoration-line-through': product.latest_price && (product.latest_price.sale_price || product.latest_price.loyalty_card_price) }">{{ product.latest_price ? `£${product.latest_price.rrp_price}` : 'N/A' }}</td>
              <td>{{ product.latest_price && product.latest_price.sale_price ? `£${product.latest_price.sale_price}` : 'N/A' }}</td>
              <td>{{ product.latest_price && product.latest_price.loyalty_card_price ? `£${product.latest_price.loyalty_card_price}` : 'N/A' }}</td>
              <td>{{ product.latest_price ? product.latest_price.rrp_price_per_weight : 'N/A' }}</td>
              <td>{{ product.latest_price ? product.latest_price.sale_deal : 'N/A' }}</td>
              <td>{{ product.latest_price ? product.latest_price.loyalty_card_deal : 'N/A' }}</td>
              <td>{{ product.latest_price ? new Date(product.latest_price.datetime_price_updated).toLocaleString() : 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <!-- Basket Actions Component -->
  <ProductBasketActions :product="product" />

  <!-- Price History Chart centered under both columns -->
  <div class="row">
    <div class="col-12 d-flex justify-content-center">
      <img v-if="groupProductData.id" :src="`/price-history/${groupProductData.id}/`" alt="Price History Chart" class="price-history-chart img-fluid">
    </div>
  </div>
</template>




<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useSupermarketImagesStore } from '@/stores/supermarket';
import ProductBasketActions from '@/pages/ProductBasketActions.vue';
// import ProductPriceHistoryGraph from '@/pages/ProductPriceHistoryGraph.vue';

export default {
  components: { ProductBasketActions },
  setup() {
    const route = useRoute();
    const showModal = ref(false);
    const creatingList = ref(false);
    const shoppingLists = ref([]);
    const selectedList = ref(null);
    const newListName = ref('');
    const groupProductData = ref({});
    const selectedProduct = ref({});


    const fetchGroupProductData = async () => {
      try {
        const response = await axios.get(`/product-details/${route.params.id}`);
        groupProductData.value = response.data;
        console.log('groupProductData', response.data)
        selectedProduct.value = response.data.products[0] || {};
      } catch (error) {
        console.error('Error fetching group product details:', error);
      }
    };

    const selectProduct = (product) => {
      selectedProduct.value = product;  // Set the selected product
    };

    // const fetchLists = async () => {
    //   try {
    //     const response = await axios.get('/lists/');
    //     shoppingLists.value = response.data.map(list => ({ value: list.id, text: list.name }));
    //   } catch (error) {
    //     console.error('Error fetching lists:', error);
    //   }
    // };

    // const addToSelectedList = async () => {
    //   if (!selectedList.value) return;
    //   await axios.post('/add-to-list/', { listId: selectedList.value, productId: selectedProduct.value.id });
    //   showModal.value = false;
    // };

    // const createNewList = () => {
    //   creatingList.value = true;
    // };

    // const finalizeListCreation = async () => {
    //   if (!newListName.value) return;
    //   const response = await axios.post('/create-list/', { name: newListName.value });
    //   shoppingLists.value.push({ value: response.data.id, text: response.data.name });
    //   selectedList.value = response.data.id;
    //   creatingList.value = false;
    //   addToSelectedList();
    // };

    onMounted(() => {
      fetchGroupProductData();
      // fetchLists();
    });

    return {
      groupProductData, selectedProduct, showModal, shoppingLists, selectedList, newListName, creatingList   
    };
  }
};
</script>

<style scoped>
.product-details {
  text-align: left; /* Aligns the product details text to the left */
}

.product-image {
  width: 70%; /* Reduces the image width to 70% */
  display: block; /* Ensures the image is block level */
  margin: 20px auto; /* Centers the image horizontally and adds vertical space */
}

.styled-table thead th {
  background-color: #004085; /* Dark blue background for the table header */
  color: #ffffff; /* White text color */
}

.table-hover thead th {
  background-color: #6c757d; /* Bootstrap dark theme for headers */
}

.col-md-6 {
  display: flex;
  flex-direction: column; /* Keeps content aligned in a column */
  align-items: center; /* Center-aligns the children */
}
.price-history-chart {
  max-width: 100%; /* Ensures the image is responsive and scales correctly */
  height: auto; /* Maintains the aspect ratio */
}

.styled-table {
  margin-top: 100px; /* Adds margin above the table */
  border-collapse: collapse; /* for better border handling */
  width: 100%; /* Ensures the table uses the full width of its container */
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Adds a subtle shadow to the table */
  border-radius: 0.25rem; /* Slight rounding of corners for aesthetic */
}

@media (max-width: 768px) {
  .product-image, .styled-table {
    width: 100%; /* Full width for smaller devices */
  }
}
.supermarket-image {
  height: 40px; /* Reduced height for logos */
  width: auto; /* Width is automatically adjusted to maintain aspect ratio */
  margin-top: 5px; /* Reduced spacing from text */
}
</style>
