<template>
  <div class="profile-page d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow" :class="{ 'animate-change': isEditing }">
      <h3 class="text-center">{{ title }}</h3>
      <div v-if="!isEditing">
        <img :src="userProfile.profile_image" alt="Profile Image" class="profile-image mx-auto d-block mb-3" />
        <p><strong>Username:</strong> {{ userProfile.username }}</p>
        <p><strong>Email:</strong> {{ userProfile.email }}</p>
        <p><strong>First Name:</strong> {{ userProfile.first_name }}</p>
        <p><strong>Last Name:</strong> {{ userProfile.last_name }}</p>
        <p><strong>Address:</strong> {{ userProfile.address }}</p>
        <button @click="editProfile" class="btn btn-primary w-100">Edit Profile</button>
      </div>
      <form v-else @submit.prevent="updateProfile">
        <div class="mb-3">
          <label for="username" class="form-label">Username:</label>
          <input id="username" v-model="userProfile.username" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input id="email" v-model="userProfile.email" type="email" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="firstName" class="form-label">First Name:</label>
          <input id="firstName" v-model="userProfile.first_name" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="lastName" class="form-label">Last Name:</label>
          <input id="lastName" v-model="userProfile.last_name" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="address" class="form-label">Address:</label>
          <input id="address" v-model="userProfile.address" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">New Password (leave blank to keep current):</label>
          <input id="newPassword" v-model="newPassword" type="password" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Confirm New Password:</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="profileImage" class="form-label">Profile Image:</label>
          <input id="profileImage" type="file" @change="handleFileUpload" class="form-control" />
        </div>
        <button type="submit" class="btn btn-success w-100 mb-2">Save Changes</button>
        <button @click="cancelEdit" class="btn btn-secondary w-100">Cancel</button>
      </form>
    </div>
  </div>
</template>

  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {        
        title: "User Profile",
        userProfile: {
          username: '',
          email: '',
          first_name: '',
          last_name: '',
          profile_image: '',
          address: '',
        },
        newPassword: '',
        confirmPassword: '',
        isEditing: false,
        selectedFile: null,
      };
    },
    methods: {
      fetchUserProfile() {
        axios.get('/profile/').then(response => {
          this.userProfile = response.data;
        });
      },
      updateProfile() {
        const formData = new FormData();
        formData.append('username', this.userProfile.username);
        formData.append('email', this.userProfile.email);
        formData.append('first_name', this.userProfile.first_name);
        formData.append('last_name', this.userProfile.last_name);
        formData.append('address', this.userProfile.address);
        if (this.newPassword && this.newPassword === this.confirmPassword) {
          formData.append('password', this.newPassword);
        }
        if (this.selectedFile) {
          formData.append('profile_image', this.selectedFile, this.selectedFile.name);
        }
  
        axios.put('/profile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }).then(() => {
          this.isEditing = false;
          alert('Profile updated successfully.');
          this.fetchUserProfile(); // Refresh profile data
        }).catch(error => {
          console.error('Error updating profile:', error.response.data);
        });
      },
      editProfile() {
        this.isEditing = true;
      },
      cancelEdit() {
        this.isEditing = false;
      },
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
    },
    mounted() {
      this.fetchUserProfile();
    },
  };
</script>
  
<style scoped>
.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: block;
  margin-bottom: 10px;
}
.animate-change {
  transition: transform 0.3s ease-in-out;
}
.animate-change:hover {
  transform: scale(1.03);
}
.card {
  max-width: 500px; /* Adjust size as needed */
}
.vh-100 {
  height: 100vh; /* Makes div full height of the viewport */
}
</style>






<!-- <template>1111111111111111111111111111111111111111111111
    <div class="profile-page">
      <h3>{{ title }}</h3>
      <div v-if="!isEditing">
        <img :src="userProfile.profile_image" alt="Profile Image" class="profile-image"/>
        <p>Username: {{ userProfile.username }}</p>
        <p>Email: {{ userProfile.email }}</p>
        <p>First Name: {{ userProfile.first_name }}</p>
        <p>Last Name: {{ userProfile.last_name }}</p>
        <p>Address: {{ userProfile.address }}</p>
        <button @click="editProfile">Edit Profile</button>
      </div>
      <form v-else @submit.prevent="updateProfile">
        <div>
          <label>Username:</label>
          <input v-model="userProfile.username" type="text" />
        </div>
        <div>
          <label>First Name:</label>
          <input v-model="userProfile.first_name" type="text" />
        </div>
        <div>
          <label>Last Name:</label>
          <input v-model="userProfile.last_name" type="text" />
        </div>
        <div>
          <label>Address:</label>
          <input v-model="userProfile.address" type="text" />
        </div>
        <div>
          <label>New Password (leave blank to keep current):</label>
          <input v-model="newPassword" type="password" />
        </div>
        <div>
          <label>Confirm New Password:</label>
          <input v-model="confirmPassword" type="password" />
        </div>
        <div>
          <label>Profile Image:</label>
          <input type="file" @change="handleFileUpload" />
        </div>
        <button type="submit">Save Changes</button>
        <button @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        title: "User Profile",
        userProfile: {
          username: '',
          email: '',
          first_name: '',
          last_name: '',
          profile_image: '',
          address: '',
        },
        newPassword: '',
        confirmPassword: '',
        isEditing: false,
        selectedFile: null,
      };
    },
    methods: {
      fetchUserProfile() {
        axios.get('/profile/').then(response => {
          this.userProfile = response.data;
        });
      },
      updateProfile() {
        const formData = new FormData();
        formData.append('username', this.userProfile.username);
        formData.append('first_name', this.userProfile.first_name);
        formData.append('last_name', this.userProfile.last_name);
        formData.append('address', this.userProfile.address);
        if (this.newPassword === this.confirmPassword && this.newPassword) {
          formData.append('password', this.newPassword);
        }
        if (this.selectedFile) {
          formData.append('profile_image', this.selectedFile);
        }
  
        axios.put('/profile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }).then(() => {
          this.isEditing = false;
          alert('Profile updated successfully.');
          this.fetchUserProfile();
        }).catch(error => {
          console.error('Error updating profile:', error.response.data);
        });
      },
      editProfile() {
        this.isEditing = true;
      },
      cancelEdit() {
        this.isEditing = false;
      },
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
    },
    mounted() {
      this.fetchUserProfile();
    },
  };
  </script>
  
  <style scoped>
  .profile-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
  }
  </style>
   -->