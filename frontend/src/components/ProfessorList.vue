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
<div class="grid grid-cols-[4fr_11fr] gap-x-[30px] w-screen p-[64px]"> 
    <!--LEFT DIV-->
    <div class="flex flex-col gap-2 text-left">
        <input class="rounded-xl bg-[#FFFFFF] form-text mt-[5px] h-[35px]" placeholder="INSERT SEARCH BAR HERE"/>
        <!--QUERY/FILTERS DIV-->
        <div class="bg-[#52848A] rounded-xl p-[18px]  flex flex-col gap-2 text-left">
            <p>UNIVERSITY</p>
            <p>DEPARTMENT</p>
        </div>
    </div>

    <!--RIGHT DIV-->
    <div>
        <h1 class="text-5xl font-bold text-left">Professors</h1>
    <p v-if="isLoading">Loading professors...</p>

    <ul class="grid grid-cols-1 gap-y-[10px]">
        <li  v-for="prof in professors" :key="prof.professor_id">
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

</template>

const props = defineProps({
    lname: String,
    fname: String,
    avgScore: String,
    tags: Array,
    numReviews: String,
})