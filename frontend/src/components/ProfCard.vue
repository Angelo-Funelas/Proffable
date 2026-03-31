<script setup>
import {ref} from 'vue'
const props = defineProps({
    lname: String,
    fname: String,
    avgScore: Number,
    tags: Array,
    numReviews: Number,
    favoriteCount: Number,
})
</script>

<template>
<div class="bg-[#719294] rounded-xl p-[18px] flex justify-between items-start">

    <div class="flex flex-col text-left">
        <h3 class="text-xl font-bold">{{ fname }} {{ lname }}</h3>
        <p class="text-sm">University of Unknown </p>
        <p class="text-sm flex items-center gap-[2px]"><img src="../assets/Star.svg" class="h-[16px]"> {{ avgScore }} ({{ numReviews }} reviews)</p>
        <p class="text-sm">Tags:</p>

    </div>

    <div class="flex flex-col items-center gap-1">
        <img src="../assets/Heart.svg" class="h-[16px]">
        <span class="text-sm">{{ favoriteCount }}</span>
    </div>

</div>
</template>