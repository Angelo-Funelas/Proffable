<template>
  <div class="main-container">
    
    <nav class="navbar">
      <div class="logo-circle">
        <img src="../assets/ProffableLogo.png" alt="Logo" class="logo-img" />
      </div>
    </nav>

    <div class="content-wrapper">
      <div class="login-card">
        
        <h1 class="welcome-text">
          Welcome to <span class="brand-subtext">Proffable</span>!
        </h1>

        <div class="input-group">
          <div class="input-row">
            <img src="../assets/EmailLogin.png" class="input-icon" alt="Email" />
            <input type="email" placeholder="Email" class="text-input" />
          </div>

          <div class="input-row">
            <img src="../assets/PasswordLogin.png" class="input-icon" alt="Password" />
            <input 
              :type="isPasswordVisible ? 'text' : 'password'" 
              placeholder="Password" 
              class="text-input" 
            />
            <button @click="togglePassword" type="button" class="toggle-btn">
              <img src="../assets/ShowPassword.png" class="toggle-icon" alt="Show" />
            </button>
          </div>
        </div>

        <div class="link-container">
          <a href="#" class="forgot-link">Forgot Password?</a>
        </div>

        <button class="signin-button">Sign In</button>

        <div class="divider">
          <span>or</span>
        </div>
        <button class="google-button" type="button">
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" class="google-icon" alt="Google" />
          Sign in with Google
        </button>

        <p class="signup-text">
          Don't have an account? 
          <a href="#" class="signup-link">Sign up</a>
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const isPasswordVisible = ref(false);
const togglePassword = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};
</script>

<style>
:global(#app) {
  max-width: none !important;
  width: 100vw !important;
  padding: 0 !important;
  margin: 0 !important;
}
:global(body) {
  margin: 0 !important;
  display: block !important;
}

.main-container {
  min-height: 100vh;
  width: 100%;
  background-color: #e9e9e9;
  display: flex;
  flex-direction: column;
}

.navbar {
  width: 100%;
  background-color: #5c898d;
  height: 4rem;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.logo-circle {
  background-color: #d9d9d9;
  border-radius: 9999px;
  height: 2.5rem;
  width: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-img {
  height: 1.75rem;
  width: 1.75rem;
  object-fit: contain;
}

.content-wrapper {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.login-card {
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.welcome-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #505946;
  margin-bottom: 2.5rem;
}

.brand-subtext { color: #6b7280; }

.input-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #9ca3af;
  padding: 0.25rem 0;
}

.input-icon {
  height: 1.25rem;
  width: 1.25rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.text-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #374151;
  font-size: 0.875rem;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 0.25rem;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.toggle-icon {
  height: 1.25rem;
  width: auto;
  object-fit: contain;
  opacity: 0.6;
}

.link-container {
  width: 100%;
  text-align: left;
  margin-top: 0.5rem;
}

.forgot-link {
  font-size: 10px;
  color: #60a5fa;
  text-decoration: none;
}

.signin-button {
  margin-top: 3rem;
  width: 100%;
  max-width: 200px;
  padding: 0.6rem 0;
  background-color: #5c898d;
  color: white;
  border-radius: 9999px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: filter 0.2s;
}

.signin-button:hover { filter: brightness(1.1); }

.divider {
  width: 100%;
  text-align: center;
  border-bottom: 1px solid #d1d5db;
  line-height: 0.1em;
  margin: 2rem 0;
}

.divider span {
  background: #e9e9e9;
  padding: 0 10px;
  color: #9ca3af;
  font-size: 12px;
}
/* https://developers.google.com/identity/branding-guidelines */
.google-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 0.6rem 0;
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.google-button:hover {
  background-color: #f9fafb;
}

.google-icon {
  height: 18px;
  width: 18px;
}

.signup-text { margin-top: 1.5rem; font-size: 11px; color: #4b5563; }
.signup-link { color: #5c898d; font-weight: 700; text-decoration: none; }
</style>