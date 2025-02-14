// stores/supermarket.js
import tescoLogo from '@/assets/supermarkets/Tesco-logo.png';
import sainsburysLogo from '@/assets/supermarkets/Sainsburys-logo.png';
import asdaLogo from '@/assets/supermarkets/Asda-logo.png';
import morrisonsLogo from '@/assets/supermarkets/Morrisons-logo.png';

import { defineStore } from 'pinia';

export const useSupermarketStore = defineStore('supermarket', {
  state: () => ({
    selectedSupermarketId: null,
  }),
});

export const useSupermarketImagesStore = defineStore('supermarketImages', {
  state: () => ({
    images: {
      1: tescoLogo,
      2: sainsburysLogo,
      3: asdaLogo,
      4: morrisonsLogo,
    }
  }),
});