<template>
  <HoverCard>
    <HoverCardTrigger>
      <slot :class="iconClass ? iconClass : ''" />
    </HoverCardTrigger>
    <HoverCardContent>
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