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
  <div class="bg-card shadow-md rounded-xl p-[18px] text-text-main text-left h-full border border-gray-100">
    <h3 class="text-xl font-bold mb-4 text-primary">Grade Distribution</h3>

    <div v-if="sortedDistribution.length > 0" class="flex flex-col space-y-4">
      <div v-for="item in sortedDistribution" :key="item.grade">
        
        <div class="flex justify-between items-end mb-1">
          <span class="font-bold text-sm text-text-main">
            {{ item.grade }} 
            <span class="text-[10px] font-normal text-text-muted ml-1">({{ gradeRanges[item.grade] }})</span>
          </span>
          <span class="text-xs font-bold text-primary">
            {{ Math.round(item.percentage) }}%
          </span>
        </div>
        
        <div class="w-full bg-surface rounded-full h-2.5 overflow-hidden">
          <div
            class="bg-primary h-full rounded-full transition-all duration-1000 ease-out"
            :style="{ width: animated ? item.percentage + '%' : '0%' }"
          ></div>
        </div>

      </div>
    </div>

    <div v-else class="flex items-center justify-center h-32 text-sm italic text-text-muted opacity-60">
      No grade data available.
    </div>
  </div>
</template>