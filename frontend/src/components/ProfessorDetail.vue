<script setup>
    import {ref, computed, onMounted} from 'vue'
    import api from "@/api/axios"
    import ProfCard from './ProfCard.vue'
    import ReviewCard from './ReviewCard.vue'
    import SearchFilters from './SearchFilters.vue'
    import { useRoute } from 'vue-router'
    import Navbar from './Navbar.vue';
    import { useRouter } from 'vue-router'
    import RatingSelector from './RatingSelector.vue'
    import ReviewFormNew from './ReviewFormNew.vue'

    const professor = ref({})
    const route = useRoute()
    const reviews = ref([])
    const router = useRouter()

    const API_URL = 'http://localhost:8000/api/'
    const api = axios.create({
        baseURL:API_URL
    })
    
    const professors = ref()
    async function fetchProfessor(){
        isLoading.value = true
        try{
            const response = await api.get(`professors/${route.params.professorId}`)
            professor.value = response.data
        } catch(error){
            console.log("Error with fetching professors: ",error)
        }
        isLoading.value = false
    }
    const professor_reviewed = ref(false)
    async function fetchReviews(){
        try {
            const response = await api.get('reviews/', { params: { professor: route.params.professorId } })
            reviews.value = response.data
            for (const review of response.data) {
                if (review.is_owner) professor_reviewed.value = true
                break
            }
            console.log(response.data)
        } catch(error){
            console.log("Error with fetching reviews: ", error)
        }
    }
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

    const handleDelete = () => {
        professor_reviewed.value = false;
        fetchReviews();
    }

    onMounted(()=>{
        fetchProfessor()
        fetchReviews()
        fetchProfessors()
    })
</script>

<template>
    <Navbar/>
    <div class="main-container">

        <div class="grid grid-cols-[4fr_11fr] gap-x-[30px] w-screen p-[64px]"> 
            <!--LEFT DIV-->
            <div>
                <!--SEARCH FILTERS-->
                <SearchFilters />
                <!--SIMILAR PROFESSORS' CARDS-->
                <h1 class="text-2xl font-bold text-left mt-[30px] mb-[10px]">Similar Professors</h1>
                <ul class="grid grid-cols-1 gap-2.5">
                    <li  v-for="prof in professors" :key="prof.professor_id">
                        <ProfCard
                        :lname="prof.l_name"
                        :fname="prof.f_name"
                        :avgScore="prof.avg_rating || 0"
                        :numReviews="prof.review_count"
                        />
                    </li>
                </ul>
            </div>

            <!--RIGHT DIV: contains hardcoded data-->
            <div>
                <!--PROFESSOR CARD-->
                <h1 class="text-5xl font-bold text-left">{{ professor.f_name }} {{ professor.l_name }}</h1>
                <div class="bg-[#719294] rounded-xl p-[18px] flex justify-between items-start mt-2.5">
                    <div class="flex flex-col gap-2 text-left">
                        <h3 class="text-2xl"><span class="font-bold">University of Unknown</span> | Literature</h3>
                        <p class="text-sm flex items-center gap-[2px]"><img src="../assets/Star.svg" class="h-[16px]"> 
                            {{professor.avg_rating}} ({{ professor.review_count }} review/s)</p>
                        <p class="text-sm">Tags:</p>
                    </div>

                    <div class="flex flex-col items-center gap-1">
                        <img src="../assets/Heart.svg" class="h-[16px]">
                        <span class="text-sm">{{professor.review_count}}</span>
                    </div>
                </div>
                <div class="grid grid-cols-[2.1fr_1fr] gap-[10px] mt-2.5">
                    <!--AI OVERVIEW-->
                    <div class="bg-white rounded-xl p-[18px] flex flex-col text-[#719294] text-left">
                        <h3 class="text-2xl font-bold">AI Overview of Reviews</h3>
                        <ul class="space-y-2 mt-2">
                            <li><span class="font-bold">Pros</span>: Lectures are well-organized and grading is generally fair and transparent.</li>
                            <li><span class="font-bold">Cons</span>: Fast-paced teaching style may require students to keep up with lessons consistently.</li>
                            <li><span class="font-bold">Verdict</span>: Strong choice for students who prefer structured classes and can handle quicker pacing.</li>
                        </ul>
                    </div>
                    <!--GRADE DISTRIBUTION-->
                    <div class="bg-white rounded-xl p-[18px] text-[#719294] text-left">
                        <h3 class="text-2xl font-bold">Grade Distribution</h3>
                        <div class="flex flex-col space-y-1.5">
                            <!-- A -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">A</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[45%]"></div>
                            </div>
                            <span class="text-sm">45%</span>
                            </div>
                            <!-- B+ -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">B+</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[25%]"></div>
                            </div>
                            <span class="text-sm">25%</span>
                            </div>
                            <!-- B -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">B</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[15%]"></div>
                            </div>
                            <span class="text-sm">15%</span>
                            </div>
                            <!-- C+ -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">C+</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[8%]"></div>
                            </div>
                            <span class="text-sm">8%</span>
                            </div>
                            <!-- C -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">C</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[5%]"></div>
                            </div>
                            <span class="text-sm">5%</span>
                            </div>
                            <!-- D -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">D</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[2%]"></div>
                            </div>
                            <span class="text-sm">2%</span>
                            </div>
                            <!-- F -->
                            <div class="flex items-center gap-3">
                            <span class="w-8 font-bold">F</span>
                            <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
                                <div class="bg-[#719294] h-4 rounded-full w-[0%] opacity-40"></div>
                            </div>
                            <span class="text-sm">0%</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="!professor_reviewed" class="bg-white p-4 pt-2 mt-4 rounded-xl text-left">
                    <ReviewFormNew @submitReview="fetchReviews"/>
                </div>
                <!--REVIEW CARDS-->
                <div class="flex justify-between items-center">
                    <h1 class="text-2xl font-bold text-left my-2.5">Reviews ({{reviews.length}})</h1>
                </div>
                <div>
                    <ul class="grid grid-cols-1 gap-2.5">
                        <li v-for="review in reviews" :key="review.review_id">
                            <ReviewCard
                            @delete="handleDelete"
                            :reviewId="review.review_id"
                            :semester="review.semester"
                            :subject="review.subject"
                            :review-text="review.comment_text"
                            :grade="review.received_grade"
                            :rating="review.review_rating"
                            :tags="review.tags"
                            :likes="review.likes"
                            :is-owner="review.is_owner"
                            />
                        </li>
                    </ul>
                </div>
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
