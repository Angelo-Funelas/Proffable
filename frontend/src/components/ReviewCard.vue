<script setup>
import {ref, onMounted, watch, computed} from 'vue'
import { useFloating, offset, flip, shift } from '@floating-ui/vue'
import { onClickOutside } from '@vueuse/core'
import api from "@/api/axios"
import ReviewFormNew from './ReviewFormNew.vue'

const props = defineProps({
  reviewId: Number,
  semester: String,
  subject: String,
  reviewText: String,
  grade: String,
  rating: Number,
  tags: Array,
  likes: Number,
  isOwner: Boolean,
  isModerator: Boolean,
})  

const showReportModal = ref(false)
const reason = ref("")
const description = ref("")
const helpfulCountLocal = ref(props.likes) 
const hasVoted = ref(false) 

const submitReport = async () => {

  try {
    const response = await api.post("review-reports/", {
      review: props.reviewId,
      reason: reason.value,
      description: description.value
    })

    alert("Report submitted.")

    showReportModal.value = false
    reason.value = ""
    description.value = ""

  } catch (error) {
    console.error(error)
    alert("Error submitting report.")
  }

}

onMounted(async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reviews/${props.reviewId}/has_voted/`, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      hasVoted.value = data.voted
    }
  } catch (error) {
    console.error("Could not check vote status", error)
  }
})

const toggleHelpful = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reviews/${props.reviewId}/vote/`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
      },
    });

    if (!response.ok) throw new Error("Failed to vote");

    const data = await response.json()
    helpfulCountLocal.value = data.helpful_count
    hasVoted.value = data.voted

  } catch (error) {
    console.error(error);
    alert("Error updating vote");
  }
};

const review_data = ref({
  reviewId: null,
  semester: '',
  subject: '',
  reviewText: '',
  grade: '',
  rating: 0,
  tags: [],
  likes: 0,
  isOwner: false,
})

watch(() => props, (newProps) => {
  review_data.value = {
    ...newProps,
  }
}, { immediate: true, deep: true })

const handleEdit = (rating, grade_received, comment_text) => {
    review_data.value.rating = rating;
    review_data.value.grade_received = grade_received;
    review_data.value.reviewText = comment_text;
    isEditing.value = false;
    emit('edit');
}
const isEditing = ref(false) 

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
const emit = defineEmits(['delete', 'edit'])

const canDelete = computed(() => props.isOwner || props.isModerator)

const deleteReview = async () => {
  const confirmMsg = "MODERATOR ACTION: Are you sure you want to delete this user's review?";
  
  if (confirm(confirmMsg)) {
    try {
      await api.delete(`reviews/${props.reviewId}/`);
      emit('delete');
    } catch (error) {
      console.error("Failed to delete review:", error);
    }
  }
}


const handleDelete = async () => {
    await api.delete(`reviews/${props.reviewId}/`);
    emit('delete');
}
</script>

