<template>
  <div class="min-h-screen w-full bg-[#e9e9e9] flex flex-col font-sans">
    
    <Navbar/>

    <div class="flex-grow flex items-center justify-center p-6">
      <div class="w-full max-w-[320px] flex flex-col items-center">
        
        <h1 class="text-2xl font-bold text-[#505946] mb-10 text-center">
          Welcome to <span class="text-gray-500">Proffable</span>!
        </h1>

        <form @submit.prevent="handleLogin" class="w-full flex flex-col gap-6">
          
          <div class="flex items-center border-b border-gray-400 py-2 focus-within:border-[#5c898d] transition-colors">
            <svg class="h-5 w-5 mr-3 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <input type="email" placeholder="Email" required class="flex-grow bg-transparent outline-none text-gray-700 text-sm border-none" />
          </div>

          <div class="flex items-center border-b border-gray-400 py-2 focus-within:border-[#5c898d] transition-colors">
            <svg class="h-5 w-5 mr-3 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <input 
              :type="isPasswordVisible ? 'text' : 'password'" 
              placeholder="Password" 
              required
              class="flex-grow bg-transparent outline-none text-gray-700 text-sm border-none" 
            />
            <button @click="togglePassword" type="button" class="shrink-0 p-1 flex items-center cursor-pointer border-none !bg-white rounded-md shadow-sm outline-none hover:!bg-gray-50 transition-colors">
              <svg v-if="!isPasswordVisible" class="h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.076m1.903-1.903A9.952 9.952 0 0112 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3l18 18" />
              </svg>
            </button>
          </div>

          <div class="flex justify-center">
            <button type="submit" class="mt-12 w-full max-w-[200px] py-2.5 !bg-[#5c898d] !text-white rounded-full font-semibold cursor-pointer border-none transition-all hover:brightness-110 active:scale-95 shadow-md">
              Sign In
            </button>
          </div>
        </form>

        <div class="w-full flex items-center my-8 before:flex-1 before:border-b before:border-gray-300 after:flex-1 after:border-b after:border-gray-300">
          <span class="px-3 text-xs text-gray-400">or</span>
        </div>

        <div id="googleSignInDiv" class="google-button">
        </div>

        <p class="mt-6 text-[11px] text-gray-600">
          Don't have an account? 
          <a href="#" class="text-[#5c898d] font-bold no-underline hover:underline">Sign up</a>
        </p>

      </div>
    </div>
  </div>
  <div v-if="loadingVisible" id="loading">Loading...</div>
  <div v-if="errorMsg" id="error">{{ errorMsg }}</div>
  <div v-if="successMsg" id="success">{{ successMsg }}</div>
  <div v-if="tokenData" id="tokenDisplay">{{ JSON.stringify(tokenData, null, 2) }}</div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import Navbar from './Navbar.vue';
  const isPasswordVisible = ref(false); 
  const togglePassword = () => { isPasswordVisible.value = !isPasswordVisible.value; };

  // Fix: This actually runs when the form submits now
  const handleLogin = () => {
    alert("Logging in...");
  };
  const api = "http://127.0.0.1:8000/api";

  const loadingVisible = ref(false);
  const errorMsg = ref("");
  const successMsg = ref("");
  const tokenData = ref(null);

  function handleCallbackResponse(response) {
    console.log("Response received:", response);
    
    // Show loading state
    loadingVisible.value = true;
    errorMsg.value = "";
    successMsg.value = "";
    
    // Prepare form data
    const formData = new FormData();
    formData.append("token", response.credential);
    
    // Send token to your Django API
    fetch(`${api}/google-login/`, {
      method: "POST",
      body: formData,
    })
    .then(res => {
      if (!res.ok) {
        throw new Error("Login failed. Please try again.");
      }
      return res.json();
    })
    .then(data => {
      console.log("Login successful:", data);
      
      // Display tokens in the div
      const tokenInfo = {
        tokens: data.tokens,
        full_response: data
      };

      successMsg.value = "Login successful!";
      tokenData.value = data;
    })
    .catch(err => {
      console.error("Login error:", err);
      errorMsg.value = "An unexpected error occurred.";
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
        { 
          theme: "outline", 
          size: "large",
          text: "sign_in_with",
          shape: "pill"
        }
      );
    } else {
      errorMsg.value = "Google script not loaded.";
    }
  })

</script>

<style>
/* Reset and Overrides */
#app { max-width: none !important; width: 100vw !important; padding: 0 !important; margin: 0 !important; }
body { margin: 0 !important; display: block !important; }
</style>