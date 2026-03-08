import { defineStore } from 'pinia';

export const useFilterStore = defineStore('filter', {
  state: () => ({
    rating: 0,
    university: "",
  }),
  actions: {
    async updateRating(rating: number) {
      this.rating = rating;
    }
  }
});