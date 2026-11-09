<script setup lang="ts">
import type { CollapsibleContentProps } from "reka-ui";
import type { HTMLAttributes } from "vue";
import { reactiveOmit } from "@vueuse/core";
import { CollapsibleContent } from "reka-ui";
import { cn } from "@/lib/utils";

const props = defineProps<CollapsibleContentProps & { class?: HTMLAttributes["class"] }>();
const delegatedProps = reactiveOmit(props, "class");
</script>

<template>
  <CollapsibleContent
    data-slot="collapsible-content"
    v-bind="delegatedProps"
    :class="cn('sh-collapsible-content overflow-hidden', props.class)"
  >
    <slot />
  </CollapsibleContent>
</template>

<style scoped>
.sh-collapsible-content[data-state="open"] {
  animation: collapsible-down 200ms ease-out;
}

.sh-collapsible-content[data-state="closed"] {
  animation: collapsible-up 200ms ease-in;
}

@keyframes collapsible-down {
  from {
    height: 0;
    opacity: 0;
  }
  to {
    height: var(--reka-collapsible-content-height);
    opacity: 1;
  }
}

@keyframes collapsible-up {
  from {
    height: var(--reka-collapsible-content-height);
    opacity: 1;
  }
  to {
    height: 0;
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .sh-collapsible-content[data-state] {
    animation: none;
  }
}
</style>
