<template>
  <Popover>
    <PopoverTrigger as-child>
      <slot />
    </PopoverTrigger>

    <PopoverContent
      class="w-auto border p-0 shadow-xl"
      side="bottom"
      :side-offset="8"
      @close-auto-focus.prevent
    >
      <ColorPickerRoot v-model="model" class="flex w-[200px] flex-col gap-2.5">
        <ColorPickerCanvas class="h-[150px] w-full rounded-lg" />
        <ColorPickerSliderHue class="h-3 w-full rounded-md" />
        <ColorPickerSliderAlpha class="h-3 w-full rounded-md" />
        <ColorPickerInputHex class="w-full text-center text-sm text-brown-100 focus:ring-1" />
      </ColorPickerRoot>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import {
  ColorPickerRoot,
  ColorPickerCanvas,
  ColorPickerSliderHue,
  ColorPickerSliderAlpha,
  ColorPickerInputHex,
} from "@vuelor/picker";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

// v-model 雙向綁定色碼，預設黑色
const model = defineModel<string>({ default: "#000000" });
</script>
