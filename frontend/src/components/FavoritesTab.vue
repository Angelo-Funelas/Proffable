<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/axios"

const emit = defineEmits(["message"])
const router = useRouter()

const favoriteProfessors = ref([])

const fetchFavoriteProfessors = async () => {
  try {
    const res = await api.get("favorite-prof/")
    favoriteProfessors.value = res.data
  } catch (err) {
    console.error(
      "GET /favorite-prof failed:",
      err.response?.status,
      err.response?.data || err.message
    )
    emit("message", {
      text: "Failed to load favorite professors.",
      type: "error",
    })
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
    emit("message", {
      text: "Favorite professor removed.",
      type: "success",
    })
  } catch (err) {
    console.error(
      "DELETE /favorite-prof failed:",
      err.response?.status,
      err.response?.data || err.message
    )
    emit("message", {
      text: "Failed to remove favorite professor.",
      type: "error",
    })
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
  <div class="bg-card rounded-[24px] p-8 shadow-xl border border-gray-100 text-left">
    <div class="mb-6">
      <h1
        class="text-4xl font-bold text-text-main tracking-tight max-[980px]:text-2xl"
      >
        Favorite Professors<span class="text-primary">.</span>
      </h1>
      <p class="text-text-muted mt-2 text-lg max-[980px]:text-base">
        Professors you've saved for quick access.
      </p>
    </div>

    <div
      v-if="favoriteProfessors.length === 0"
      class="text-text-muted italic py-4"
    >
      You don't have any favorite professors yet.
    </div>

    <div v-else class="flex flex-col gap-4">
      <div
        v-for="prof in favoriteProfessors"
        :key="prof.id"
        class="bg-card border border-gray-100 rounded-xl p-5 shadow-sm hover:border-primary/30 transition-all"
      >
        <div class="flex justify-between items-start gap-4">
          <div class="flex-1 min-w-0">
            <h3
              class="text-lg font-bold text-primary cursor-pointer hover:underline transition-colors truncate"
              @click="goToProfessorProfile(prof.professor_id)"
            >
              {{ getProfessorFullName(prof) || prof.professor_name }}
            </h3>

            <p class="text-sm text-text-muted mt-0.5">
              {{ prof.institution || prof.email || 'Faculty Member' }}
            </p>

            <div
              v-if="prof.avg_score != null"
              class="flex items-center gap-1.5 mt-2"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 40 38"
                class="fill-accent"
              >
                <path
                  d="M20,0l6.2,12.5,13.8,2-10,9.7,2.4,13.8-12.4-6.5-12.4,6.5,2.4-13.8L0,14.5l13.8-2L20,0Z"
                />
              </svg>
              <span class="font-bold text-sm text-text-main">
                {{ Number(prof.avg_score).toFixed(2) }}
              </span>
              <span class="text-text-muted text-xs">
                ({{ prof.review_count || 0 }}
                {{ prof.review_count === 1 ? 'review' : 'reviews' }})
              </span>
            </div>

            <div
              v-if="prof.courses && prof.courses.length > 0"
              class="mt-3"
            >
              <span class="text-xs font-bold text-text-main">Courses:</span>
              <div class="flex flex-wrap gap-1.5 mt-1">
                <span
                  v-for="course in prof.courses"
                  :key="course.code"
                  class="text-xs bg-surface text-primary font-semibold px-2.5 py-1 rounded-lg border border-gray-100 cursor-default"
                  :title="course.name"
                >
                  {{ course.code }}
                </span>
              </div>
            </div>

            <div
              v-if="prof.tags && prof.tags.length > 0"
              class="flex flex-wrap gap-1.5 mt-3 items-center"
            >
              <span class="text-xs font-bold text-text-main">Tags:</span>
              <span
                v-for="tag in prof.tags"
                :key="tag"
                class="text-[11px] bg-surface text-primary font-bold px-2 py-0.5 rounded-full border border-gray-100"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="flex flex-col items-end gap-3 shrink-0 pt-1">
            <button
              class="text-xs font-semibold text-red-500 hover:text-red-700 transition-colors cursor-pointer"
              @click="removeFavorite(prof.id)"
            >
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>