<template>
  <div class="flex w-full cursor-pointer justify-center">
    <Dialog>
      <DialogTrigger as-child>
        <div class="flex h-12 w-12 items-center justify-center">
          <Tooltip>
            <TooltipTrigger as-child class="cursor-pointer">
              <slot />
            </TooltipTrigger>
            <TooltipContent
              side="right"
              class="flex max-w-xs items-center justify-end gap-0.5 truncate"
            >
              <p>{{ props.name }}</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </DialogTrigger>

      <DialogContent as-child class="flex gap-0 border-none px-0 py-0" @close-auto-focus.prevent>
        <component :is="props.dialogContent" />
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import type { Component } from "vue";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { Dialog, DialogTrigger, DialogContent } from "@/components/ui/dialog";

const props = defineProps<{
  name: string;
  /** 自訂 Dialog 內容組件 */
  dialogContent: Component;
}>();
</script>