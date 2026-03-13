<script setup>
    import {ref} from 'vue'
    const emit = defineEmits(['rate']);
    const props = defineProps({initialRating:{default:0}})

    const starRatingHover = ref(0);
    const starRating = ref(props.initialRating);

    const handleMouseEnter = (n) => {
        starRatingHover.value = n;
    };
    const handleMouseLeave = (n) => {
        starRatingHover.value = 0;
    }

    const setRating = (n) => {
        if (starRating.value > 0 && starRating.value == n) return clearRating();
        starRating.value = n;;
        emit('rate', n);
    }

    const clearRating = () => {
        starRating.value = 0;
        emit('rate', 0);
    }
</script>

<template>
    <div>
        <svg width="40" height="38" viewBox="0 0 40 38"
        v-for="n in 5"
        :key="n"
        class=" drop-shadow-[1px_2px_2px_rgba(0,0,0,.4)] inline fill-[#505946] cursor-pointer px-1 mx-0.5"
        :class="{ 
            'fill-[#cbcb7c]': starRatingHover >= n && starRating < n,
            'star-active': starRating >= n
        }"
        @mouseenter="handleMouseEnter(n)"
        @mouseleave="handleMouseLeave(n)"
        @click="setRating(n)">
            <path class="cls-1" d="M20,0l6.2,12.5,13.8,2-10,9.7,2.4,13.8-12.4-6.5-12.4,6.5,2.4-13.8L0,14.5l13.8-2L20,0Z"/>
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