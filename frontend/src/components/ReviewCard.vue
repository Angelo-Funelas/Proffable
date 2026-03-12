<script setup>
import {ref, watch} from 'vue'
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
                <button class="text-sm" v-if="isOwner" @click="isEditing = true">
                    <img src="../assets/edit.svg" class="h-[24px]">
                </button>
                <button class="text-sm" v-if="isOwner">
                    <img src="../assets/delete.svg" class="h-[24px]">
                </button>
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

            <p class="italic flex items-center gap-[2px]"><img src="../assets/ThumbsUp.png" class="h-[16px] mr-[4px]"> {{ review_data.likes }} found this helpful</p>
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