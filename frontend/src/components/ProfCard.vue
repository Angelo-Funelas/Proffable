<script setup>
import Heart from './Heart.vue';
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
<div class="bg-card shadow-md rounded-xl p-[18px] flex justify-between items-start">

    <div class="flex flex-col text-left text-text-main">
        <h3 class="text-xl font-bold">{{ fname }} {{ lname }}</h3>
        <p class="text-sm text-text-muted">{{ institutions?.map(i => i.name).join(', ') || 'Unknown Institution' }}</p>
        <p class="text-sm flex items-center gap-[2px] text-text-muted"><img src="../assets/Star.svg" class="h-[16px]"> {{ avgScore }} ({{ numReviews }} reviews)</p>
        <div class="text-sm text-text-muted flex flex-wrap gap-1 items-center">
            <span>Tags:</span>
            <span v-for="tag in tags" :key="tag" class='bg-gray-200 text-[#719294] px-2 py-1 rounded-full'>
                {{ tag }}
            </span>
        </div>

    </div>

    <Heart :filled="is_favorited" :favorite_count="favoriteCount"/>
</div>
</template>