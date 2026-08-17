<template>
  <div :class="cn('flex w-[50px] flex-col items-center gap-2.5 p-0', props.style)">
    <TooltipProvider>
      <ToolItem
        v-for="(tool, index) in tools"
        :key="index"
        :name="tool.name"
        :dialogContent="tool.dialogContent"
      >
        <component :is="tool.icon" class="h-6 w-6 text-brown-400" />
      </ToolItem>
    </TooltipProvider>
  </div>
</template>

<script setup lang="ts">
import { TooltipProvider } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils.ts";
import ToolItem from "./ToolItem.vue";
import { Languages } from "@lucide/vue";

import TranslateDialog from "./tool/translate/TranslateDialog.vue";

const props = defineProps<{
  style?: Record<string, string>;
}>();

const tools = [{ name: "翻譯", icon: Languages, dialogContent: TranslateDialog }];
</script>
