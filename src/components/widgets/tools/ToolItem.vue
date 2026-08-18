<template>
  <div class="flex w-full cursor-pointer justify-center">
    <!-- 若有傳入 dialogContent，則渲染 Dialog 結構 -->
    <Dialog>
      <DialogTrigger as-child>
        <div class="flex h-12 w-12 items-center justify-center focus-within:outline-0">
          <Tooltip>
            <TooltipTrigger as-child>
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

      <DialogContent as-child class="flex gap-0 border-none px-0 py-0">
        <DialogTitle class="sr-only">{{ props.name }}</DialogTitle>
        <component :is="props.dialogContent" />
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import type { Component } from "vue";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { Dialog, DialogTrigger, DialogContent, DialogTitle } from "@/components/ui/dialog";

const props = defineProps<{
  name: string;
  /** 自訂 Dialog 內容組件 */
  dialogContent: Component;
}>();
</script>