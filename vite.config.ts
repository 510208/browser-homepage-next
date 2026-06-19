import { defineConfig } from "vite";

import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath, URL } from "node:url";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],

  resolve: {
    tsconfigPaths: true,

    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@assets": fileURLToPath(new URL("./src/assets", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components", import.meta.url)),
      "@styles": fileURLToPath(new URL("./src/styles", import.meta.url)),
    },
  },
});
