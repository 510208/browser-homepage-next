<template>
  <HoverCard>
    <HoverCardTrigger>
      <slot :class="iconClass ? iconClass : ''" />
    </HoverCardTrigger>
    <HoverCardContent class="w-[400px] overflow-hidden px-0 py-0" align="end">
      <slot name="content" />
    </HoverCardContent>
  </HoverCard>
</template>

<script lang="ts" setup>
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";

defineProps<{
  iconClass?: string;
}>();
</script>
