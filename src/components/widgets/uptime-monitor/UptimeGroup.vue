<script setup lang="ts">
import { ChevronDown } from "@lucide/vue";
import { Separator } from "reka-ui";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { UptimeGroupData } from "@/lib/uptime-kuma/utils";
import { statusLabels } from "@/lib/uptime-kuma/utils";
import UptimeStatusDot from "./UptimeStatusDot.vue";
import UptimeHeartbeatBar from "./UptimeHeartbeatBar.vue";
import UptimeRate from "./UptimeRate.vue";
import UptimeMonitorItem from "./UptimeMonitorItem.vue";

defineProps<{ group: UptimeGroupData; defaultOpen?: boolean }>();
</script>

<template>
  <Collapsible
    v-slot="{ open }"
    :default-open="defaultOpen"
    class="rounded-[10px] bg-brown-700 px-2 py-2"
  >
    <CollapsibleTrigger as-child>
      <Button
        variant="link"
        type="button"
        :aria-label="`${group.name}：${statusLabels[group.status]}，${open ? '收合' : '展開'}監視器`"
        class="relative grid h-auto w-full gap-x-[19px] p-0 text-left font-normal hover:bg-transparent grid-cols-[minmax(0,96px)_minmax(0,1fr)_auto]"
      >
        <Tooltip>
          <TooltipTrigger as-child>
            <span class="flex min-w-0 items-center gap-1">
              <UptimeStatusDot :status="group.status" group />
              <span class="truncate text-base leading-[1.1] text-brown-300">{{
                group.name
              }}</span>
            </span>
          </TooltipTrigger>
          <TooltipContent
            >{{ group.name }}：{{ statusLabels[group.status] }}</TooltipContent
          >
        </Tooltip>
        <UptimeHeartbeatBar :heartbeats="group.heartbeats" />
        <UptimeRate :uptime="group.uptime" :status="group.status" badge />
        <ChevronDown
          aria-hidden="true"
          class="absolute top-2 -right-0.5 size-3 text-brown-600 transition-transform duration-200 motion-reduce:transition-none"
          :class="{ 'rotate-180': open }"
        />
      </Button>
    </CollapsibleTrigger>

    <CollapsibleContent>
      <div class="flex flex-col gap-2.5 pt-2.5 pb-1">
        <Separator decorative class="h-px bg-brown-600" />
        <ul v-if="group.monitors.length" class="flex flex-col gap-2.5">
          <UptimeMonitorItem
            v-for="monitor in group.monitors"
            :key="monitor.id"
            :monitor="monitor"
          />
        </ul>
        <p v-else class="text-sm text-brown-400">此群組沒有監視器。</p>
      </div>
    </CollapsibleContent>
  </Collapsible>
</template>
