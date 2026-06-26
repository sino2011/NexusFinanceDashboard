import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  base: "/NexusFinanceDashboard/",
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    proxy: {
      "/login": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
      "/api": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
      "/home": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
      "/settings": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
      "/Transactions": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
      "/Reports": {
        target: "https://yassinafify.pythonanywhere.com",
        changeOrigin: true,
        secure: true,
      },
    },
  },
});
