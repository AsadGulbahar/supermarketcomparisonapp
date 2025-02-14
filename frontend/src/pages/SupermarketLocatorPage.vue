<!-- <template>
  <div>
    <input v-model="userInput" placeholder="Enter your address or click on 'Use My Location'"/>
    <button @click="searchSupermarkets">Search</button>
    <button @click="useCurrentLocation">Use My Location</button>
    <google-map
      :center="mapCenter"
      :zoom="15"
      style="width: 100%; height: 400px;"
    >
      <marker :position="mapCenter" />
    </google-map>
    <ul v-if="supermarkets.length">
      <li v-for="market in supermarkets" :key="market.name">
        <p>Name: {{ market.name }}</p>
        <p>Address: {{ market.address }}</p>
        <p>Opening Times: <ul><li v-for="time in market.opening_times">{{ time }}</li></ul></p>
        <p>Distance: {{ parseFloat(market.distance).toFixed(2) }} km</p>
      </li>
    </ul>
  </div>
</template> -->

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="input-group mb-4">
          <input 
            v-model="userInput" 
            type="text" 
            class="form-control" 
            placeholder="Enter your address or click on 'Use My Location'" 
          />
          <button 
            @click="searchSupermarkets" 
            class="btn btn-outline-primary"
          >
            Search
          </button>
          <button 
            @click="useCurrentLocation" 
            class="btn btn-outline-secondary"
          >
            Use My Location
          </button>
        </div>
        <div v-if="supermarkets.length" class="result-list">
          <ul class="list-group">
            <li 
              v-for="market in supermarkets" 
              :key="market.name" 
              class="list-group-item"
            >
              <h5 class="mb-1">{{ market.name }}</h5>
              <p class="mb-1">Address: {{ market.address }}</p>
              <p class="mb-1">
                Opening Times:
                <ul>
                  <li 
                    v-for="time in market.opening_times" 
                    :key="time"
                    class="opening-times"
                  >
                    {{ time }}
                  </li>
                </ul>
              </p>
              <p class="mb-1">
                Distance: {{ parseFloat(market.distance).toFixed(2) }} km
              </p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        userInput: '',
        supermarkets: [],
      };
    },
    methods: {
      searchSupermarkets() {
        axios.get(`/find-supermarkets?address=${this.userInput}`)
          .then(response => {
            this.supermarkets = response.data.supermarkets;
          })
          .catch(error => console.error('Error:', error));
      },
      useCurrentLocation() {
        navigator.geolocation.getCurrentPosition(position => {
          axios.get(`/find-supermarkets?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}`)
            .then(response => {
              this.supermarkets = response.data.supermarkets;
            })
            .catch(error => console.error('Error:', error));
        });
      }
    }
  }
  </script>  

<style scoped>
.result-list {
  max-height: 400px;
  overflow-y: auto; /* Allow scrolling if the list is long */
}

.list-group-item {
  background-color: #f7f7f7; /* Light background for list items */
  border: 1px solid #ddd; /* Borders for list items */
  border-radius: 0.25rem; /* Rounded corners for list items */
  margin-bottom: 0.5rem; /* Spacing between list items */
}

.opening-times {
  background-color: #fff; /* White background for nested list items */
  border: none; /* No borders for nested list items */
  padding-left: 20px; /* Indent nested list items */
}

</style>



<!-- 

<template>
    <div>
      <input v-model="userInput" placeholder="Enter your address or click on 'Use My Location'"/>
      <button @click="searchSupermarkets">Search</button>
      <button @click="useCurrentLocation">Use My Location</button>
      <ul v-if="supermarkets.length">
        <li v-for="market in supermarkets" :key="market.name">
          <p>Name: {{ market.name }}</p>
          <p>Address: {{ market.address }}</p>
          <p>Opening Times: <ul><li v-for="time in market.opening_times">{{ time }}</li></ul></p>
          <p>Distance: {{ market.distance.toFixed(2) }} km</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        userInput: '',
        supermarkets: [],
      };
    },
    methods: {
      searchSupermarkets() {
        axios.get(`/find-supermarkets?address=${this.userInput}`)
          .then(response => {
            this.supermarkets = response.data.supermarkets;
          })
          .catch(error => console.error('Error:', error));
      },
      useCurrentLocation() {
        navigator.geolocation.getCurrentPosition(position => {
          axios.get(`/find-supermarkets?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}`)
            .then(response => {
              this.supermarkets = response.data.supermarkets;
            })
            .catch(error => console.error('Error:', error));
        });
      }
    }
  }
  </script>   -->












<!-- <template>
    <div>
      <input v-model="address" placeholder="Enter your address"/>
      <button @click="searchSupermarkets">Search</button>
      <button @click="useCurrentLocation">Use My Location</button>
      <div id="map" style="height: 400px; width: 100%;"></div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        address: '',
        map: null,
        markers: [],
        AdvancedMarkerElement: null,  // Define this to store the AdvancedMarkerElement class
      };
    },
    methods: {
      async loadGoogleMaps() {
        console.log("Loading Google Maps Script");
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyBMiZe6R1m-wKSk4RKfZReTjDbEubJRN7w&callback=initMap&v=beta`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
        script.onload = async () => {
          console.log("Google Maps Script loaded successfully.");
        };
      },
      initMap() {
        this.map = new google.maps.Map(document.getElementById('map'), {
            center: { lat: 51.5227863381085, lng: -0.042924527167958644 },
            zoom: 8,
            mapId: '7480d37a9ed452a4'
        });
        this.placeMarkers();
      },
      placeMarkers() {
        this.markers.forEach(marker => {
          const markerInstance = new this.AdvancedMarkerElement({
            position: new google.maps.LatLng(marker.position.lat, marker.position.lng),
            map: this.map,
            title: marker.title,
          });
          markerInstance.setMap(this.map); // Adds the marker to the map
        });
      },
      searchSupermarkets() {
        const params = this.address ? { address: this.address } : {};
        axios.get('/find-supermarkets/', { params })
        .then(response => {
          this.markers.forEach(marker => marker.setMap(null));  // Clear existing markers
          this.markers = [];
          response.data.supermarkets.forEach(supermarket => {
            this.placeMarker({
              lat: supermarket.geometry.location.lat, 
              lng: supermarket.geometry.location.lng, 
              title: supermarket.name
            });
          });
        })
        .catch(error => console.error('Error:', error));
      },
      useCurrentLocation() {
        navigator.geolocation.getCurrentPosition(position => {
          const params = { latitude: position.coords.latitude, longitude: position.coords.longitude };
          axios.get('/find-supermarkets/', { params })
          .then(response => {
            this.markers.forEach(marker => marker.setMap(null));  // Clear existing markers
            this.markers = [];
            response.data.supermarkets.forEach(supermarket => {
              this.placeMarker({
                lat: supermarket.geometry.location.lat,
                lng: supermarket.geometry.location.lng,
                title: supermarket.name
              });
            });
          })
          .catch(error => console.error('Error:', error));
        });
      },
      placeMarker(info) {
        if (this.AdvancedMarkerElement) {
          const marker = new this.AdvancedMarkerElement({
            position: new google.maps.LatLng(info.lat, info.lng),
            map: this.map,
            title: info.title,
          });
          marker.setMap(this.map);  // Add the marker to the map
          this.markers.push(marker);
        } else {
          console.error("AdvancedMarkerElement is not defined yet.");
        }
      }
    },
    mounted() {
      this.loadGoogleMaps();
      window.initMap = this.initMap.bind(this);
    }
  }
  </script>
  
  <style scoped>
  /* Add your CSS styling here */
  </style>
   -->