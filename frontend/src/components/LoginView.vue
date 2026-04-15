<script setup>
  import { useRouter, useRoute } from 'vue-router'
  import { ref, onMounted } from 'vue';
  import Navbar from './Navbar.vue';

  const router = useRouter()
  const route = useRoute()
  const api = "http://127.0.0.1:8000/api";

  const isPasswordVisible = ref(false); 
  const loadingVisible = ref(false);
  const errorMsg = ref("");
  const successMsg = ref("");
  
  const login = ref("")
  const password = ref("")

  const togglePassword = () => { isPasswordVisible.value = !isPasswordVisible.value; };

  const handleLogin = async () => {
    loadingVisible.value = true;
    errorMsg.value = "";
    successMsg.value = "";

    try {
      const res = await fetch(`${api}/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          username: login.value, 
          password: password.value 
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        errorMsg.value = data.detail || "Invalid username or password.";
        return;
      }

      const data = await res.json();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      successMsg.value = "Welcome back!";
      
      setTimeout(() => {
          const nextPage = route.query.next || '/'
          router.push(nextPage)
      }, 500);

    } catch (err) {
      errorMsg.value = "Connection error. Please check your server.";
    } finally {
      loadingVisible.value = false;
    }
  };

  function handleCallbackResponse(response) {
    loadingVisible.value = true;
    errorMsg.value = "";
    
    const formData = new FormData();
    formData.append("token", response.credential);
    
    fetch(`${api}/google-login/`, {
      method: "POST",
      body: formData,
    })
    .then(async res => {
      if (!res.ok) throw new Error('Google authentication failed.');
      return res.json();
    })
    .then(data => {
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      router.push(route.query.next || '/')
    })
    .catch(err => {
      errorMsg.value = err.message;
    })
    .finally(() => {
      loadingVisible.value = false;
    });
  }

  onMounted(() => {
    if (window.google && window.google.accounts) {
      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        callback: handleCallbackResponse
      });
      
      window.google.accounts.id.renderButton(
        document.getElementById("googleSignInDiv"),
        { theme: "outline", size: "large", text: "continue_with", shape: "pill", width: "320" }
      );
    }
  })
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

<template>
  <div class="min-h-screen w-full flex flex-col font-sans bg-surface relative overflow-x-hidden">
    
    <Navbar/>

    <div class="flex-grow flex items-center justify-center p-6 pb-32 relative z-10">
      <div class="w-full max-w-[400px] bg-card p-10 rounded-3xl shadow-xl border border-gray-100 flex flex-col items-center">
        
        <div class="mb-8 flex flex-col items-center">
            <h1 class="text-3xl font-bold text-text-main text-center tracking-tight">
                Welcome back<span class="text-primary">!</span>
            </h1>
            <p class="text-text-muted text-sm mt-2">Sign in to your Proffable account</p>
        </div>

        <form @submit.prevent="handleLogin" class="w-full flex flex-col gap-6">
          
          <div class="flex flex-col gap-1.5">
            <label class="text-[11px] font-bold uppercase tracking-widest text-text-muted ml-1">Username or Email</label>
            <div class="flex items-center bg-surface border border-gray-100 rounded-xl px-4 py-3 focus-within:border-primary/50 transition-all">
                <svg class="h-5 w-5 mr-3 text-primary opacity-60 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <input
                  v-model="login" 
                  placeholder="Enter your login" 
                  required 
                  class="flex-grow bg-transparent outline-none text-text-main placeholder:text-text-muted/50 text-sm" 
                />
            </div>
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-[11px] font-bold uppercase tracking-widest text-text-muted ml-1">Password</label>
            <div class="flex items-center bg-surface border border-gray-100 rounded-xl px-4 py-3 focus-within:border-primary/50 transition-all">
                <svg class="h-5 w-5 mr-3 text-primary opacity-60 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <input 
                  v-model="password"
                  :type="isPasswordVisible ? 'text' : 'password'" 
                  placeholder="••••••••" 
                  required
                  class="flex-grow bg-transparent outline-none text-text-main placeholder:text-text-muted/50 text-sm" 
                />
                <button @click="togglePassword" type="button" class="shrink-0 ml-2 text-text-muted hover:text-primary transition-colors">
                  <svg v-if="!isPasswordVisible" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.076m1.903-1.903A9.952 9.952 0 0112 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3l18 18" />
                  </svg>
                </button>
            </div>
          </div>

          <transition name="fade">
            <div v-if="errorMsg" class="bg-red-50 text-red-600 text-xs p-3 rounded-lg text-center font-medium">{{ errorMsg }}</div>
          </transition>
          <div v-if="successMsg" class="bg-green-50 text-green-600 text-xs p-3 rounded-lg text-center font-medium">{{ successMsg }}</div>

          <div class="flex justify-center mt-2">
            <button 
              type="submit" 
              :disabled="loadingVisible"
              class="w-full py-3.5 bg-primary text-white rounded-full font-bold cursor-pointer border-none transition-all hover:brightness-110 active:scale-[0.98] shadow-lg disabled:opacity-60 disabled:cursor-not-allowed text-sm"
            >
              {{ loadingVisible ? 'Authenticating...' : 'Sign In' }}
            </button>
          </div>
        </form>

        <div class="w-full flex items-center my-8 before:flex-1 before:border-b before:border-gray-100 after:flex-1 after:border-b after:border-gray-100">
          <span class="px-4 text-[10px] font-bold uppercase tracking-widest text-text-muted">or</span>
        </div>

        <div id="googleSignInDiv" class="w-full flex justify-center"></div>

         <p class="mt-8 text-xs text-text-main">
          Don't have an account? 
          <router-link to="/sign-up" class="text-primary font-bold no-underline hover:underline ml-1">
            Sign Up 
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