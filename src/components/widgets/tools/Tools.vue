<template>
  <div :class="cn('flex w-[50px] flex-col items-center gap-2.5 p-0', props.style)">
    <TooltipProvider>
      <ToolItem
        v-for="(tool, index) in tools"
        :key="index"
        :name="tool.name"
        :dialogContent="tool.dialogContent"
      >
        <component :is="tool.icon" class="h-6 w-6 text-brown-400" />
      </ToolItem>

      <div class="flex h-12 w-12 items-center justify-center">
        <Tooltip>
          <TooltipTrigger as-child class="cursor-pointer">
            <a href="https://it-tools.tech">
              <Toolbox class="h-6 w-6 text-brown-400" />
            </a>
          </TooltipTrigger>
          <TooltipContent
            side="right"
            class="flex max-w-xs items-center justify-end gap-0.5 truncate"
          >
            <p>IT Tools</p>
          </TooltipContent>
        </Tooltip>
      </div>
    </TooltipProvider>
  </div>
</template>

<script setup lang="ts">
import { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils.ts";
import ToolItem from "./ToolItem.vue";
import { Languages, Palette, Pilcrow, Toolbox } from "@lucide/vue";
import { defineAsyncComponent } from "vue";

const TranslateDialog = defineAsyncComponent(() => import("./tool/translate/TranslateDialog.vue"));
const ColorDialog = defineAsyncComponent(() => import("./tool/color/ColorDialog.vue"));
const BullshitDialog = defineAsyncComponent(() => import("./tool/bullshit/BullshitDialog.vue"));

const props = defineProps<{
  style?: Record<string, string>;
}>();

const tools = [
  { name: "翻譯", icon: Languages, dialogContent: TranslateDialog },
  { name: "色碼轉換器", icon: Palette, dialogContent: ColorDialog },
  { name: "廢話產生器", icon: Pilcrow, dialogContent: BullshitDialog },
];
</script>