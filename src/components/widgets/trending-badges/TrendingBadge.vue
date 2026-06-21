<template>
  <div class="flex items-center justify-start gap-2.5 p-2.5">
    <slot name="icon"></slot>
    <p class="text-base font-light text-brown-300">
      {{ props.data }}
    </p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  data?: string;
}>();
</script>