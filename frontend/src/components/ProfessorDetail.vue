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
    import SearchFilters from './SearchFilters.vue'
</script>

<template>
    <div class="main-container">
        <nav class="navbar">
            <div class="logo-circle">
                <img src="../assets/ProffableLogo.png" alt="Logo" class="logo-img" />
            </div>
        </nav>

        <div class="grid grid-cols-[4fr_11fr] gap-x-[30px] w-screen p-[64px]"> 
            <!--LEFT DIV-->
            <div>
                <SearchFilters/>
                <h1 class="text-2xl font-bold text-left mt-[30px] mb-[10px]">Similar Professors</h1>
                <ul class="grid grid-cols-1 gap-2.5">
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

            <!--RIGHT DIV-->
            <div>
                <h1 class="text-5xl font-bold text-left">Jane Doe</h1>
            </div>
        </div>
    </div>
</template>