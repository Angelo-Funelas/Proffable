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
    import GradeDistribution from './GradeDistribution.vue'

    const professor = ref({})
    const route = useRoute()
    const reviews = ref([])
    const courses = ref([])
    const router = useRouter()
    const gradeDistRef = ref(null)
    
    const professors = ref()

    const isModerator = ref(false)
    const isAuthorized = ref(false)

    async function checkModStatus() {
    try {
        const res = await api.get('me/')
        isModerator.value = res.data.is_moderator
        isAuthorized.value = true
    } catch (err) {
        console.error(err)
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
        gradeDistRef.value?.fetchAnalytics()
    }

    const handleReviewSubmit = () => {
        fetchReviews()
        gradeDistRef.value?.fetchAnalytics()
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
            if (error.response.status == 401) {
                router.push({ 
                    path: '/login', 
                    query: { next: router.currentRoute.value.fullPath } 
                })
            }
        }
    }
    const goToProf = (professorId) => {
        console.log('navigating to', professorId)
        router.push(`/professor/${professorId}`)
    }

    const formattedAvgRating = computed(() => {
    const rating = professor.value.avg_rating;
    return rating ? Number(rating).toFixed(2) : "0.00";
    });

    const reviewCountText = computed(() => {
    const count = professor.value.review_count || 0;
    if (count === 1) return '1 review';
    return `${count} reviews`;
    });

    const sortedReviews = computed(() => {
    if (!reviews.value) return [];
    return [...reviews.value].sort((a, b) => {
        if (a.is_owner && !b.is_owner) return -1;
        if (!a.is_owner && b.is_owner) return 1;
        return b.review_id - a.review_id;
    });
});

    watch(() => route.params.professorId, () => {
        professor_reviewed.value = false
        fetchProfessor()
        fetchReviews()
        fetchSimilar()
        checkModStatus()
        fetchCourses()
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
                <h2 class="text-xl font-bold text-left mt-8 mb-4 text-primary tracking-tight">
                    Similar Professors
                </h2>

                <ul class="grid grid-cols-1 gap-3">
                    <template v-if="professors && professors.length > 0">
                        <li 
                            v-for="prof in professors" 
                            :key="prof.professor_id" 
                            @click="goToProf(prof.professor_id)"
                            class="cursor-pointer transition-transform duration-200 hover:scale-[1.02] active:scale-100"
                        >
                            <ProfCard
                                :lname="prof.l_name"
                                :fname="prof.f_name"
                                :institutions="prof.institutions"
                                :avgScore="prof.avg_rating || 0"
                                :numReviews="prof.review_count"
                                :tags="prof.tags"
                                :is_favorited="prof.is_favorited"
                                :favoriteCount="prof.favorite_count"
                                :showHeart="false"
                            />
                        </li>
                    </template>
    <div v-else class="bg-surface border border-dashed border-gray-300 rounded-xl p-8 text-center">
        <p class="text-sm text-text-muted italic">No similar professors found.</p>
    </div>
</ul>
            </div>

            <!--RIGHT DIV-->
            <div>
                <!--PROFESSOR CARD-->
                <h1 class="text-5xl font-bold text-left">{{ professor.f_name }} {{ professor.l_name }}</h1>
                <div class="bg-card shadow-md rounded-xl p-[18px] flex justify-between items-start mt-2.5">
                    <div class="flex flex-col gap-2 text-left">
                        <h3 class="text-2xl"><span class="font-bold">{{ professor.institutions?.map(i => i.name).join(', ') || 'Unknown Institution' }}</span> </h3>
                        <p class="text-sm flex items-center gap-1.5">
                            <svg width="18" height="18" viewBox="0 0 40 38" class="fill-accent">
                                <path d="M20,0l6.2,12.5,13.8,2-10,9.7,2.4,13.8-12.4-6.5-12.4,6.5,2.4-13.8L0,14.5l13.8-2L20,0Z"/>
                            </svg>
                            
                            <span class="font-bold text-text-main">{{ formattedAvgRating }}</span>
                            
                            <span class="text-text-muted">({{ reviewCountText }})</span>
                        </p>
                        <div class="text-sm flex flex-wrap gap-2 items-center">
                            <div class="text-sm flex flex-wrap gap-2 items-center mt-2">
                                <span class="font-bold text-text-main">Tags:</span>
                                
                                <template v-if="professor.tags && professor.tags.length > 0">
                                    <span v-for="tag in professor.tags" :key="tag" 
                                        class="bg-surface text-primary border border-gray-100 px-3 py-0.5 rounded-full text-[11px] font-bold shadow-sm">
                                        {{ tag.tag_name }}
                                    </span>
                                </template>
                                <span v-else class="text-text-muted italic text-xs">No tags yet</span>
                            </div>
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
                    <GradeDistribution ref="gradeDistRef" :professorId="professor.professor_id" />
                </div>
                <div v-if="isAuthorized" class="bg-card shadow-lg mt-4 text-left rounded-2xl p-8 border border-gray-100">
                    <ReviewFormNew @submitReview="handleReviewSubmit"/>
                </div>
                <!--REVIEW CARDS-->
                <div class="flex justify-between items-center">
                    <h1 class="text-2xl font-bold text-left my-2.5">Reviews ({{reviews.length}})</h1>
                </div>
                <div>
                    <ul class="grid grid-cols-1 gap-2.5">
                        <li v-for="review in sortedReviews" :key="review.review_id">
                            <ReviewCard
                                @delete="handleDelete"
                                @edit="fetchReviews(); gradeDistRef?.fetchAnalytics()"
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
