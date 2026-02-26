import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    host: true,         // Allows access from outside the container
    port: 5173,
    watch: {
      usePolling: true, // Required for Docker on Windows/WSL to see file changes
    },
    hmr: {
      clientPort: 5173, // Ensures the browser connects to the right HMR port
    },
  },
})
