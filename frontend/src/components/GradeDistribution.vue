<script setup>
    import { ref, computed, onMounted, watch, nextTick } from 'vue'
    import api from "@/api/axios"

    const props = defineProps(['professorId'])
    const distribution = ref([])
    const animated = ref(false)

    const gradeOrder = ['A', 'B+', 'B', 'C+', 'C', 'D', 'F']

    const gradeRanges = {
        'A':  '90–100',
        'B+': '90–100',
        'B':  '80–89',
        'C+': '70–79',
        'C':  '70–79',
        'D':  '60–69',
        'F':  'Below 60'
    }

    const sortedDistribution = computed(() =>
        [...distribution.value].sort((a, b) => {
            const ai = gradeOrder.indexOf(a.grade)
            const bi = gradeOrder.indexOf(b.grade)
            const aIdx = ai === -1 ? gradeOrder.length : ai
            const bIdx = bi === -1 ? gradeOrder.length : bi
            return aIdx - bIdx
        })
    )

    const fetchAnalytics = async () => {
        if (!props.professorId) return
        try {
            animated.value = false
            const response = await api.get(`professors/${props.professorId}/analytics/`)
            distribution.value = response.data.distribution
            await nextTick()
            setTimeout(() => { animated.value = true }, 50)
        } catch (error) {
            console.error("Failed to load analytics:", error)
        }
    }

    onMounted(fetchAnalytics)
    watch(() => props.professorId, fetchAnalytics)

    defineExpose({ fetchAnalytics })
</script>

<template>
  <div class="bg-white rounded-xl p-[18px] text-[#719294] text-left">
    <h3 class="text-2xl font-bold mb-4">Grade Distribution</h3>

    <div v-if="sortedDistribution.length > 0" class="flex flex-col space-y-1.5">
      <div v-for="item in sortedDistribution" :key="item.grade" class="flex items-center gap-3">
        <span class="w-20 font-bold text-sm">{{ gradeRanges[item.grade] ?? '—' }}</span>
        <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
          <div
            class="bg-[#719294] h-4 rounded-full transition-all duration-700"
            :style="{ width: animated ? item.percentage + '%' : '0%' }"
          ></div>
        </div>
        <span class="text-sm">{{ item.percentage }}%</span>
      </div>
    </div>

    <div v-else class="text-sm italic opacity-70">
      No grade data available yet.
    </div>
  </div>
</template>