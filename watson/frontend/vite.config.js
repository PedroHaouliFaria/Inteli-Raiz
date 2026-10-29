import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  css: { preprocessorOptions: { scss: { api: 'modern-compiler', quietDeps: true } } },
  server: {
    proxy: {
      // Encaminha /api/* para o backend FastAPI em desenvolvimento.
      // O cookie SameSite=Lax funciona porque o browser vê uma única origem.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: false,
      },
    },
  },
});
