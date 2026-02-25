<template> 

<div class="flex flex-col gap-2 text-left">
        <input class="rounded-2xl bg-[#FFFFFF] form_text mt-[5px] h-[35px] text-center " placeholder="Search for a professor or course"/>
        <!--QUERY/FILTERS DIV-->

        <!--NOTE: THE FUNCTIONS BELOW ARE OUT OF THE SCOPE IN CURRENT ITERATION AND ARE ONLY PLACEHOLDERS-->
        <div class="bg-[#52848A] rounded-xl p-[18px]  flex flex-col gap-2 text-left">
        <!-- University Dropdown -->
        <div class="relative">
            <select class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] form_text 
                appearance-none outline-none">
            <option disabled selected>University</option>
            </select>

            <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
        </div>
        <div class="grid grid-cols-1 gap-1 justify-center">
            <div class="flex justify-center">
                <img src="../assets/BigStar.svg" class="h-[48px]" />
                <img src="../assets/BigStar.svg" class="h-[48px]" />
                <img src="../assets/BigStar.svg" class="h-[48px]" />
                <img src="../assets/BigStar.svg" class="h-[48px]" />
                <img src="../assets/BigStar.svg" class="h-[48px]" />
            </div>
            <p class="text-center">Average Rating</p>
        </div>
        </div>

        <!-- <button class="bg-[#52848A] rounded-xl px-[18px] w-max justify-center mx-auto">
            Add a Professor
        </button> -->
        
    </div>
</template> 