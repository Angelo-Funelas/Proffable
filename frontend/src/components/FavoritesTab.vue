<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from 'vue-router'
import api from "@/api/axios"

const emit = defineEmits(['message'])
const router = useRouter()

const favoriteProfessors = ref([])

const fetchFavoriteProfessors = async () => {
  try {
    const res = await api.get("favorite-prof/")
    favoriteProfessors.value = res.data
  } catch (err) {
    console.error("GET /favorite-prof failed:", err.response?.status, err.response?.data || err.message)
    emit('message', { text: "Failed to load favorite professors.", type: "error" })
  }
}

onMounted(() => {
  fetchFavoriteProfessors()
})

const removeFavorite = async (favoriteId) => {
  try {
    await api.delete(`favorite-prof/${favoriteId}/`)
    favoriteProfessors.value = favoriteProfessors.value.filter(
      (prof) => prof.id !== favoriteId
    )
    emit('message', { text: "Favorite professor removed.", type: "success" })
  } catch (err) {
    console.error("DELETE /favorite-prof failed:", err.response?.status, err.response?.data || err.message)
    emit('message', { text: "Failed to remove favorite professor.", type: "error" })
  }
}

const getProfessorFullName = (professor) => {
  return [professor.f_name, professor.m_name, professor.l_name]
    .filter(Boolean)
    .join(" ")
}

const goToProfessorProfile = (professorId) => {
  if (!professorId) return
  router.push(`/professor/${professorId}`)
}
</script>

<template>
  <div class="tab-panel">
    <h1 class="section-title">Favorite Professors</h1>

    <div v-if="favoriteProfessors.length === 0" class="empty-state">
      You don't have any favorite professors yet.
    </div>

    <div v-else class="favorites-grid">
      <div
        v-for="prof in favoriteProfessors"
        :key="prof.id"
        class="favorite-card"
      >
        <div
          class="favorite-info clickable-info"
          @click="goToProfessorProfile(prof.professor_id)"
        >
          <h3>{{ getProfessorFullName(prof) || prof.professor_name }}</h3>
          <p>{{ prof.email || "No email available" }}</p>
        </div>

        <button class="secondary-btn" @click="removeFavorite(prof.id)">
          Remove
        </button>
      </div>
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

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.favorite-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.favorite-info h3 {
  margin: 0 0 0.3rem 0;
  color: #333;
}

.favorite-info p {
  margin: 0;
  color: #666;
}

.clickable-info {
  cursor: pointer;
}

.clickable-info:hover {
  opacity: 0.85;
}

.favorite-info.clickable-info {
  flex: 1;
}

.secondary-btn {
  background: white;
  color: #4f6c72;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  padding: 0.7rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.secondary-btn:hover {
  background: #f3f4f6;
}

@media (max-width: 980px) {
  .section-title {
    font-size: 1.6rem;
  }
}
</style>
