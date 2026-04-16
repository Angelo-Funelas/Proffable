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
</script>

<template>
  <div class="tab-panel">
    <h1 class="section-title">Your Reviews</h1>

    <div v-if="userReviews.length === 0" class="empty-state">
      You have not submitted any reviews yet. Share your experience to help other students choose professors.
    </div>

    <div v-else class="reviews-list">
      <article
        v-for="review in userReviews"
        :key="review.review_id"
        class="review-card"
      >
        <div class="review-header">
          <div>
            <h3
              class="clickable-info"
              @click="goToProfessorProfile(review.professor)"
            >
              {{ review.professor_name }}
            </h3>
            <p class="review-date">{{ formatDate(review.review_date) }}</p>
          </div>

          <div class="review-rating">
            {{ review.review_rating }}/5
          </div>
        </div>

        <p class="review-comment">{{ review.comment_text }}</p>

        <div class="review-meta">
          <span>Grade: {{ review.received_grade || "N/A" }}</span>
          <span>Helpful: {{ review.helpful_count }}</span>
        </div>

        <div class="review-actions">
          <button
            class="secondary-btn"
            @click="goToProfessorProfile(review.professor)"
          >
            View Professor
          </button>
          <button
            class="danger-btn small-btn"
            @click="deleteReview(review.review_id)"
          >
            Delete
          </button>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.tab-panel {
  background: white;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.section-title {
  font-size: 2rem;
  font-weight: 800;
  color: #5a624f;
  margin: 0 0 1.25rem 0;
}

.empty-state {
  font-size: 1rem;
  color: #6b7280;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1rem;
}

.review-card h3 {
  margin: 0 0 0.3rem 0;
  color: #333;
}

.review-date,
.review-comment,
.review-meta {
  margin: 0;
  color: #666;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.review-rating {
  background: #719294;
  color: white;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  font-weight: 700;
}

.review-comment {
  margin-top: 0.85rem;
  line-height: 1.5;
}

.review-meta {
  margin-top: 0.85rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.95rem;
}

.review-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.75rem;
}

.clickable-info {
  cursor: pointer;
}

.clickable-info:hover {
  opacity: 0.85;
}

.secondary-btn,
.danger-btn {
  border: none;
  border-radius: 999px;
  padding: 0.7rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: filter 0.15s, background 0.15s;
}

.secondary-btn {
  background: white;
  color: #4f6c72;
  border: 1px solid #d1d5db;
}

.secondary-btn:hover {
  background: #f3f4f6;
}

.danger-btn {
  background: #c94b4b;
  color: white;
}

.danger-btn:hover {
  filter: brightness(1.08);
}

.small-btn {
  padding: 0.55rem 0.9rem;
  font-size: 0.85rem;
}

@media (max-width: 980px) {
  .section-title {
    font-size: 1.6rem;
  }
}
</style>
