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
<div class="prof-card">
    <h3>{{ fname }} {{ lname }}</h3>
    <p>{{ avgScore }} ({{ numReviews }}) Reviews</p>
    <p>Tags:</p>
    <ul>
        <li v-for="tag in tags" :key="id">
            {{ tag }}
        </li>
    </ul>
</div>
</template>