<script setup>
    import {ref, onMounted, watch, computed} from 'vue'
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
        await api.delete(`institution-domains/${props.id}/`);
        emit('delete');
        showModal.value = false;
    }
</script>

<template>
    <div class="grid bg-[#f2f2f2] p-2 grid-cols-[80%_20%] grid-rows-1">
        <span class="flex justify-start">{{ domain }}</span>
        <span class="flex justify-end"><img @click="showModal=true" ref="reference" src="../assets/delete.svg" class="h-[24px] cursor-pointer hover:scale-[1.1]"></span>
    </div>
    <div
        v-if="showModal"
        ref="floating"
        :style="floatingStyles"
        class="bg-white w-80 border-[#719294] border-2 shadow-xl p-4 rounded-md z-50"
    >
        <p class="mb-2 text-[#0B0D09] text-left">Are you sure you want to delete this email domain?</p>
        <div class="flex justify-end gap-2">
            <button @click="handleDelete" class="bg-red-600 text-white rounded-full px-4 py-1 text-sm">Yes, Delete</button>
            <button @click="showModal = false" class="bg-primary text-white rounded-full px-4 py-1 text-sm">Cancel</button>
        </div>
    </div>
</template>