<template>
  <div
    class="mx-auto w-full max-w-2xl overflow-hidden rounded-xl border bg-popover text-popover-foreground shadow-md"
  >
    <div class="flex items-center border-b px-3">
      <SearchIcon class="mr-2 size-5 shrink-0 opacity-70" />
      <input
        type="text"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @keydown.down.prevent="$emit('keydown:down')"
        @keydown.up.prevent="$emit('keydown:up')"
        @keydown.enter.prevent="$emit('keydown:enter')"
        class="flex h-11 w-full rounded-md bg-transparent py-3 text-base outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
      />
    </div>

    <div class="max-h-[300px] overflow-y-auto">
      <div
        v-if="loading && suggestions.length === 0"
        class="p-2 py-6 text-center text-sm text-muted-foreground"
      >
        <slot name="loading">等等...還在搜尋中！</slot>
      </div>

      <div v-if="suggestions.length > 0" class="p-2">
        <div class="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
          {{ groupHeading }}
        </div>
        <ul class="mt-1 space-y-1">
          <li
            v-for="(suggestion, index) in suggestions"
            :key="`${suggestion}-${index}`"
            :data-highlighted="highlightedIndex === index"
            :class="[
              'flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors duration-75',
              highlightedIndex === index
                ? 'bg-accent font-medium text-accent-foreground '
                : 'text-foreground hover:bg-accent/50',
            ]"
            @mouseenter="$emit('update:highlightedIndex', index)"
            @click="$emit('select', suggestion)"
          >
            <slot name="item-icon">
              <ArrowRightIcon class="sh-arrow-animate h-4 w-4 shrink-0 opacity-70" />
            </slot>
            <span>{{ suggestion }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowRightIcon, SearchIcon } from "@lucide/vue";

withDefaults(
  defineProps<{
    modelValue: string; // 綁定輸入框的值
    suggestions: string[]; // 外部傳入的建議陣列
    highlightedIndex: number; // 當前鍵盤高亮的索引
    loading?: boolean; // 是否正在搜尋中
    placeholder?: string; // 輸入框提示字
    groupHeading?: string; // 分組標題
  }>(),
  {
    loading: false,
    placeholder: "搜尋你想搜的...",
    groupHeading: "搜尋建議",
  },
);

defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "update:highlightedIndex", index: number): void;
  (e: "select", suggestion: string): void;
  (e: "keydown:down"): void;
  (e: "keydown:up"): void;
  (e: "keydown:enter"): void;
}>();
</script>

<style scoped>
/* 當滑鼠 hover 到 li，或者 li 具備鍵盤高亮屬性時，對內部的 sh-arrow-animate 觸發動畫 */
li:hover .sh-arrow-animate,
li[data-highlighted="true"] .sh-arrow-animate {
  animation: shakeX 0.6s ease-in-out infinite;
}

@keyframes shakeX {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-2px);
  }
  75% {
    transform: translateX(3px);
  }
}
</style>
