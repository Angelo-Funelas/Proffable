<script setup>
import {ref, computed, onMounted} from 'vue'
// Current Docker setup lacks CORS HEADER. 
// Uses temporary professors json list for now.
// The following code should be used instead (note that it is temporarily 
// written with Fetch, must be updated to use Axios later when installed)
//
// const professors = ref([])
// onMounted(()=>{
//     fetchProfessors()
// })
//
// const API_URL = 'http://localhost:8000/api/professors/'
// async function fetchProfessors(){
//     isLoading.value = true
//     try{
//         const response = await fetch(API_URL)
//         professors.value = await response.json()
//     } catch(error){
//         console.log("Error with fetching professors: ",error)
//     }
//     isLoading.value = false
// }
const isLoading = ref(false)
const professors = [{
    f_name: "Jane",
    l_name: "Doe",
    m_name: "Rat",
    email: "2jane4doe@gmail.com"
}]
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