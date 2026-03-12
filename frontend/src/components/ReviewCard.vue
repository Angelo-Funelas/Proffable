<script setup>
import {ref} from 'vue'

const props = defineProps({
  semester: String,
  subject: String,
  reviewText: String,
  grade: String,
  rating: Number,
  tags: Array,
  likes: Number,
})

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
            <div class="flex align-middle gap-3">
                <button class="text-sm">
                    <img src="../assets/edit.svg" class="h-[24px]">
                </button>
                <button class="text-sm">
                    <img src="../assets/delete.svg" class="h-[24px]">
                </button>
                <button class="text-sm">
                    <img src="../assets/Flag.png" class="h-[24px]">
                </button>
            </div>
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
</template>