<template>
  <TooltipProvider>
    <Tooltip>
      <TooltipTrigger>
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