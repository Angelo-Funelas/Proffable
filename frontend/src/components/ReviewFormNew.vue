<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import api from "@/api/axios"
import RatingSelector from './RatingSelector.vue'

const route = useRoute()
const message = ref('')
const isError = ref(false)

const emit = defineEmits(['submitReview']);

const form = ref({
  review_rating: '',
  comment_text: '',
  received_grade: ''
})
const handleRate = (value) => {
  form.value.review_rating = value;
};

// Call Backend for Review 
async function submitReview() {
  // TODO: FIX THIS SO THAT IT ACCURATELY CREATES A POST REQUEST TO THE API 
  console.log({
      professor: route.params.professorId,
      review_rating: form.value.review_rating,
      comment_text: form.value.comment_text,
      received_grade: form.value.received_grade
    })
  try {
    await api.post('reviews/', {
      professor: route.params.professorId,
      review_rating: form.value.review_rating,
      comment_text: form.value.comment_text,
      received_grade: form.value.received_grade
    })
    message.value = 'Review submitted successfully!'
    isError.value = false
    form.value = { review_rating: '', comment_text: '', received_grade: '' }
    emit('submitReview')
  } catch (err) {
    // REPLACE LATER WITH "something went wrong :(" FOR TESTING PURPOSES
    message.value = JSON.stringify(err.response?.data)
  }
}
</script>

<template>
    <form @submit.prevent="submitReview">
        <h1 class="text-2xl font-bold text-left my-2.5 mb-0">Write a Review</h1>
        <RatingSelector @rate="handleRate"/>
        <input type="text" v-model="form.received_grade" class="border-[#e9e9e9] border-2 rounded-xl my-2 p-2 text-[#719294] w-60" placeholder="Grade Received: e.g. A+, 92, 1.75">
        <textarea v-model="form.comment_text" class="border-[#e9e9e9] border-2 rounded-xl resize-none w-full text-[#719294] p-2" placeholder="What was good? What could be improved?"></textarea>
        <button type="submit" class="bg-[#52848A] rounded-full px-[18px] py-1 w-max cursor-pointer">
            Submit Review
        </button>
        <!-- Feedback -->
        <p
            v-if="message"
            class="text-sm text-center"
            :class="isError ? 'text-red-500' : 'text-green-600'"
        >
            {{ message }}
        </p>
    </form>
</template>