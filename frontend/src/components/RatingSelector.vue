<script setup>
    import {ref} from 'vue'
    const starRatingHover = ref(5);
    const starRating = ref(0);

    const handleMouseEnter = (n) => {
        starRatingHover.value = n;
    };
    const handleMouseLeave = (n) => {
        starRatingHover.value = 0;
    }
    const setRating = (n) => {
        starRating.value = n;
    }
</script>

<template>
    <div class="flex justify-center text-[40px] text-white mb-[10px]">
        <span v-for="n in 5" :key="n" class="cursor-pointer px-1" :class="{ 'text-[#cbcb7c]': starRatingHover >= n && starRating < n, 'star-active': starRating >= n }" @mouseenter="handleMouseEnter(n)" @mouseleave="handleMouseLeave(n)" @click="setRating(n)">
            ★
        </span>
    </div>

    <p class="text-center text-white opacity-80 -mt-[20px]">
        Average Rating
    </p>
</template>

<style>
.star-active {
    @apply text-[#ffe51f];
    animation: pulse .2s cubic-bezier(.02,1.68,.95,.99);
}
@keyframes pulse {
    0% {
        scale: 1;
    }
    50% {
        scale: 1.2;
    }
    100% {
        scale: 1;
    }
}
</style>