// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router';

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import SupermarketLocatorPage from '../pages/SupermarketLocatorPage.vue';

import BasketPage from '../pages/BasketPage.vue';
import BudgetPage from '../pages/BudgetPage.vue';
import CheckoutPriceComparisonPage from '../pages/CheckoutPriceComparisonPage.vue';
import EditUserProfilePage from '../pages/EditUserProfilePage.vue';
import GroceryListPage from '../pages/GroceryListPage.vue';
import GroceryListPriceTrackHistoryPage from '../pages/GroceryListPriceTrackHistoryPage.vue';

import MainProductsPage from '../pages/MainProductsPage.vue';

import OrderHistoryPage from '../pages/OrderHistoryPage.vue';
import SingleProductPage from '../pages/SingleProductPage.vue';
import SearchResultsPage from '../pages/SearchResultsPage.vue';

import App from '../App.vue'

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/supermarketLocator/', name: 'Supermarket Locator Page', component: SupermarketLocatorPage },

        { path: '/basket/', name: 'Basket Page', component: BasketPage },
        { path: '/budget/', name: 'Budget Page', component: BudgetPage },
        { path: '/checkout/', name: 'Checkout Price Comparison Page', component: CheckoutPriceComparisonPage },
        { path: '/profile/', name: 'Edit User Profile Page', component: EditUserProfilePage },
        { path: '/groceryList/', name: 'Grocery List Page', component: GroceryListPage },
        { path: '/groceryPriceTrackHistory/', name: 'Grocery List Price Track History Page', component: GroceryListPriceTrackHistoryPage },
        { path: '/mainProducts/', name: 'Main Products Page', component: MainProductsPage },
        { path: '/orderHistory/', name: 'Order History Page', component: OrderHistoryPage },           
        { path: '/search-results/', name: 'Search Results Page', component: SearchResultsPage, props: true },
        { path: '/product-details/:id', name: 'SingleProductPage', component: SingleProductPage, props: true},
        { path: '/app',  name: 'App', component: App}, 
    ]
})

export default router
