<script setup>
import {ref} from 'vue'
const props = defineProps({
    lname: String,
    fname: String,
    avgScore: Number,
    tags: Array,
    numReviews: Number,
})
</script>

<template>
<div class="bg-[#719294] rounded-xl p-[18px] flex justify-between items-start w-full">

    <div class="flex flex-col gap-2 text-left">
        <h3 class="text-xl font-bold">{{ fname }} {{ lname }}</h3>
        <p class="text-sm">University of Unknown </p>
        <p class="text-sm">⭐ {{ avgScore }} ({{ numReviews }} reviews)</p>
        <p class="text-sm">Tags:</p>

    </div>

    <div class="flex flex-col items-center gap-1">
        <span>🤍</span>
        <span class="text-sm">{{ numReviews }}</span>
    </div>

</div>
</template>