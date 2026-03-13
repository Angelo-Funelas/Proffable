<script setup>
import {ref} from 'vue'

const props = defineProps({
  reviewId: Number,
  semester: String,
  subject: String,
  reviewText: String,
  grade: String,
  rating: Number,
  tags: Array,
  likes: Number,
})

const showReportModal = ref(false)
const reason = ref("")
const description = ref("")

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

        <p class="italic flex items-center gap-[2px]"><img src="../assets/ThumbsUp.png" class="h-[16px] mr-[4px]"> {{ likes }} found this helpful</p>
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