<template>
  <div
    class="flex w-full max-w-2xl flex-col flex-nowrap items-stretch gap-0 overflow-hidden rounded-2xl border border-brown-800 bg-brown-900"
  >
    <!-- 色彩預覽與調色盤 Trigger -->
    <ColorPickerPopover v-model="selectedColor">
      <div
        class="flex h-20 w-full cursor-pointer items-center justify-center transition-colors hover:bg-[#4A2D1F]"
        :style="{ backgroundColor: selectedColor }"
      >
        <span
          class="rounded bg-black/40 px-3 py-1 text-sm font-medium text-[#EAD0C3] backdrop-blur-sm"
        >
          {{ selectedColor }}
        </span>
      </div>
    </ColorPickerPopover>

    <!-- 色彩名稱顯示 -->
    <div class="flex flex-col gap-1 border-b border-[#4A2D1F] p-4">
      <span class="text-xs font-medium tracking-widest text-brown-400">色彩名稱</span>
      <div class="flex gap-1">
        <span class="text-lg font-semibold text-[#EAD0C3]">{{ colorName }}</span>
        <Button variant="ghost" size="icon-sm" @click="handleCopy"><Copy /></Button>
      </div>
    </div>

    <!-- 各類色彩格式輸入與顯示區 -->
    <div class="grid grid-cols-2 gap-2 p-2">
      <ColorSettingFrame v-model="hexValue" title="HEX" />
      <ColorSettingFrame v-model="rgbValue" title="RGB" />
      <ColorSettingFrame v-model="hslValue" title="HSL" />
      <ColorSettingFrame v-model="labValue" title="LAB" />
      <ColorSettingFrame v-model="lchValue" title="LCH" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { ColorPickerPopover } from "@/components/ui/color-picker";
import ColorSettingFrame from "./ColorSettingFrame.vue";
import { Button } from "@/components/ui/button";
import { Copy } from "@lucide/vue";
import { toast } from "vue-sonner";

import { colord, extend } from "colord";
import labPlugin from "colord/plugins/lab";
import lchPlugin from "colord/plugins/lch";
import namesPlugin from "colord/plugins/names";

extend([labPlugin, lchPlugin, namesPlugin]);

const selectedColor = ref("#114514FF");

const colorName = computed(() => {
  const c = colord(selectedColor.value);
  return c.isValid() ? c.toName({ closest: true }) || "Unknown" : "Invalid Color";
});

const createColorComputed = (getter: (c: ReturnType<typeof colord>) => string) => {
  return computed({
    get: () => {
      const c = colord(selectedColor.value);
      return c.isValid() ? getter(c) : "";
    },
    set: (val: string) => {
      const newColor = colord(val);
      if (newColor.isValid()) {
        selectedColor.value = newColor.toHex();
      } else {
        // 輸入無效時，強制觸發重新渲染以還原正確數值
        selectedColor.value = `${selectedColor.value}`;
      }
    },
  });
};

const hexValue = createColorComputed((c) => c.toHex());
const rgbValue = createColorComputed((c) => c.toRgbString());
const hslValue = createColorComputed((c) => c.toHslString());
const labValue = createColorComputed((c) => {
  const lab = c.toLab();
  return `lab(${Math.round(lab.l)}% ${Math.round(lab.a)} ${Math.round(lab.b)})`;
});
const lchValue = createColorComputed((c) => c.toLchString());

function handleCopy() {
  navigator.clipboard.writeText(colorName.value).then(
    () => {
      console.log("Copied to clipboard:", colorName.value);
      toast.success("已複製到剪貼簿");
    },
    (err) => {
      console.error("Failed to copy text: ", err);
      toast.error("複製失敗");
    },
  );
}
</script>