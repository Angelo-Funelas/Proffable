<script setup>
import { computed } from 'vue'

const props = defineProps({
    pages: { type: Number, default: 1 },
    currentPage: { type: Number, default: 1 },
})

const emit = defineEmits(['switchPage'])

const visiblePages = computed(() => {
    const total = props.pages;
    const current = props.currentPage;

    if (total <= 8) {
        return Array.from({ length: total }, (_, i) => i + 1);
    }

    let start = current - 3;
    let end = current + 2;

    if (start <= 1) {
        start = 2;
        end = 7;
    } 
    else if (end >= total) {
        end = total - 1;
        start = total - 6;
    }

    const pagesArr = [1];
    for (let i = start; i <= end; i++) {
        pagesArr.push(i);
    }
    pagesArr.push(total);

    return pagesArr;
});
</script>

<template>
    <div class="flex justify-center items-center gap-6 my-6">
        <button 
            @click="emit('switchPage', Math.max(1, currentPage - 1))" 
            :disabled="currentPage === 1"
            class="bg-card w-8 h-8 shadow rounded-full cursor-pointer text-text-muted disabled:opacity-30 disabled:cursor-not-allowed transition-opacity"
        >
            &lt;
        </button>

        <ul class="flex gap-2 items-center">
            <template v-for="(page, index) in visiblePages" :key="page">
                <li v-if="index > 0 && page - visiblePages[index - 1] > 1" class="text-text-muted px-1">
                    ...
                </li>

                <li @click="emit('switchPage', page)">
                    <p class="flex items-center justify-center shadow rounded-full w-8 h-8 cursor-pointer transition-all"
                        :class="{ 
                            'bg-accent text-white font-bold scale-110': page === currentPage,
                            'bg-card text-text-muted hover:bg-slate-100': page !== currentPage,
                        }"
                    >
                        {{ page }}
                    </p>
                </li>
            </template>
        </ul>

        <button 
            @click="emit('switchPage', Math.min(pages, currentPage + 1))" 
            :disabled="currentPage === pages"
            class="bg-card w-8 h-8 shadow rounded-full cursor-pointer text-text-muted disabled:opacity-30 disabled:cursor-not-allowed transition-opacity"
        >
            &gt;
        </button>
    </div>
</template>