<template>
    <main>
        <!-- Bootstrap navbar with custom color and integrated search bar -->
        <b-navbar toggleable="lg" class="bg-navy w-100">
            <b-navbar-brand :to="{name: 'Main Page'}" class="text-white">Supermarket Comparison App</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav class="me-auto">
                    <b-nav-item :to="{name: 'Supermarket Locator Page'}" class="text-white">Supermarket Locator</b-nav-item>
                    <b-nav-item :to="{name: 'Edit User Profile Page'}" class="text-white">Edit User Profile Page</b-nav-item>
                </b-navbar-nav>
                <!-- Search Bar Component -->
                <SearchBar />
                <!-- Logout Button as Nav Item -->
                <b-navbar-nav class="ms-auto">
                    <b-nav-item @click="logout" class="text-danger">Logout</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>

        <RouterView class="flex-shrink-0" />
    </main>
</template>



<script>
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import SearchBar from "@/pages/SearchBar.vue";
import axios from "@/axios-config.js";

export default defineComponent({
    components: { 
        RouterView,
        SearchBar,
    },
    
    setup() {
        const logout = async () => {
            try {
                console.log('About to send logout')            
                await axios.post('/logout/');         
                console.log('Logged out')
                window.location.href = 'http://127.0.0.1:8000/';
            } catch (error) {
                console.error('Logout failed:', error);
            }
        };

        return {
            logout,
        };
    },
});
</script>

<style scoped>
.bg-navy {
    background-color: #000080; /* Navy color */
    width: 100%; /* Ensures the navbar stretches across the width */
}

/* Increased specificity for navbar links */
.b-navbar-nav .b-nav-item .nav-link, 
.b-navbar-brand {
    color: #fff !important; /* Force white color */
    transition: color 0.3s ease; /* Smooth transition for color */
}

/* Style for navbar brand and items to change on hover */
.b-navbar-nav .b-nav-item .nav-link:hover, 
.b-navbar-brand:hover {
    color:white; /* Lightens the color on hover for a subtle effect */
    
}

/* Adjusting navbar brand spacing */
.b-navbar-brand {
    margin-left: 1rem; /* Adds space to the left of the navbar brand */
}

/* This ensures that any text inside the navbar navigation is white */
.b-navbar-nav {
    color: #fff !important;
}

/* Specificity for direct children only */
.b-navbar-nav > .nav-item > .nav-link {
    color: #fff !important;
}

</style>
