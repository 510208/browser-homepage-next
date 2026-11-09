<script setup lang="ts">
import { computed } from "vue";
import type { UptimeStatus, UptimeSummaryData } from "@/lib/uptime-kuma/utils";
import { statusColors } from "@/lib/uptime-kuma/utils";
import UptimeStatusDot from "./UptimeStatusDot.vue";

const props = defineProps<{
  summary: UptimeSummaryData;
  loading: boolean;
  unavailable: boolean;
}>();

const titles: Record<UptimeStatus, string> = {
  up: "狀態正常",
  down: "服務異常",
  pending: "狀態待確認",
  maintenance: "服務維護中",
  unknown: "狀態未知",
};
const status = computed(() =>
  props.loading || props.unavailable ? "unknown" : props.summary.status,
);
const title = computed(() =>
  props.loading
    ? "載入中…"
    : props.unavailable
      ? "無法取得狀態"
      : titles[status.value],
);
</script>

<template>
  <header
    class="flex flex-col gap-2.5 bg-brown-700 p-6"
    role="status"
    aria-live="polite"
  >
    <div
      class="flex items-center gap-3"
      :style="{
        color:
          status === 'up'
            ? 'rgba(205, 244, 205, 0.9)'
            : statusColors[status].color,
      }"
    >
      <UptimeStatusDot :status="status" large />
      <p class="text-4xl font-bold">{{ title }}</p>
    </div>
    <p class="text-xl text-brown-400">
      <template v-if="!loading && !unavailable">
        {{ summary.total }} 監視器 / {{ summary.up }} 線上 /
        {{ summary.down }} 離線 / {{ summary.maintenance }} 維護<span
          v-if="summary.pending"
        >
          / {{ summary.pending }} 待確認</span
        ><span v-if="summary.unknown"> / {{ summary.unknown }} 未知</span>
      </template>
      <template v-else>{{
        loading ? "正在確認服務狀態" : "暫時無法確認服務狀態"
      }}</template>
    </p>
  </header>
</template>
