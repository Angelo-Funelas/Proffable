<script setup>
import {ref, onMounted} from 'vue'

const props = defineProps({
  reviewId: Number,
  semester: String,
  subject: String,
  reviewText: String,
  grade: String,
  rating: Number,
  tags: Array,
  likes: Number,
  isOwner:Boolean,
})  

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
                <!-- <span>Anonymous Student | {{ semester }} {{ subject }}</span> -->
            </div>
            <button class="text-sm" @click="showReportModal = true">
                <img src="../assets/Flag.png" class="h-[24px]">
            </button>    
        </div>
        <div class="flex">
            <div v-for="n in rating">
                <img src="../assets/BigStarFilled.svg" class="h-[36px]" />
            </div>
            <div v-for="n in 5-rating">
                <img src="../assets/BigStar.svg" class="h-[36px]" />
            </div>
        </div>
        
        <p class="text-xl"><span class="font-bold">Review</span>: {{ reviewText }}</p>
        <p class="text-sm"><span class="font-bold">Grade Received</span>: {{ grade }}</p>

        <div class="flex flex-wrap gap-2">
            <p class="text-sm"><span class="font-bold">Tags</span>:</p>
            <span v-for="(tag, index) in tags" :key="index" class="text-sm underline px-1">
                {{ tag }}
            </span>
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