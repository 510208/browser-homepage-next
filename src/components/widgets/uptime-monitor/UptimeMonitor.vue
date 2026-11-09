<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { ArrowRight, RefreshCw } from "@lucide/vue";
import { TooltipProvider } from "@/components/ui/tooltip";
import UptimeSummary from "./UptimeSummary.vue";
import UptimeGroup from "./UptimeGroup.vue";
import { useUptimeMonitor } from "./useUptimeMonitor";

defineProps<{
  statusPageUrl?: string;
}>();

const { groups, summary, isLoading, isRefreshing, error, updatedAt, refresh } =
  useUptimeMonitor();
</script>

<template>
  <section
    id="sh-uptime-monitor"
    aria-label="服務監控"
    :aria-busy="isRefreshing"
    class="flex w-[400px] max-w-full flex-col overflow-hidden rounded-md border border-brown-700 bg-brown-800"
  >
    <TooltipProvider :delay-duration="200">
      <UptimeSummary
        :summary="summary"
        :loading="isLoading"
        :unavailable="!!error && !updatedAt"
      />

      <div class="flex flex-col gap-2.5 px-5 pt-3.5 pb-5">
        <div class="flex items-center justify-between">
          <h2 class="text-xl leading-[1.1] font-bold text-white">概覽</h2>
          <Button
            v-if="statusPageUrl"
            variant="ghost"
            size="sm"
            as-child
            class="h-auto gap-2.5 px-2.5 py-1 text-xs leading-[1.1] font-normal text-brown-500"
          >
            <a :href="statusPageUrl" target="_blank" rel="noopener noreferrer">
              檢視更多
              <ArrowRight aria-hidden="true" class="size-3" />
            </a>
          </Button>
          <Button
            v-else
            variant="ghost"
            type="button"
            :disabled="isRefreshing"
            class="h-auto gap-2.5 px-2.5 py-1 leading-[1.1] font-normal text-brown-500 hover:text-brown-300"
            @click="refresh"
          >
            <RefreshCw
              aria-hidden="true"
              :class="{
                'animate-spin motion-reduce:animate-none': isRefreshing,
              }"
            />
            {{ isRefreshing ? "更新中…" : "重新整理" }}
          </Button>
        </div>

        <div
          v-if="error"
          role="alert"
          class="flex flex-col gap-2 text-sm text-brown-300 my-2"
        >
          <p>
            {{ error
            }}{{
              updatedAt ? "，目前顯示上次成功更新的資料。" : "，請稍後重試。"
            }}
          </p>
          <time
            v-if="updatedAt"
            :datetime="updatedAt.toISOString()"
            class="text-xs text-brown-400"
          >
            上次更新：{{ updatedAt.toLocaleString("zh-TW") }}
          </time>
          <Button
            variant="outline"
            size="sm"
            type="button"
            class="self-start"
            :disabled="isRefreshing"
            @click="refresh"
          >
            {{ isRefreshing ? "更新中…" : "重試" }}
          </Button>
        </div>

        <p v-if="isLoading" role="status" class="py-4 text-sm text-brown-400">
          正在取得監控資料…
        </p>
        <template v-else-if="groups.length">
          <UptimeGroup
            v-for="(group, index) in groups"
            :key="group.id"
            :group="group"
            :default-open="index === 0"
          />
        </template>
        <p v-else-if="!error" role="status" class="py-4 text-sm text-brown-400">
          目前沒有公開的監視器。
        </p>
      </div>
    </TooltipProvider>
  </section>
</template>
