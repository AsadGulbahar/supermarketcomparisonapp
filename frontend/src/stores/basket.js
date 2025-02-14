import { defineStore } from 'pinia';

export const useBasketStore = defineStore('basket', {
    state: () => ({
        items: [],  // Change to array
    }),
    actions: {
        addToBasket(product, quantity) {
            const existingProduct = this.items.find(p => p.id === product.id);  // Use find here correctly
            if (existingProduct) {
                existingProduct.quantity += quantity;
            } else {
                this.items.push({ ...product, quantity });  // Use push for arrays
            }
        },
        removeFromBasket(productId) {
            this.items = this.items.filter(p => p.id !== productId);  // Use filter to remove
        },
        updateQuantity(productId, quantity) {
            const product = this.items.find(p => p.id === productId);
            if (product) {
                product.quantity = quantity;
            }
        },
        getQuantity(productId) {
            const product = this.items.find(p => p.id === productId);
            return product ? product.quantity : 0;
        }
    }
});
