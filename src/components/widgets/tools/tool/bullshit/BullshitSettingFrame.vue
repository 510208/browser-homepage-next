<template>
  <div :class="cn('flex flex-col gap-1 p-3', props.class)">
    <Label class="text-xs font-medium tracking-widest text-brown-400" :for="props.name">{{
      props.title
    }}</Label>
    <div class="flex gap-1">
      <Input
        v-model="value"
        :id="props.name"
        class="w-full flex-1 border-[#5C3A29] bg-[#382014] text-[#EAD0C3] focus-visible:ring-[#0d99ff]"
        @update:modelValue="emit('update:modelValue', $event.toString())"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils.ts";

const props = defineProps<{
  title: string;
  modelValue: string;
  name: string;
  class?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const value = ref(props.modelValue);
</script>
