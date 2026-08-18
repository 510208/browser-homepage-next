<template>
  <Popover>
    <PopoverTrigger as-child>
      <slot />
    </PopoverTrigger>

    <PopoverContent
      class="w-auto border-[#5C3A29] bg-[#4A2D1F] p-0 shadow-xl"
      side="bottom"
      :side-offset="8"
      @close-auto-focus.prevent
    >
      <Suspense>
        <template #default>
          <AsyncVuelorPicker v-model="model" />
        </template>
        <template #fallback>
          <div class="flex h-[240px] w-[200px] items-center justify-center text-sm text-[#C29B88]">
            載入調色盤...
          </div>
        </template>
      </Suspense>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { defineAsyncComponent, h } from "vue";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

// v-model 雙向綁定色碼，預設黑色
const model = defineModel<string>({ default: "#000000" });

// 動態非同步載入 Vuelor 元件
const AsyncVuelorPicker = defineAsyncComponent({
  loader: async () => {
    const {
      ColorPickerRoot,
      ColorPickerCanvas,
      ColorPickerSliderHue,
      ColorPickerSliderAlpha,
      ColorPickerInputHex,
    } = await import("@vuelor/picker");

    return {
      setup() {
        return () =>
          h(
            ColorPickerRoot,
            {
              modelValue: model.value,
              // 將 val 宣告為 any 以兼顧 string / ColorObject / null 型別
              "onUpdate:modelValue": (val: any) => {
                if (typeof val === "string") {
                  model.value = val;
                } else if (val && typeof val === "object" && "hexa" in val) {
                  // 若傳回 ColorObject 則取其 hexa 屬性
                  model.value = val.hexa;
                }
              },
              class: "flex flex-col gap-2.5 w-[200px]",
            },
            () => [
              h(ColorPickerCanvas, { class: "h-[150px] w-full rounded-lg" }),
              h(ColorPickerSliderHue, { class: "h-3 w-full rounded-md" }),
              h(ColorPickerSliderAlpha, { class: "h-3 w-full rounded-md" }),
              h(ColorPickerInputHex, {
                class:
                  "w-full rounded-md border border-[#5C3A29] bg-[#382014] px-2 py-1 text-center text-sm text-[#EAD0C3] focus:outline-none focus:ring-1 focus:ring-[#0d99ff]",
              }),
            ],
          );
      },
    };
  },
});
</script>
