import { defineConfig, type PluginOption } from "vite";

import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import { visualizer } from "rollup-plugin-visualizer";

import { fileURLToPath, URL } from "node:url";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    visualizer({
      open: true, // 打包完自動打開瀏覽器看分析圖
      filename: "stats.html", // 產出的分析檔名
      gzipSize: true, // 顯示 gzip 後的大小，更貼近實際網路傳輸
      brotliSize: true,
    }) as PluginOption,
  ],

  resolve: {
    tsconfigPaths: true,

    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@assets": fileURLToPath(new URL("./src/assets", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components", import.meta.url)),
      "@styles": fileURLToPath(new URL("./src/styles", import.meta.url)),
    },
  },

  build: {
    rolldownOptions: {
      output: {
        manualChunks(id) {
          // 如果偵測到節點來自 opencc，就單獨打包成一個叫 opencc 的檔案
          if (id.includes("node_modules/opencc-js") || id.includes("opencc")) {
            return "opencc-vendor";
          }
        },
      },
    },
  },
});
