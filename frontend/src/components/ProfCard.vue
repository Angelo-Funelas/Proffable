<script setup>
import Heart from './Heart.vue';
import {ref} from 'vue'
const props = defineProps({
    lname: String,
    fname: String,
    avgScore: Number,
    tags: Array,
    numReviews: Number,
    favoriteCount: Number,
    is_favorited: Boolean,
    institutions: Array,
    showHeart: { type: Boolean, default: true }
})

</script>

<template>
    <div class="bg-card shadow-md border border-gray-100 rounded-xl p-[18px] flex justify-between items-start transition-all hover:border-primary/30">

        <div class="flex flex-col text-left text-text-main gap-1">
            <h3 class="text-lg font-bold text-primary">{{ fname }} {{ lname }}</h3>
            
            <p class="text-xs font-medium text-text-muted italic">
                {{ institutions?.[0]?.name || institutions?.[0] || 'Faculty Member' }}
            </p>

            <p class="text-sm flex items-center gap-1.5 text-text-main">
                <svg width="16" height="16" viewBox="0 0 40 38" class="fill-accent">
                    <path d="M20,0l6.2,12.5,13.8,2-10,9.7,2.4,13.8-12.4-6.5-12.4,6.5,2.4-13.8L0,14.5l13.8-2L20,0Z"/>
                </svg>
                <span class="font-bold">{{ Number(avgScore).toFixed(2) }}</span>
                <span class="text-text-muted text-xs">({{ numReviews }} reviews)</span>
            </p>

            <div class="text-[11px] flex flex-wrap gap-1 items-center mt-1">
                <span class="font-bold text-text-main">Tags:</span>
                <template v-if="tags && tags.length > 0">
                    <span v-for="tag in tags" :key="tag" 
                        class="bg-surface text-primary px-2 py-0.5 rounded-full border border-gray-100 font-bold">
                        {{ tag }}
                    </span>
                </template>
                <span v-else class="text-text-muted italic">None</span>
            </div>
        </div>

        <Heart :show="showHeart" :filled="is_favorited" :favorite_count="favoriteCount" class="scale-90" />
    </div>
</template>