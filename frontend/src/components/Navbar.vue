<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

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
  <nav class="w-full bg-gradient-to-b from-[#719294] to-[#52848A] h-16 flex items-center justify-between px-6 shadow-md">

    <div
      @click="goToHomePage"
      class="bg-[#d9d9d9] rounded-full h-10 w-10 flex items-center justify-center overflow-hidden shadow-sm cursor-pointer"
    >
      <img src="../assets/ProffableLogo.png" alt="Logo" class="h-7 w-7 object-contain pointer-events-none" />
    </div>

    <button
      v-if="isAuthenticated"
      @click="logout"
      class="text-white font-semibold hover:opacity-80 transition"
    >
      Logout
    </button>

    <button
      v-else
      @click="goToLogin"
      class="text-white font-semibold hover:opacity-80 transition"
    >
      Login
    </button>

  </nav>
</template>