<script setup>
import Navbar from './Navbar.vue';
</script>

<template>
  <div class="main-container">

    <Navbar/>

    <!-- MAIN CONTENT -->
    <div class="flex flex-col items-center mt-[80px]">
        <!-- PROFFABLE LOGO + TITLE -->
      <div class="flex flex-col items-center mb-[40px]">
      <div class="flex items-center">
          <img src="../assets/ProffableLogo.png" class="h-[150px]" />
          <span class="text-[#505946] text-[100px] font-bold mb-[5px] ml-[-15px]">roffable</span>
      </div>
      
      <p class="text-[#0B0D09] text-2xl font-bold italic -mt-10 -mr-20">
        Choosing a professor made Proffable.
      </p>
    </div>

      <!-- SEARCH BAR -->
      <div class="w-[720px] relative mb-[-30px] z-10">
        <div class="flex items-center bg-white rounded-full shadow-md px-[24px] py-[18px]">

          <!-- Input -->
          <input
            type="text"
            placeholder="Search for a professor or course"
            class="flex-1 outline-none text-lg text-[#719294]"
          />

          <!-- Filter Button -->
          <button class="ml-[20px] font-medium text-[#0B0D09] flex items-center gap-[6px]">
            Filter
            <span>▾</span>
          </button>

        </div>
      </div>


      <!-- FILTER CARD -->
      <div class="w-[720px] bg-[#5c898d] rounded-[18px] pt-[60px] pb-[30px] px-[40px] shadow-lg">

        <!-- DROPDOWNS -->
        <div class="flex gap-[20px] mb-[40px]">

          <div class="flex-1">
            <select class="w-full px-[18px] py-[14px] rounded-[14px] bg-gray-100 text-[#719294]">
              <option>University</option>
            </select>
          </div>

          <div class="flex-1">
            <select class="w-full px-[18px] py-[14px] rounded-[14px] bg-gray-100 text-[#719294]">
              <option>Department</option>
            </select>
          </div>

        </div>



        <!-- STAR RATING -->
        <div class="flex justify-center gap-[10px] text-[40px] text-white mb-[10px]">
          ★ ★ ★ ★ ★
        </div>

        <p class="text-center text-white opacity-80 -mt-[20px]">
          Average Rating
        </p>

      </div>

    </div>

  </div>
</template>

<style scoped>
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

</style> 