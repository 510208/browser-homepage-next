<template>
  <div class="min-h-14">
    <HoverCard :open-delay="50" :close-delay="200">
      <HoverCardTrigger>
        <Avatar class="size-10">
          <AvatarImage
            src="https://gravatar.com/avatar/f7598bd8d4aba38d7219341f81a162fc842376b3b556b1995cbb97271d9e2915?v=1753291388000&size=50&d=initials"
            alt="@510208"
          />
          <AvatarFallback>SH</AvatarFallback>
          <AvatarBadge :class="ringColor" />
        </Avatar>
      </HoverCardTrigger>

      <HoverCardContent
        align="end"
        as-child
        class="mt-2 max-h-[calc(100dvh-80px)] w-[400px] max-w-[calc(100vw-24px)] overflow-y-auto border-0 p-0"
      >
        <UptimeMonitor />
      </HoverCardContent>
    </HoverCard>
  </div>
</template>

<script setup lang="ts">
import {
  Avatar,
  AvatarImage,
  AvatarFallback,
  AvatarBadge,
} from "@components/ui/avatar";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { UptimeMonitor } from "@/components/widgets/uptime-monitor";
import { useUptimeMonitor } from "../uptime-monitor/useUptimeMonitor";
import { computed, watch } from "vue";

const { summary } = useUptimeMonitor();

console.log("[Avatar] summary: ", summary.value);
const ringColor = computed(() => {
  const status = summary.value?.status;

  if (["up"].includes(status ?? "")) {
    return "bg-green-500";
  }

  if (["down", "unknown"].includes(status ?? "")) {
    return "bg-red-500";
  }

  if (["maintenance"].includes(status ?? "")) {
    return "bg-blue-500";
  }

  return "bg-yellow-500";
});

watch(
  summary,
  (value) => {
    console.log("[Avatar] summary updated:", value);
    console.log("[Avatar] ringColor:", ringColor.value);
  },
  { immediate: true },
);
</script>
