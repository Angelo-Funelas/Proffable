<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from "@/api/axios"
import RatingSelector from './RatingSelector.vue'

const props = defineProps({
  reviewId: Number,
  editing: Boolean,
  review_rating: Number,
  grade_received: String,
  comment_text: String,
})

const route = useRoute()
const message = ref('')
const isError = ref(false)
const tags = ref([])

const emit = defineEmits(['submitReview', 'cancelReview']);

const form = ref({
  review_rating: props.review_rating,
  comment_text: props.comment_text,
  received_grade: props.grade_received,
  tags: [],
})
const handleRate = (value) => {
  form.value.review_rating = value;
};

onMounted(async () => {
  try {
    const [tagRes] = await Promise.all([
      api.get('tags/'),
    ])
    tags.value = tagRes.data
    console.log(tags.value)
  } catch (err) {
    console.error("Failed to load tags data", err)
  }
})

const toLetterGrade = (input) => {
  const n = parseFloat(input)
  if (isNaN(n)) return input
  if (n >= 90) return 'A'
  if (n >= 80) return 'B'
  if (n >= 70) return 'C'
  if (n >= 60) return 'D'
  return 'F'
}

async function submitReview() {
  const normalizedGrade = toLetterGrade(form.value.received_grade)
  try {
    if (props.editing) {
      await api.put(`reviews/${props.reviewId}/`, {
        professor: route.params.professorId,
        review_rating: form.value.review_rating,
        comment_text: form.value.comment_text,
        received_grade: normalizedGrade,
        tags: form.value.tags,
      })
      message.value = 'Edited Review!'
    } else {
      await api.post('reviews/', {
        professor: route.params.professorId,
        review_rating: form.value.review_rating,
        comment_text: form.value.comment_text,
        received_grade: normalizedGrade,
        tags: form.value.tags,
      })
      message.value = 'Submitted Review!'
    }
    isError.value = false
    emit('submitReview', form.value.review_rating, form.value.received_grade, form.value.comment_text)
    form.value = { review_rating: '', comment_text: '', received_grade: '', tags:[] }
  } catch (err) {
    // REPLACE LATER WITH "something went wrong :(" FOR TESTING PURPOSES
    message.value = JSON.stringify(err.response?.data)
  }
}

function toggleTag(id) {
  if (form.value.tags.includes(id)) {
    form.value.tags = form.value.tags.filter(x => x !== id)
  } else {
    form.value.tags.push(id)
  }
}

</script>

<template>
    <form @submit.prevent="submitReview">
        <h1 class="text-2xl font-bold text-left my-2.5 mb-0" v-if="!editing">Write a Review</h1>
        <RatingSelector @rate="handleRate" :rating="review_rating"/>
        <input maxlength="12" type="text" v-model="form.received_grade" class="border-[#e9e9e9] border-2 rounded-xl my-2 p-2 text-[#719294] w-60" placeholder="Grade Received: e.g. A+, 92, 1.75">
        <textarea v-model="form.comment_text" class="border-[#e9e9e9] border-2 rounded-xl resize-none w-full text-[#719294] p-2" placeholder="What was good? What could be improved?"></textarea>
        <div class="flex flex-wrap gap-2 my-2.5">
          <h1 class="text-xl text-left font-bold" v-if="!editing">Tags: </h1>
          <div 
            v-for="t in tags" 
            :key="t.tag_id"
            @click="toggleTag(t.tag_id)"
            :class="form.tags.includes(t.tag_id) ? 'bg-primary text-white px-2 py-1 rounded-full cursor-pointer' : 'bg-gray-200 text-[#719294] px-2 py-1 rounded-full cursor-pointer'"
          >
            {{ t.tag_name }}
          </div>
        </div>
        <button type="submit" class="bg-accent hover:bg-accent-hover text-white mx-1 rounded-full px-[18px] py-1 w-max cursor-pointer">
          <span v-if="!editing">Submit Review</span>  
          <span v-if="editing">Save</span>  
        </button>
        <button v-if="editing" @click="$emit('cancelReview')" type="button" class="bg-[#a2a2a2] text-white mx-1 rounded-full px-[18px] py-1 w-max cursor-pointer">
          Cancel
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