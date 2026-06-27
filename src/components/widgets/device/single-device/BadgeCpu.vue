<template>
  <DeviceCard>
    <!-- CPU -->
    <CpuIcon class="text-brown-500" :size="24" />

    <template #content>
      <div class="relative flex flex-col gap-0">
        <div class="bg-brown-700 px-5 py-6">
          <!-- 處理器資訊 -->
          <div class="flex flex-col items-start gap-2.5">
            <h2 class="text-3xl font-bold text-white">
              {{ cpuData?.overall_usage_percent?.toFixed(1) || "N/A" }}%
            </h2>
            <div class="flex flex-col gap-0.5">
              <p
                class="text-overflow-ellipsis overflow-hidden text-lg whitespace-nowrap text-brown-400"
              >
                {{ cpuData?.model || "未知的處理器" }}
              </p>
            </div>
          </div>
        </div>

        <div
          v-if="cpuData?.per_core_usage_percent && cpuData.per_core_usage_percent.length > 0"
          class="max-h-48 overflow-y-auto px-5 py-2.5"
        >
          <span class="mb-1.5 block text-base font-medium text-gray-400">核心負載狀態</span>
          <div class="grid grid-cols-2 gap-x-3 gap-y-1.5">
            <div
              v-for="(usage, index) in cpuData.per_core_usage_percent"
              :key="index"
              class="flex items-center justify-between text-base"
            >
              <span class="w-6 font-mono text-gray-500">C{{ index }}</span>
              <Progress :model-value="parseInt(usage.toFixed(0))" class="w-24" />
              <span class="w-8 text-right font-mono text-gray-400">{{ usage.toFixed(0) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DeviceCard>
</template>

<script setup lang="ts">
import type { CpuStatus } from "@/types/deviceDataResponse";
import DeviceCard from "../DeviceCard.vue";
import { CpuIcon } from "@lucide/vue";
import { Progress } from "@/components/ui/progress";

// 定義元件的 Props 屬性
const { cpuData } = defineProps<{
  cpuData: CpuStatus | undefined;
}>();
</script>