<template>
  <div class="custom-dropdown d-flex align-items-center">
    <!-- Dropdown selection on the left -->
    <div class="dropdown-selection mr-2" @click="toggleDropdown">
      <img v-if="selectedSupermarketImage" :src="selectedSupermarketImage" class="supermarket-image img-fluid" />
      <span v-if="!selectedSupermarketId" class="whitefont">Select a Supermarket</span>
      <span v-else class="whitefont">Selected Supermarket</span>
    </div>

    <!-- Dropdown menu -->
    <div v-if="showDropdown" class="dropdown-menu show">
      <div class="dropdown-item" @click="selectSupermarket(null)">
        <span>All Supermarkets</span>
      </div>
      <div class="dropdown-item" v-for="(image, id) in images" :key="id" @click="selectSupermarket(id)">
        <img :src="image" class="supermarket-image img-fluid" />
      </div>
    </div>

    <!-- Search input in the middle -->
    <input type="text" v-model="searchQuery" class="form-control flex-grow-1 mx-2" placeholder="Search for products..." />

    <!-- Search button on the right -->
    <button @click="performSearch" class="btn btn-primary">Search</button>
  </div>
</template>


<script>
import { ref, computed } from 'vue';
import { useRouter } from "vue-router";
import { useSupermarketStore, useSupermarketImagesStore } from '@/stores/supermarket';

export default {
  setup() {
    const supermarketStore = useSupermarketStore();
    const { images } = useSupermarketImagesStore();
    const searchQuery = ref('');
    const showDropdown = ref(false);

    const selectedSupermarketId = computed({
      get: () => supermarketStore.selectedSupermarketId,
      set: (value) => { supermarketStore.selectedSupermarketId = value; }
    });

    const selectedSupermarketImage = computed(() => {
      return images[selectedSupermarketId.value];
    });

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
    };

    const selectSupermarket = (id) => {
      selectedSupermarketId.value = id;
      toggleDropdown();
    };

    const router = useRouter(); // Use useRouter to programmatically navigate
    
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
          alert("Please enter a search term.");
          return;
      }

      // Navigate to the search results page with query parameters
      router.push({
          name: 'Search Results Page',
          query: {
          query: searchQuery.value,
          supermarket_id: selectedSupermarketId.value || undefined,
          }
      });
    };

    return {
      searchQuery,
      showDropdown,
      toggleDropdown,
      selectSupermarket,
      performSearch,
      selectedSupermarketId,
      selectedSupermarketImage,
      images,
    };
  },
};
</script>

<style scoped>
.custom-dropdown {
  position: relative;
  display: flex; /* Ensures flex layout */
  align-items: center; /* Centers items vertically */
  width: 100%; /* Full width to span the parent container */
}

.dropdown-selection {
  cursor: pointer;
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  align-items: center;
}

.supermarket-image {
  width: 30px; /* Size of the supermarket image */
  margin-right: 10px; /* Spacing to the right of the image */
}

.dropdown-menu {
  position: absolute;
  top: 100%; /* Positions the dropdown directly below the toggle element */
  left: 0;
  background-color: #f9f9f9;
  width: auto; /* Adjust width to fit content */
  max-width: 250px; /* Max width to limit the dropdown size */
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1050; /* Ensure the dropdown is above most content but below fixed elements like navbars */
  overflow: hidden; /* Hides any overflow, useful for smaller screens */
}

.dropdown-item {
  white-space: nowrap; /* Ensures the text does not wrap */
  padding: 12px 16px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f1f1f1;
}

.form-control {
  flex-grow: 1; /* Allows the search input to grow and fill the space */
}

.btn-primary {
  margin-left: 2px; /* Spacing between button and input */
}

@media (max-width: 576px) {
  .custom-dropdown {
    flex-direction: column; /* Stacks elements vertically on smaller screens */
  }
  .form-control, .btn-primary {
    width: 100%; /* Full width for smaller screens */
    margin-top: 10px; /* Spacing after dropdown */
  }
  .dropdown-menu {
    width: 100%; /* Full width on smaller screens */
  }
  .whitefont{
    font: white;
  }
}
</style>
