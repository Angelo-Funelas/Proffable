<script setup>
    import {ref} from 'vue'
    const emit = defineEmits(['rate']);

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
        emit('rate', n);
    }
</script>

<template>
    <div class="min-w-auto text-[40px] text-white">
        <svg width="48" height="48" viewBox="0 0 48 48" v-for="n in 5" :key="n" class="inline fill-[#505946] h-[48px] cursor-pointer px-1" :class="{ 'fill-[#cbcb7c]': starRatingHover >= n && starRating < n, 'star-active': starRating >= n }" @mouseenter="handleMouseEnter(n)" @mouseleave="handleMouseLeave(n)" @click="setRating(n)">
            <path d="M24 4L30.18 16.52L44 18.54L34 28.28L36.36 42.04L24 35.54L11.64 42.04L14 28.28L4 18.54L17.82 16.52L24 4Z"/>
        </svg>
    </div>
</template>

<style>
.star-active {
    @apply fill-[#ffe51f];
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