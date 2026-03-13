<script setup>
import {ref, watch, onMounted} from 'vue'
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
})

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
const emit = defineEmits(['delete'])
const handleDelete = async () => {
    await api.delete(`reviews/${props.reviewId}/`);
    emit('delete');
}
const showReportModal = ref(false)
const reason = ref("")
const description = ref("")
const helpfulCountLocal = ref(props.likes) 
const hasVoted = ref(false) 

const submitReport = async () => {

  try {
    const response = await fetch("http://127.0.0.1:8000/api/review-reports/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        review: props.reviewId,
        reason: reason.value,
        description: description.value
      })
    })

    if (!response.ok) {
      throw new Error("Failed to submit report")
    }

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

</script>

<template>
    <div class="bg-[#ffffff] rounded-xl p-5 flex flex-col gap-2 text-left text-[#719294]">
        <div class="flex justify-between items-center">
            <div class="flex gap-3 items-center">
                <div class="w-10 h-10 rounded-full bg-[#e9e9e9] border border-[#719294] flex items-center justify-center text-xl">
                    <img src="../assets/User.png" class="h-[20px]">
                </div>
                <!-- Uses Placeholder Semester and Subject Values for Now-->
                 <span>Anonymous Student | 25-26 1st Sem LIT 5111</span>
                <!-- <span>Anonymous Student | {{ review_data.semester }} {{ review_data.subject }}</span> -->
            </div>
            <div class="flex align-middle gap-3">
                <button class="text-sm" @click="showReportModal = true" v-if="isOwner" @click="isEditing = true">
                    <img src="../assets/edit.svg" class="h-[24px]">
                </button>
                <button class="text-sm" v-if="isOwner" @click="showModal=true" ref="reference">
                    <img src="../assets/delete.svg" class="h-[24px]">
                </button>
                <div
                    v-if="showModal"
                    ref="floating"
                    :style="floatingStyles"
                    class="bg-white w-80 border-[#719294] border-2 shadow-xl p-4 rounded-md z-50 shadow-md"
                >
                    <p class="mb-2">Are you sure you want to permanently delete this review?</p>
                    <button @click="handleDelete" class="bg-[#919191] hover:bg-[#9b3838] text-white mx-1 rounded-full px-[18px] py-1 w-max cursor-pointer">Yes, Delete</button>
                    <button @click="showModal = false" class="bg-[#52848A] text-white mx-1 rounded-full px-[18px] py-1 w-max cursor-pointer">Cancel</button>
                </div>
                <button class="text-sm" v-if="!isOwner">
                    <img src="../assets/Flag.png" class="h-[24px]">
                </button>
            </div>
        </div>
        <div v-if="!isEditing">
            <div class="flex">
                <div v-for="n in review_data.rating">
                    <img src="../assets/BigStarFilled.svg" class="h-[36px]" />
                </div>
                <div v-for="n in 5-review_data.rating">
                    <img src="../assets/BigStar.svg" class="h-[36px]" />
                </div>
            </div>
            
            <p class="text-xl"><span class="font-bold">Review</span>: {{ review_data.reviewText }}</p>
            <p class="text-sm"><span class="font-bold">Grade Received</span>: {{ review_data.grade }}</p>

            <div class="flex flex-wrap gap-2">
                <p class="text-sm"><span class="font-bold">Tags</span>:</p>
                <span v-for="(tag, index) in review_data.tags" :key="index" class="text-sm underline px-1">
                    {{ tag }}
                </span>
            </div>

            <p class="italic flex items-center gap-[2px]">
            <img src="../assets/ThumbsUp.png" class="h-[16px] mr-[4px]"> {{ review_data.likes }} found this helpful</p>
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


        <div 
        v-if="showReportModal" 
        class="fixed inset-0 flex items-center justify-center bg-black/30 z-20"
        >
        <div class="bg-white p-6 rounded-xl w-[320px] shadow-lg z-30 text-[#719294]" >
            <h2 class="text-lg font-bold mb-4 text-[#0B0D09]">Report Review</h2>

            <select v-model="reason" class="border border-[#719294] p-2 w-full mb-3 rounded-lg text-sm text-[#0B0D09] outline-none focus:border-[#5c898d]">
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
            placeholder="Additional details (optional)"
            class="border border-[#719294] p-2 w-full mb-4 rounded-lg text-sm text-[#0B0D09] placeholder:text-[#719294] outline-none focus:border-[#5c898d] resize-none h-24"
            ></textarea>

            <div class="flex justify-end gap-2">
            <button @click="showReportModal = false" class="border border-[#719294] text-[#719294] px-4 py-1.5 rounded-full text-sm hover:bg-[#e9e9e9] transition-colors">
                Cancel
            </button>
            <button @click="submitReport" class="bg-[#719294] text-white px-4 py-1.5 rounded-full text-sm hover:brightness-110 transition-all">
                Submit
            </button>
            </div>
        </div>
        <div class="flex items-center gap-[2px]">
        <button 
            @click="toggleHelpful"
            class="flex items-center gap-1 text-sm transition-colors"
            :class="hasVoted ? 'text-[#5c898d]' : 'text-[#719294] hover:text-[#5c898d]'"
        >
            <svg 
                :fill="hasVoted ? '#5c898d' : 'none'"
                :stroke="hasVoted ? '#5c898d' : '#719294'"
                class="h-[16px] w-[16px]"
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                >
                <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z" />
                <path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
            </svg>
            {{ helpfulCountLocal }}
        </button>
        <span class="text-sm text-[#719294]">found this helpful</span>
        </div>
    </div>


    <div 
    v-if="showReportModal" 
    class="fixed inset-0 flex items-center justify-center bg-black/30 z-20"
    >
    <div class="bg-white p-6 rounded-xl w-[320px] shadow-lg z-30 text-[#719294]" >
        <h2 class="text-lg font-bold mb-4 text-[#0B0D09]">Report Review</h2>

        <select v-model="reason" class="border border-[#719294] p-2 w-full mb-3 rounded-lg text-sm text-[#0B0D09] outline-none focus:border-[#5c898d]">
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
        placeholder="Additional details (optional)"
        class="border border-[#719294] p-2 w-full mb-4 rounded-lg text-sm text-[#0B0D09] placeholder:text-[#719294] outline-none focus:border-[#5c898d] resize-none h-24"
        ></textarea>

        <div class="flex justify-end gap-2">
        <button @click="showReportModal = false" class="border border-[#719294] text-[#719294] px-4 py-1.5 rounded-full text-sm hover:bg-[#e9e9e9] transition-colors">
            Cancel
        </button>
        <button @click="submitReport" class="bg-[#719294] text-white px-4 py-1.5 rounded-full text-sm hover:brightness-110 transition-all">
            Submit
        </button>
        </div>
    </div>
    </div>
</template>