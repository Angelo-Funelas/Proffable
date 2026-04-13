<script setup>
import {ref} from 'vue'
const props = defineProps({
    lname: String,
    fname: String,
    avgScore: Number,
    tags: Array,
    numReviews: Number,
    favoriteCount: Number,
    is_favorited: Boolean,
    institutions: Array,
})

</script>

<template>
<div class="bg-[#719294] rounded-xl p-[18px] flex justify-between items-start">

    <div class="flex flex-col text-left">
        <h3 class="text-xl font-bold">{{ fname }} {{ lname }}</h3>
        <p class="text-sm">{{ institutions?.map(i => i.name).join(', ') || 'Unknown Institution' }}</p>
        <p class="text-sm flex items-center gap-[2px]"><img src="../assets/Star.svg" class="h-[16px]"> {{ avgScore }} ({{ numReviews }} reviews)</p>
        <div class="text-sm flex flex-wrap gap-1 items-center">
            <span>Tags:</span>
            <span v-for="tag in tags" :key="tag" class='bg-gray-200 text-[#719294] px-2 py-1 rounded-full'>
                {{ tag }}
            </span>
        </div>

    </div>

    <div class="flex flex-col items-center gap-1">
        <img v-if="is_favorited" src="../assets/FilledHeart.svg" class="size-[16px]">
        <img v-else src="../assets/Heart.svg" class="size-[16px]">
        <span class="text-sm">{{ favoriteCount }}</span>
    </div>

</div>
</template>