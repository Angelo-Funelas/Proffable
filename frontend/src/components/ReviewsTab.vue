<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from 'vue-router'
import api from "@/api/axios"

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

const deleteReview = async (reviewId) => {
  try {
    await api.delete(`reviews/${reviewId}/`)
    userReviews.value = userReviews.value.filter(
      (review) => review.review_id !== reviewId
    )
    emit('message', { text: "Review deleted successfully.", type: "success" })
  } catch (err) {
    console.error("DELETE /reviews failed:", err.response?.status, err.response?.data || err.message)
    emit('message', { text: "Failed to delete review.", type: "error" })
  }
}

const goToProfessorProfile = (professorId) => {
  if (!professorId) return
  router.push(`/professor/${professorId}`)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// === STYLE TOKENS ===
const btnSecondary =
  'bg-card hover:bg-surface text-text-main border border-gray-200 px-6 py-2.5 rounded-full font-semibold text-sm cursor-pointer transition-colors'
const btnDangerSmall =
  'bg-red-600 hover:bg-red-700 text-white px-3.5 py-2 rounded-full font-semibold text-xs cursor-pointer transition-all border-0'
</script>

<template>
  <div class="bg-card rounded-[24px] p-8 shadow-xl border border-gray-100">
    <div class="mb-6 text-left">
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

    <div v-else class="flex flex-col gap-4">
      <article
        v-for="review in userReviews"
        :key="review.review_id"
        class="bg-surface border border-gray-100 rounded-2xl p-4"
      >
        <div class="flex justify-between items-start gap-4">
          <div>
            <h3
              class="m-0 mb-1 text-text-main font-bold text-lg cursor-pointer hover:opacity-80 transition-opacity"
              @click="goToProfessorProfile(review.professor)"
            >
              {{ review.professor_name }}
            </h3>
            <p class="m-0 text-text-muted text-sm">
              {{ formatDate(review.review_date) }}
            </p>
          </div>

          <div
            class="bg-primary text-white px-3 py-1.5 rounded-full font-bold text-sm shadow-sm whitespace-nowrap"
          >
            {{ review.review_rating }}/5
          </div>
        </div>

        <p class="mt-3 text-text-main leading-relaxed">
          {{ review.comment_text }}
        </p>

        <div
          class="mt-3 flex gap-4 flex-wrap text-sm text-text-muted"
        >
          <span>Grade: {{ review.received_grade || "N/A" }}</span>
          <span>Helpful: {{ review.helpful_count }}</span>
        </div>

        <div class="mt-4 flex gap-3">
          <button
            :class="btnSecondary"
            @click="goToProfessorProfile(review.professor)"
          >
            View Professor
          </button>
          <button
            :class="btnDangerSmall"
            @click="deleteReview(review.review_id)"
          >
            Delete
          </button>
        </div>
      </article>
    </div>
  </div>
</template>