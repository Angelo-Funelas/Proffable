<script setup>
    import {ref, computed, onMounted, watch} from 'vue'
    import api from "@/api/axios"
    import ProfCard from './ProfCard.vue'
    import ReviewCard from './ReviewCard.vue'
    import SearchFilters from './SearchFilters.vue'
    import { useRoute } from 'vue-router'
    import Navbar from './Navbar.vue';
    import { useRouter } from 'vue-router'
    import RatingSelector from './RatingSelector.vue'
    import ReviewFormNew from './ReviewFormNew.vue'
    import Heart from './Heart.vue'
    import AiOverview from './AiOverview.vue'

    const professor = ref({})
    const route = useRoute()
    const reviews = ref([])
    const courses = ref([])
    const router = useRouter()
    
    const professors = ref()

    const isModerator = ref(false)

    async function checkModStatus() {
    try {
        const res = await api.get('me/')
        isModerator.value = res.data.is_moderator
    } catch (err) {
        isModerator.value = false
    }
}

    async function fetchProfessor(){
        isLoading.value = true
        try{
            const response = await api.get(`professors/${route.params.professorId}`)
            professor.value = response.data
            console.log(professor.value.read_tags)
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
                if (!review.is_owner) continue
                professor_reviewed.value = true
                break
            }
        } catch(error){
            console.log("Error with fetching reviews: ", error)
        }
    }
    async function fetchSimilar(){
        isLoading.value = true
        try{
            const response = await api.get(`professors/${route.params.professorId}/similar/`)
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

    async function fetchCourses(){
        try{
            const response = await api.get(`professors/${route.params.professorId}/courses/`)
            courses.value = response.data
            console.log(courses.value)
        } catch(error){
            console.log("Error with fetching professors: ",error)
        }
    }

    onMounted(()=>{
        fetchProfessor()
        fetchReviews()
        checkModStatus()
        fetchSimilar()
        fetchCourses()
    })

    async function toggleFavorite() {
        try{
            if (professor.value.is_favorited){
                await api.delete(`favorite-prof/${professor.value.favorite_id}/`)
            } else {
                const response = await api.post('favorite-prof/' ,{
                professor_id: route.params.professorId
            })
            
            }
            fetchProfessor()
        } catch(error){
            console.log("Error toggling favorite: ",error)
        }
    }
    const goToProf = (professorId) => {
        console.log('navigating to', professorId)
        router.push(`/professor/${professorId}`)
    }
    watch(() => route.params.professorId, () => {
        professor_reviewed.value = false
        fetchProfessor()
        fetchReviews()
        fetchSimilar()
        checkModStatus()
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
                    <li  v-for="prof in professors" :key="prof.professor_id" @click="goToProf(prof.professor_id)"
                    class="cursor-pointer">
                        <ProfCard
                        :lname="prof.l_name"
                        :fname="prof.f_name"
                        :avgScore="prof.avg_rating || 0"
                        :numReviews="prof.review_count"
                        :tags="prof.tags"
                        :is_favorited="prof.is_favorited"
                        :favoriteCount="prof.favorite_count"
                        />
                    </li>
                </ul>
            </div>

            <!--RIGHT DIV: contains hardcoded data-->
            <div>
                <!--PROFESSOR CARD-->
                <h1 class="text-5xl font-bold text-left">{{ professor.f_name }} {{ professor.l_name }}</h1>
                <div class="bg-card shadow-md rounded-xl p-[18px] flex justify-between items-start mt-2.5">
                    <div class="flex flex-col gap-2 text-left">
                        <h3 class="text-2xl"><span class="font-bold">{{ professor.institutions?.map(i => i.name).join(', ') 
                        || 'Unknown Institution' }}</span> </h3>
                        <p class="text-sm flex items-center gap-[2px]"><img src="../assets/Star.svg" class="h-[16px]"> 
                            {{professor.avg_rating}} ({{ professor.review_count }} review/s)</p>
                        <div class="text-sm flex flex-wrap gap-1 items-center"><span>Tags:</span>
                            <span v-for="tag in professor.tags" :key="tag" class='bg-gray-200 text-[#719294] px-2 py-1 rounded-full'>
                                {{ tag }}
                            </span>
                        </div>
                        <h2><span class="font-bold">Courses: {{ courses?.map(i => i.course_name).join(', ') || 
                        'No Registered Courses' }}</span> </h2>
                    </div>

                    <!-- FAVORITE PROF-->
                    <Heart @click=toggleFavorite :filled="professor.is_favorited" :favorite_count="professor.favorite_count"/>
                </div>
                <div class="grid grid-cols-[2.1fr_1fr] gap-[10px] mt-2.5">
                    <AiOverview :professor_id="route.params.professorId"/>
                    <!--GRADE DISTRIBUTION-->
                    <div class="bg-card shadow rounded-xl p-[18px] text-[#719294] text-left">
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
                <div class="bg-card shadow p-4 pt-2 mt-4 rounded-xl text-left">
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
                                @edit="fetchReviews"
                                :reviewId="review.review_id"
                                :is-owner="review.is_owner"
                                :is-moderator="isModerator" 
                                :review-text="review.comment_text"
                                :rating="review.review_rating"
                                :grade="review.received_grade"
                                :likes="review.helpful_count"
                                :tags="review.read_tags"
                                :course-code="review.course_code"
                                :course-name="review.course_name"
                                :semester-term="review.read_semester_term"
                                :semester-year="review.semester_year"
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
