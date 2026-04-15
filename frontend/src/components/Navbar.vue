<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import LogoIcon from './LogoIcon.vue'
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
  <nav class="w-full bg-white h-16 flex items-center justify-between px-8 shadow-md border-b border-gray-100 relative z-50">
    
    <div @click="goToHomePage" class="flex items-center cursor-pointer group select-none">
      <LogoIcon class="h-10 transition-transform group-hover:scale-105 pointer-events-none"/>
      <span class="text-primary font-bold text-xl tracking-tighter">roffable</span>
    </div>

    <div v-if="isAuthenticated" class="relative">
      <div
        @click="toggleDropdown"
        class="flex items-center gap-3 cursor-pointer text-text-main hover:bg-surface px-3 py-1.5 rounded-full transition-colors select-none"
      >
        <img
          v-if="user?.profile_picture_url"
          :src="user.profile_picture_url"
          class="h-8 w-8 rounded-full object-cover border border-gray-200 pointer-events-none"
        />
        <div
          v-else
          class="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold pointer-events-none"
        >
          {{ user?.f_name?.[0]?.toUpperCase() || "U" }}
        </div>

        <span class="font-bold text-sm hidden md:block pointer-events-none">
          Hi, {{ user?.f_name || "User" }}
        </span>

        <span class="text-[10px] text-text-muted transition-transform pointer-events-none" :class="{'rotate-180': dropdownOpen}">▼</span>
      </div>

      <transition name="fade">
        <div
          v-if="dropdownOpen"
          class="absolute right-0 mt-3 w-48 bg-card rounded-xl shadow-xl border border-gray-100 py-2 overflow-hidden z-[60]"
        >
          <div class="px-4 py-2 border-b border-gray-50 mb-1">
            <p class="text-[10px] font-bold text-text-muted uppercase">Account</p>
          </div>
          
          <button
            @click="goToProfile"
            type="button"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm font-medium text-text-main hover:bg-surface hover:text-primary transition-all cursor-pointer !pointer-events-auto active:scale-[0.98] border-none outline-none"
          >
             Profile
          </button>

          <button
            @click="logout"
            type="button"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm font-medium text-red-500 hover:bg-red-50 transition-all cursor-pointer !pointer-events-auto active:scale-[0.98] border-none outline-none"
          >
             Logout
          </button>
        </div>
      </transition>
    </div>

    <button
      v-else
      @click="goToLogin"
      type="button"
      class="bg-accent hover:brightness-110 hover:scale-105 text-white font-bold px-6 py-2 rounded-full text-sm shadow-md transition-all active:scale-95 cursor-pointer !pointer-events-auto"
    >
      Login
    </button>

  </nav>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>