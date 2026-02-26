<script setup>
import {ref, computed, onMounted} from 'vue'
import axios from 'axios'
import ProfCard from './ProfCard.vue'
import SearchFilters from './SearchFilters.vue'
import { useRouter } from 'vue-router'
import Navbar from './Navbar.vue'

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

const router = useRouter()
const goToProf = (professorId) =>{
    router.push(`/professor/${professorId}`)
}

</script>

<template>

<div class="min-h-screen bg-[#e8e8e8] flex flex-col">
    
    <Navbar/>

    <div class="grid grid-cols-[4fr_11fr] gap-x-[30px] w-screen p-[64px]"> 
        <!--LEFT DIV-->
        <SearchFilters/>

        <!--RIGHT DIV-->
        <div>
            <h1 class="text-5xl font-bold text-left mb-[10px]">Professors</h1>
        <p v-if="isLoading">Loading professors...</p>

        <ul class="grid grid-cols-1 gap-y-[10px]">
            <li  v-for="prof in professors" :key="prof.professor_id" 
            @click="goToProf(prof.professor_id)" class="cursor-pointer">
                <ProfCard
                :lname="prof.l_name"
                :fname="prof.f_name"
                :avgScore="3"
                :numReviews="128"
                />
            </li>
        </ul>
        </div>
    </div>
</div> 

</template>


<style scoped>  

.navbar {
  width: 100%;
  background-color: #5c898d;
  height: 4rem;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.logo-circle {
  background-color: #d9d9d9;
  border-radius: 9999px;
  height: 2.5rem;
  width: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-img {
  height: 1.75rem;
  width: 1.75rem;
  object-fit: contain;
}

</style>
