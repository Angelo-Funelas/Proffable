<script setup>
    import { ref, onMounted, watch } from 'vue'
    import api from "@/api/axios" 

    const props = defineProps(['professorId'])
    const distribution = ref([])

    const fetchAnalytics = async () => {
        if (!props.professorId) return 
        try {
            const response = await api.get(`professors/${props.professorId}/analytics/`)
            distribution.value = response.data.distribution
        } catch (error) {
            console.error("Failed to load analytics:", error)
        }
    }

    onMounted(fetchAnalytics)
    watch(() => props.professorId, fetchAnalytics)
</script>

<template>
  <div class="bg-white rounded-xl p-[18px] text-[#719294] text-left">
    <h3 class="text-2xl font-bold mb-4">Grade Distribution</h3>
    
    <div v-if="distribution.length > 0" class="flex flex-col space-y-1.5">
      <div v-for="item in distribution" :key="item.grade" class="flex items-center gap-3">
        <span class="w-8 font-bold">{{ item.grade }}</span>
        <div class="w-[250px] bg-[#e9e9e9] rounded-full h-4">
          <div 
            class="bg-[#719294] h-4 rounded-full transition-all duration-700"
            :style="{ width: item.percentage + '%' }"
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