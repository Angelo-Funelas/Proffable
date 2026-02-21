<script setup>
import {ref, computed, onMounted} from 'vue'
import axios from 'axios'

const professors = ref([])
onMounted(()=>{
    fetchProfessors()
})

const API_URL = 'http://localhost:8000/api/'
const api = axios.create({
    baseURL:API_URL
})

async function fetchProfessors(){
    isLoading.value = true
    try{
        const response = await api.get('professors/')
        professors.value = response.data
    } catch(error){
        console.log("Error with fetching professors: ",error)
    }
    isLoading.value = false
}
const isLoading = ref(false)

import ProfCard from './ProfCard.vue'
</script>

<template>
<h1 class="text-5xl font-bold text-left">Professors</h1>
<p v-if="isLoading">Loading professors...</p>

<ul>
    <li v-for="prof in professors" :key="prof.professor_id">
        <ProfCard
        :lname="prof.l_name"
        :fname="prof.f_name"
        :avgScore="3"
        :numReviews="128"
        />
    </li>
</ul>
</template>

const props = defineProps({
    lname: String,
    fname: String,
    avgScore: String,
    tags: Array,
    numReviews: String,
})