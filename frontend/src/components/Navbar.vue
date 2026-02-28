<script setup>
import {useRouter} from 'vue-router';
const router = useRouter()

const goToHomePage = () => {
    router.push('/')
}

</script>

<template>
<nav class="w-full bg-gradient-to-b from-[#719294] to-[#52848A] h-16 flex items-center px-6 shadow-md">
      <div @click="goToHomePage" class="bg-[#d9d9d9] rounded-full h-10 w-10 flex 
      items-center justify-center overflow-hidden shadow-sm cursor-pointer">
        <img src="../assets/ProffableLogo.png" alt="Logo" class="h-7 w-7 object-contain 
        pointer-events-none"  />
      </div>
    </nav>

</template>