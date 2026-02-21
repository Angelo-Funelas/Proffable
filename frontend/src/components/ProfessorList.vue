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
</script>

<template>
<h2>Professors</h2>
<p v-if="isLoading">Loading professors...</p>

<ul>
    <li v-for="prof in professors" :key="prof.professor_id">
        <p>Name: {{prof.f_name}}, {{ prof.l_name }}</p> 
        <p>Email: {{ prof.email }}</p>
    </li>
</ul>
</template>