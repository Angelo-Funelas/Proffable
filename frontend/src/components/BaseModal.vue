<script setup>
defineProps({
  show: Boolean,
  title: String
});

defineEmits(['close']);
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="show" class="modal-backdrop" @click.self="$emit('close')">
        <div class="modal-container" role="dialog" aria-modal="true">
          <header class="modal-header relative">
            <slot name="header">
                <h3 class="text-lg font-bold mb-4 text-[#0B0D09]">{{ title || 'Popup' }}</h3>
            </slot>
            <button class="close-btn absolute top-0 right-0" @click="$emit('close')"><img src="../assets/close.svg" class="h-6"></button>
          </header>

          <section class="modal-body">
            <slot />
          </section>

          <footer v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px); /* The blur you wanted */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  width: 90%;
  max-width: 500px;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Animation Logic */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>