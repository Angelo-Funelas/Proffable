<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from 'vue-router'
import api from "@/api/axios"
import ReviewCard from "./ReviewCard.vue"

const emit = defineEmits(['message'])
const router = useRouter()

const userReviews = ref([])

const fetchUserReviews = async () => {
  try {
    const res = await api.get("reviews/?mine=true")
    userReviews.value = res.data
  } catch (err) {
    console.error("GET /reviews?mine=true failed:", err.response?.status, err.response?.data || err.message)
    emit('message', { text: "Failed to load your reviews.", type: "error" })
  }
}

onMounted(() => {
  fetchUserReviews()
})

const handleReviewDeleted = (reviewId) => {
  userReviews.value = userReviews.value.filter(
    (review) => review.review_id !== reviewId
  )
  emit('message', { text: "Review deleted successfully.", type: "success" })
}

const goToProfessorProfile = (professorId) => {
  if (!professorId) return
  router.push(`/professor/${professorId}`)
}
</script>

<template>
  <div class="bg-card rounded-[24px] p-8 shadow-xl border border-gray-100 text-left">
    <div class="mb-6">
      <h1
        class="text-4xl font-bold text-text-main tracking-tight max-[980px]:text-2xl"
      >
        Your Reviews<span class="text-primary">.</span>
      </h1>
      <p class="text-text-muted mt-2 text-lg max-[980px]:text-base">
        Reviews you've shared with other students.
      </p>
    </div>

    <div v-if="userReviews.length === 0" class="text-text-muted italic py-4">
      You have not submitted any reviews yet. Share your experience to help
      other students choose professors.
    </div>

    <div v-else class="flex flex-col gap-5">
      <div v-for="review in userReviews" :key="review.review_id">
        <!-- Professor link above each review card -->
        <p
          class="mb-2 text-sm font-bold text-primary cursor-pointer hover:underline transition-colors"
          @click="goToProfessorProfile(review.professor)"
        >
          {{ review.professor_name }} &rarr;
        </p>

        <ReviewCard
          :reviewId="review.review_id"
          :reviewText="review.comment_text"
          :grade="review.received_grade"
          :rating="review.review_rating"
          :tags="review.tags || []"
          :likes="review.helpful_count"
          :isOwner="true"
          :isModerator="false"
          :courseCode="review.course_code || ''"
          :courseName="review.course_name || ''"
          :semesterTerm="review.semester_term || ''"
          :semesterYear="review.semester_year || ''"
          @delete="handleReviewDeleted(review.review_id)"
          @edit="fetchUserReviews"
        />
      </div>
    </div>
  </div>
</template>