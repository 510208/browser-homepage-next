<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { computed, provide, ref } from "vue";
import { AvatarRoot } from "reka-ui";
import { cn } from "@/lib/utils";
import { avatarRingKey } from "./avatar-context";

const props = defineProps<{
  class?: HTMLAttributes["class"];
}>();

const ringCount = ref(0);
const hasRing = computed(() => ringCount.value > 0);

provide(avatarRingKey, ringCount);
</script>

<template>
  <AvatarRoot
    data-slot="avatar"
    :class="
      cn(
        'relative flex size-8 shrink-0 overflow-visible rounded-full',
        props.class,
      )
    "
  >
    <div
      :class="
        cn(
          'overflow-hidden rounded-full',
          hasRing ? 'absolute inset-[12.5%]' : 'size-full',
        )
      "
    >
      <slot />
    </div>
  </AvatarRoot>
</template>
