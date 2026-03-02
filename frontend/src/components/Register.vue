
<script setup>
import { ref } from 'vue'
import axios from 'axios' 

const API_URL = 'http://localhost:8000/api/'
const api = axios.create({
    baseURL:API_URL
})

const username = ref('')
const email = ref('')
const password = ref('')
const f_name = ref('')
const l_name = ref('')

const message = ref('')
const errorMsg = ref('')
const userInfo = ref(null)
import { useRouter } from 'vue-router'
import Navbar from './Navbar.vue'

const router = useRouter()

const handleRegister = async () => {
  message.value = ''
  errorMsg.value = ''

  try {
    await api.post('/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      f_name: f_name.value,
      l_name: l_name.value
    })

    message.value = 'Account created successfully! Redirecting to login...'

    // Clear form
    username.value = ''
    email.value = ''
    password.value = ''
    f_name.value = ''
    l_name.value = ''

    // Redirect after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (err) {
    if (err.response?.data?.error) {
      errorMsg.value = err.response.data.error
    } else {
      errorMsg.value = 'Registration failed.'
    }
  }
}
</script>

<template>

  <Navbar/> 
  
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 font-sans">
    <h1 class="text-2xl font-bold mb-6">Register New User</h1>

    <form @submit.prevent="handleRegister" class="flex flex-col gap-4 w-full max-w-sm bg-white p-6 rounded-lg shadow-md">
      <input type="text" placeholder="Username" v-model="username" required class="text-black input-field"/>
      <input type="email" placeholder="Email" v-model="email" required class="text-black input-field"/>
      <input type="password" placeholder="Password" v-model="password" required class="text-black input-field"/>
      <input type="text" placeholder="First Name" v-model="f_name" class="text-black input-field"/>
      <input type="text" placeholder="Last Name" v-model="l_name" class="text-black input-field"/>
      <button type="submit" class="btn">Register & Login</button>
    </form>

    <p v-if="message" class="mt-4 text-green-600 font-semibold">{{ message }}</p>
    <p v-if="errorMsg" class="mt-4 text-red-600 font-semibold">{{ errorMsg }}</p>

    <div v-if="userInfo" class="mt-6 bg-white p-4 rounded-lg shadow-md w-full max-w-sm">
      <h2 class="font-bold mb-2">Logged in as:</h2>
      <p><strong>Email:</strong> {{ userInfo.email }}</p>
      <p><strong>First Name:</strong> {{ userInfo.f_name }}</p>
      <p><strong>Last Name:</strong> {{ userInfo.l_name }}</p>
      <p><strong>Is Moderator:</strong> {{ userInfo.is_moderator }}</p>
    </div>
  </div>
</template>

<style>
.input-field {
  border: 1px solid #ccc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  outline: none;
  transition: border-color 0.2s;
}
.input-field:focus {
  border-color: #5c898d;
}
.btn {
  background-color: #5c898d;
  color: white;
  padding: 0.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s, transform 0.1s;
}
.btn:hover { background-color: #4e7171; }
.btn:active { transform: scale(0.98); }
</style>