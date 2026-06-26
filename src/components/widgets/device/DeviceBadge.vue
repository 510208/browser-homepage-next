<template>
  <TooltipProvider>
    <Tooltip>
      <TooltipTrigger class="flex items-center justify-start gap-2.5 p-2.5 pb-0">
        <slot :class="iconClass" />
      </TooltipTrigger>
      <TooltipContent>
        <slot name="content" />
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</template>

<script lang="ts" setup>
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

defineProps<{
  iconClass: string;
}>();
</script>
