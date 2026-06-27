<template>
  <DeviceCard>
    <CpuIcon class="text-brown-500" :size="24" />

    <template #content>
      <span class="text-sm font-medium">
        {{ cpuUsage !== undefined ? cpuUsage.toFixed(2) : "N/A" }}%
      </span>
    </template>
  </DeviceCard>
</template>

<script setup lang="ts">
import DeviceCard from "../DeviceCard.vue";
import { CpuIcon } from "@lucide/vue";

const { cpuUsage } = defineProps<{
  cpuUsage: number | undefined;
}>();
</script>