<template>
    <div class="bg-card shadow-sm rounded-xl p-6 flex flex-col gap-3 text-left text-text-main border border-gray-100">
        
        <div class="flex justify-between items-start">
            <div class="flex gap-3 items-center">
                <div class="w-10 h-10 rounded-full bg-surface border border-gray-200 flex items-center justify-center">
                    <img src="../assets/User.png" class="h-5 opacity-70">
                </div>
                <div class="flex flex-col">
                <div class="flex items-center gap-2">
                    <span class="font-bold text-sm text-text-main">
                        {{ isOwner ? 'Me' : 'Anonymous Student' }}
                    </span>
                    
                    <span v-if="isOwner" class="bg-primary/10 text-primary text-[10px] px-1.5 py-0.5 rounded-md font-bold uppercase tracking-tight">
                        Author
                    </span>
                </div>
                
                <span class="text-[11px] text-text-muted uppercase tracking-wider">
                    {{ semester }} | {{ subject }}
                </span>
            </div>
            </div>
            
            <div class="flex items-center gap-2">
                <button v-if="isOwner" @click="isEditing = true" class="p-1 hover:bg-surface rounded-lg transition-colors">
                    <img src="../assets/edit.svg" class="h-6 opacity-80">
                </button>
                
                <button v-if="isOwner" @click="showModal = true" ref="reference" class="p-1 hover:bg-red-50 rounded-lg transition-colors">
                    <img src="../assets/delete.svg" class="h-6 opacity-80">
                </button>

                <button 
                    v-if="isModerator && !isOwner" 
                    @click="deleteReview" 
                    class="text-[10px] font-bold bg-red-50 text-red-600 px-2 py-1 rounded border border-red-100 hover:bg-red-100"
                >
                    MOD DELETE
                </button>

                <button v-if="!isOwner && !isModerator" @click="showReportModal = true" class="p-1 hover:bg-surface rounded-lg transition-colors">
                    <img src="../assets/Flag.png" class="h-6 opacity-80">
                </button>

                <div v-if="showModal" ref="floating" :style="floatingStyles" class="bg-white w-64 border-gray-200 border shadow-2xl p-4 rounded-xl z-50">
                    <p class="text-sm mb-3 text-text-main font-medium">Permanently delete your review?</p>
                    <div class="flex justify-end gap-2">
                        <button @click="showModal = false" class="text-xs px-3 py-1.5 rounded-lg text-text-muted hover:bg-surface">Cancel</button>
                        <button @click="handleDelete" class="text-xs bg-red-600 text-white rounded-lg px-3 py-1.5 font-bold">Delete</button>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="!isEditing" class="space-y-3">
            
            <div class="flex gap-0.5">
                <svg 
                    v-for="n in 5" 
                    :key="n"
                    width="24" 
                    height="24" 
                    viewBox="0 0 40 38"
                    class="inline transition-colors duration-300"
                    :class="n <= review_data.rating ? 'fill-accent' : 'fill-gray-200'"
                >
                    <path d="M20,0l6.2,12.5,13.8,2-10,9.7,2.4,13.8-12.4-6.5-12.4,6.5,2.4-13.8L0,14.5l13.8-2L20,0Z"/>
                </svg>
            </div>
            
            <p class="text-[15px] leading-relaxed text-text-main">
                <span class="font-bold text-primary">Review:</span> {{ review_data.reviewText }}
            </p>

            <div class="flex items-center gap-6">
                <p class="text-xs text-text-muted">
                    <span class="font-bold text-text-main">Grade:</span> {{ review_data.grade }}
                </p>
                <div v-if="review_data.tags && review_data.tags.length > 0" class="flex gap-2 items-center">
                    <span class="text-xs font-bold text-text-main">Tags:</span>
                    <div class="flex flex-wrap gap-1">
                        <span v-for="tag in review_data.tags" :key="tag.tag_name" 
                            class="text-[10px] bg-surface text-primary font-bold px-2 py-0.5 rounded-md border border-gray-100">
                            {{ tag.tag_name }}
                        </span>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-2 pt-3 border-t border-gray-50 mt-2">
                <button 
                    @click="toggleHelpful"
                    class="flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all text-xs font-bold"
                    :class="hasVoted ? 'bg-primary text-white border-primary shadow-sm' : 'bg-white text-text-muted border-gray-200 hover:border-primary hover:text-primary'"
                >
                    <svg class="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z" />
                        <path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                    </svg>
                    {{ helpfulCountLocal }}
                </button>
                <span class="text-[11px] text-text-muted italic">students found this helpful</span>
            </div>
        </div>

        <div v-if="showReportModal" class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-[100]">
            <div class="bg-white p-6 rounded-2xl w-[340px] shadow-2xl animate-in fade-in zoom-in duration-200">
                <h2 class="text-xl font-bold mb-1 text-primary">Report Review</h2>
                <p class="text-xs text-text-muted mb-4">Help us maintain a helpful community.</p>

                <select v-model="reason" class="bg-surface border border-gray-200 p-2.5 w-full mb-3 rounded-xl text-sm text-text-main outline-none focus:ring-2 focus:ring-primary/20">
                    <option disabled value="">Select reason</option>
                    <option value="offensive">Offensive Language</option>
                    <option value="spam">Spam</option>
                    <option value="fake">Fake Review</option>
                    <option value="harassment">Harassment</option>
                    <option value="irrelevant">Irrelevant Content</option>
                    <option value="other">Other</option>
                </select>

                <textarea
                    v-model="description"
                    placeholder="Provide more context..."
                    class="bg-surface border border-gray-200 p-3 w-full mb-4 rounded-xl text-sm text-text-main placeholder:text-text-muted outline-none focus:ring-2 focus:ring-primary/20 resize-none h-28"
                ></textarea>

                <div class="flex justify-end gap-2">
                    <button @click="showReportModal = false" class="px-4 py-2 rounded-xl text-sm font-bold text-text-muted hover:bg-surface transition-colors">
                        Cancel
                    </button>
                    <button @click="submitReport" class="bg-primary text-white px-5 py-2 rounded-xl text-sm font-bold shadow-md hover:bg-primary-hover transition-all">
                        Submit Report
                    </button>
                </div>
            </div>
        </div>

        <div v-if="isEditing">
            <ReviewFormNew
                @cancelReview="isEditing = false"
                @submitReview="handleEdit"
                :reviewId="reviewId"
                :editing="isEditing"
                :review_rating="rating"
                :comment_text="reviewText"
                :grade_received="grade"
            />
        </div>
    </div>
</template>