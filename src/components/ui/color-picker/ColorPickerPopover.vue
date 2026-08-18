<template>
  <Popover>
    <PopoverTrigger as-child>
      <slot />
    </PopoverTrigger>

    <PopoverContent
      class="w-fit max-w-60 p-0 shadow-xl"
      side="bottom"
      :side-offset="8"
      @close-auto-focus.prevent
    >
      <ColorPickerRoot
        v-model="model"
        :ui="{ input: { label: 'hidden' } }"
        class="flex flex-col gap-2.5"
      >
        <!-- 色彩畫布 -->
        <ColorPickerCanvas :type="canvasType" class="h-[140px] w-full rounded-sm" />

        <!-- 滴管與滑桿區塊 -->
        <div class="flex items-center gap-2">
          <ColorPickerEyeDropper
            type="button"
            aria-label="Pick color from screen"
            class="flex size-10 shrink-0 items-center justify-center rounded-md bg-brown-700 text-brown-100 transition-colors hover:bg-brown-600 focus:ring-2 focus:ring-brown-400"
          >
            <Pipette :size="18" />
          </ColorPickerEyeDropper>

          <div class="flex flex-1 flex-col gap-3">
            <ColorPickerSliderHue class="h-3 w-full" />
            <ColorPickerSliderAlpha class="h-3 w-full" />
          </div>
        </div>

        <!-- 模式切換與輸入框區塊 -->
        <div class="flex items-center gap-1.5">
          <ColorPickerSelect
            v-model="format"
            class="w-16 shrink-0 text-brown-100"
            label="Color Format"
            placeholder="Format"
            :options="formatOptions"
          />
          <component
            :is="INPUTS[format]"
            class="w-full bg-brown-700 px-2 text-center text-white focus:ring-1 focus:ring-brown-400 focus:outline-none"
          />
        </div>
      </ColorPickerRoot>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import {
  ColorPickerRoot,
  ColorPickerCanvas,
  ColorPickerEyeDropper,
  ColorPickerSliderHue,
  ColorPickerSliderAlpha,
  ColorPickerInputHex,
  ColorPickerInputHSL,
  ColorPickerInputRGB,
  ColorPickerInputHSB,
} from "@vuelor/picker";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ColorPickerSelect } from "@/components/ui/color-picker";
import { Pipette } from "@lucide/vue";

// 雙向綁定色碼，預設為黑色
const model = defineModel<string>({ default: "#000000" });

// 色彩格式與動態輸入框映射
const INPUTS = {
  Hex: ColorPickerInputHex,
  RGB: ColorPickerInputRGB,
  HSL: ColorPickerInputHSL,
  HSB: ColorPickerInputHSB,
};

const format = ref<"Hex" | "RGB" | "HSL" | "HSB">("Hex");
const formatOptions = ["Hex", "RGB", "HSL", "HSB"];

// 根據當前選擇的色彩格式動態切換 Canvas 的顏色空間
const canvasType = computed<"HSL" | "HSV">(() => {
  return format.value === "HSL" ? "HSL" : "HSV";
});
</script>