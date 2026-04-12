<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from "@/api/axios"


const router = useRouter()

const isAuthenticated = ref(false)
const user = ref(null)
const dropdownOpen = ref(false)

const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
}

onMounted(() => {
  checkAuth()
  if (isAuthenticated.value) {
    fetchUser()
  }
})

const fetchUser = async () => {
  try {
    const res = await api.get("me/")
    user.value = res.data
  } catch(err) {
    console.error(err)
  }
}

const goToHomePage = () => {
  router.push('/')
}

const goToLogin = () => {
  router.push({ 
    path: '/login', 
    query: { next: router.currentRoute.value.fullPath } 
  })
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const goToProfile = () => {
  router.push("/profile")
  dropdownOpen.value = false
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isAuthenticated.value = false
  router.push('/')
}
</script>

<template>
  <nav class="w-full bg-white h-16 flex items-center justify-between px-6 shadow-lg">

    <div
      @click="goToHomePage"
      class="bg-[#d9d9d9] rounded-full h-10 w-10 flex items-center justify-center overflow-hidden shadow-sm cursor-pointer"
    >
      <img src="../assets/ProffableLogo.png" alt="Logo" class="h-7 w-7 object-contain pointer-events-none" />
    </div>


    <div v-if="isAuthenticated" class="relative">
      <div
        @click="toggleDropdown"
        class="flex items-center gap-2 cursor-pointer text-white font-semibold"
      >
        <img
          v-if="user?.profile_picture_url"
          :src="user.profile_picture_url"
          class="h-8 w-8 rounded-full object-cover"
        />

        <div
          v-else
          class="h-8 w-8 rounded-full bg-[#d9d9d9] flex items-center justify-center text-sm text-black"
        >
          {{ user?.f_name?.[0] || "U" }}
        </div>

        <span>
          Welcome, {{ user?.f_name || "User" }}!
        </span>

        <span>▼</span>
      </div>

      <div
        v-if="dropdownOpen"
        class="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-md text-black"
      >
        <button
          @click="goToProfile"
          class="block w-full text-left px-4 py-2 hover:bg-gray-100"
        >
          Profile
        </button>

        <button
          @click="logout"
          class="block w-full text-left px-4 py-2 hover:bg-gray-100"
        >
          Logout
        </button>
      </div>
    </div>

    <button
      v-else
      @click="goToLogin"
      class="font-semibold hover:opacity-80 transition"
    >
      Login
    </button>

  </nav>
</template>