<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RatingSelector from './RatingSelector.vue'

const router = useRouter()
const route = useRoute()

// Initialize with current query so the text doesn't disappear on refresh
const localQuery = ref(route.query.q || '')

let debounceTimer = null
const emit = defineEmits(['search'])

const handleInput = () => {
  clearTimeout(debounceTimer)
  
  debounceTimer = setTimeout(() => {
    const queryPayload = { q: localQuery.value || undefined }

    // If we are NOT on the list page, push to the list page with the query
    // Update '/professors' to match your actual list route path
    if (route.path !== '/professors') {
      router.push({ path: '/professors', query: queryPayload })
    } else {
      // If already there, just update the URL query
      router.push({ query: queryPayload })
    }
    
    emit('search', localQuery.value)
  }, 500)
}

// Sync the input if the URL query changes externally
watch(() => route.query.q, (newVal) => {
  localQuery.value = newVal || ''
})
</script>

<template> 
  <div class="flex flex-col gap-2 text-left">
    <input 
      v-model="localQuery"
      @input="handleInput"
      class="rounded-2xl bg-[#FFFFFF] form_text mt-[5px] h-[35px] px-3 text-[#719294] "
      placeholder="Search for a professor or course"
    />

    <div class="bg-[#52848A] rounded-xl p-[18px] flex flex-col gap-2 text-left">
      <div class="relative">
        <select class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] form_text appearance-none outline-none">
          <option disabled selected>University</option>
        </select>
        <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
      </div>
      <div class="text-center">
        <RatingSelector/>
        <p class="text-center">Average Rating</p>
      </div>
    </div>

    <button class="bg-[#52848A] rounded-full px-[18px] py-1 w-max justify-center mx-auto">
            Add a Professor
       </button>
  </div>
</template>