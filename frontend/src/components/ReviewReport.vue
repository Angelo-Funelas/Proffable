<script setup>
import {ref, onMounted, watch, computed} from 'vue'
import { useRouter } from 'vue-router'
import { useFloating, offset, flip, shift } from '@floating-ui/vue'
import { onClickOutside } from '@vueuse/core'
import api from "@/api/axios"
import ReviewFormNew from './ReviewFormNew.vue'

const router = useRouter();
const props = defineProps({
  reportId: Number,
  description: String,
  reason: String,
  reporter: String,
  author: String,
  review_id: Number,
  created_at: String
})

const review_data = ref({});

async function fetchReview() {
  const response = await api.get(`/reviews/${props.review_id}`)
  review_data.value = response.data
  console.log(response.data)
}

onMounted(async () => {
  fetchReview()
})

const reference = ref(null)
const floating = ref(null)
const showModal = ref(false)

onClickOutside(floating, () => (showModal.value = false))
const { floatingStyles } = useFloating(reference, floating, {
  placement: 'top', 
  middleware: [
    offset(10),
    flip(),
    shift()
  ],
})
const emit = defineEmits(['resolve'])

const handleResolve = async () => {
    await api.delete(`review-reports/${props.reportId}/`);
    emit('resolve');
}

const handleDelete = async () => {
    await api.delete(`reviews/${props.review_id}/`);
    emit('resolve');
    showModal.value = false;
}

function goToProf(professor_id) {
    router.push(`/professor/${professor_id}`)
}
</script>

<template>
    <div class="bg-[#f2f2f2] rounded-xl p-5 flex flex-col gap-2 text-left text-[#719294] shadow-md m-2">
        <div class="flex justify-between items-center">
            <div class="flex gap-3 items-center">
                <div class="w-10 h-10 rounded-full bg-[#e9e9e9] border border-[#719294] flex items-center justify-center text-xl">
                    <img src="../assets/User.png" class="h-[20px]">
                </div>
                 <span>{{ author }}</span>
            </div>
            
            <div class="flex">
                <div class="flex align-middle gap-3">
                    <button 
                        @click="showModal=true" 
                        ref="reference"
                        class="text-xs bg-red-100 text-red-600 px-2 py-1 rounded border border-red-200 hover:bg-red-200 transition-colors"
                    >
                        DELETE
                    </button>

                    <button 
                        @click="handleResolve" 
                        class="text-xs bg-green-100 text-green-600 px-2 py-1 rounded border border-green-200 hover:bg-green-200 transition-colors"
                    >
                        RESOLVE
                    </button>

                    <div
                        v-if="showModal"
                        ref="floating"
                        :style="floatingStyles"
                        class="bg-white w-80 border-[#719294] border-2 shadow-xl p-4 rounded-md z-50"
                    >
                        <p class="mb-2 text-[#0B0D09]">Are you sure you want to permanently delete this review?</p>
                        <div class="flex justify-end gap-2">
                            <button @click="handleDelete" class="bg-red-600 text-white rounded-full px-4 py-1 text-sm">Yes, Delete</button>
                            <button @click="showModal = false" class="bg-[#52848A] text-white rounded-full px-4 py-1 text-sm">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex">
            <div v-for="n in (review_data.review_rating || 0)">
                <img src="../assets/BigStarFilled.svg" class="h-[36px]" />
            </div>
            <div v-for="n in 5-(review_data.review_rating || 0)">
                <img src="../assets/BigStar.svg" class="h-[36px]" />
            </div>
        </div>
        
        <p class="text-xl"><span class="font-bold">Review</span>: {{ review_data.comment_text }}</p>
        <p class="text-sm"><span class="font-bold">Grade Received</span>: {{ review_data.received_grade }}</p>

        <div class="flex items-center gap-[2px]">
            <span class="text-sm text-[#719294]">Reported by {{ reporter }}</span>
        </div>
        <p class="underline cursor-pointer" @click="goToProf(review_data.professor)">Go to Page</p>
    </div>
</template>