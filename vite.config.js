import { defineConfig } from 'vite';
// base './' so the build works under https://strategieonline.github.io/imobiliare_landing_page/
export default defineConfig({
  base: './',
  build: { outDir: 'dist', assetsInlineLimit: 0, chunkSizeWarningLimit: 1500 },
  server: { host: true }
});
