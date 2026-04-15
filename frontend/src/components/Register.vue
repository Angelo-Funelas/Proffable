<script setup>
import { ref } from 'vue'
import api from "@/api/axios" 
import { useRouter } from 'vue-router'
import Navbar from './Navbar.vue'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const f_name = ref('')
const l_name = ref('')

const message = ref('')
const errorMsg = ref('')
const isLoading = ref(false)

const handleRegister = async () => {
  message.value = ''
  errorMsg.value = ''
  isLoading.value = true

  try {
    await api.post('/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      f_name: f_name.value,
      l_name: l_name.value
    })
    message.value = 'Account created successfully! Redirecting...'
    setTimeout(() => { router.push('/login') }, 1500)
  } catch (err) {
    errorMsg.value = err.response?.data?.error || 'Registration failed.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-surface font-sans relative overflow-x-hidden">
    <Navbar/>

    <div class="flex-grow flex items-center justify-center p-6 pb-32 relative z-10">
      <div class="w-full max-w-[450px] bg-card p-10 rounded-[24px] shadow-xl border border-gray-100 flex flex-col items-center relative z-10">
        
        <div class="mb-8 flex flex-col items-center text-center">
            <h1 class="text-3xl font-bold text-text-main tracking-tight">
                Join Proffable<span class="text-primary">.</span>
            </h1>
            <p class="text-text-muted text-sm mt-2">Create your account to start reviewing</p>
        </div>

        <form @submit.prevent="handleRegister" class="w-full flex flex-col gap-5">
          
          <div class="flex flex-col gap-1.5">
            <label class="text-[10px] font-bold uppercase tracking-widest text-text-muted ml-1">Username</label>
            <input v-model="username" type="text" placeholder="jdoe24" required 
              class="w-full bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"/>
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-[10px] font-bold uppercase tracking-widest text-text-muted ml-1">Email Address</label>
            <input v-model="email" type="email" placeholder="john@university.edu" required 
              class="w-full bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"/>
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-[10px] font-bold uppercase tracking-widest text-text-muted ml-1">Password</label>
            <input v-model="password" type="password" placeholder="••••••••" required 
              class="w-full bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"/>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
                <label class="text-[10px] font-bold uppercase tracking-widest text-text-muted ml-1">First Name</label>
                <input v-model="f_name" type="text" placeholder="John" 
                  class="w-full bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"/>
            </div>
            <div class="flex flex-col gap-1.5">
                <label class="text-[10px] font-bold uppercase tracking-widest text-text-muted ml-1">Last Name</label>
                <input v-model="l_name" type="text" placeholder="Doe" 
                  class="w-full bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"/>
            </div>
          </div>

          <div v-if="errorMsg" class="bg-red-50 text-red-600 text-xs p-3 rounded-lg text-center font-bold">
            {{ errorMsg }}
          </div>
          <div v-if="message" class="bg-green-50 text-green-600 text-xs p-3 rounded-lg text-center font-bold">
            {{ message }}
          </div>

          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full mt-2 py-3.5 bg-primary text-white rounded-full font-bold shadow-lg transition-all hover:brightness-110 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed text-sm cursor-pointer"
          >
            {{ isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <p class="mt-8 text-xs text-text-main">
          Already have an account? 
          <router-link to="/login" class="text-primary font-bold no-underline hover:underline ml-1">
            Log In 
          </router-link>
        </p> 
      </div>
    </div>

    <div class="fixed bottom-0 left-0 w-full opacity-20 grid grid-rows-1 grid-cols-29 items-end pointer-events-none z-0">
        <img src="/ateneo.png" class="row-1 col-start-1 col-span-8">
        <img src="/ust.png" class="row-1 col-start-8 col-span-8">
        <img src="/up.png" class="row-1 col-start-15 col-span-8">
        <img src="/dlsu.png" class="row-1 col-start-22 col-span-8">
    </div>
  </div>
</template>