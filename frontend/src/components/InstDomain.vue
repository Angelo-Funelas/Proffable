<script setup>
    import { ref } from 'vue'
    import { useFloating, offset, flip, shift } from '@floating-ui/vue'
    import { onClickOutside } from '@vueuse/core'
    import api from "@/api/axios"

    const props = defineProps({
        domain: String,
        id: Number
    })

    const reference = ref(null)
    const floating = ref(null)
    const showModal = ref(false)

    onClickOutside(floating, () => (showModal.value = false))
    const { floatingStyles } = useFloating(reference, floating, {
        placement: 'top', 
        middleware: [
            offset(10),
            flip(),
            shift()
        ],
    })

    const emit = defineEmits(['delete'])
    const handleDelete = async () => {
        try {
            await api.delete(`institution-domains/${props.id}/`);
            emit('delete');
            showModal.value = false;
        } catch (err) {
            console.error("Failed to delete domain:", err);
        }
    }
</script>

<template>
    <div class="group flex items-center justify-between bg-surface hover:bg-white p-3 rounded-xl border border-gray-50 transition-all hover:shadow-sm">
        <span class="text-sm font-medium text-text-main flex items-center gap-2">
            <span class="text-primary/40 text-[10px]">●</span>
            {{ domain }}
        </span>
        
        <button 
            @click="showModal = true" 
            ref="reference" 
            class="p-1.5 rounded-lg hover:bg-red-50 text-text-muted hover:text-red-500 transition-colors cursor-pointer"
        >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
        </button>
    </div>
    <div
        v-if="showModal"
        ref="floating"
        :style="floatingStyles"
        class="bg-white w-72 shadow-2xl p-5 rounded-2xl z-50 border border-gray-100 ring-1 ring-black/5"
    >
        <p class="mb-4 text-text-main text-sm font-semibold leading-tight">
            Delete this email domain?
        </p>
        <div class="flex gap-2">
            <button 
                @click="handleDelete" 
                class="flex-1 bg-red-500 text-white rounded-xl py-2 text-xs font-bold hover:bg-red-600 transition-colors cursor-pointer"
            >
                Yes, Delete
            </button>
            <button 
                @click="showModal = false" 
                class="flex-1 bg-surface text-text-muted rounded-xl py-2 text-xs font-bold hover:bg-gray-100 transition-colors cursor-pointer"
            >
                Cancel
            </button>
        </div>
    </div>
</template>