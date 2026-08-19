<template>
  <div
    class="flex w-full max-w-2xl flex-col flex-nowrap items-stretch gap-0 overflow-hidden rounded-2xl border border-brown-800 bg-brown-900"
  >
    <!-- 設定區塊 -->
    <div class="grid grid-cols-2 gap-1 p-2">
      <BullshitSettingFrame name="topic" title="主題" v-model="settings.topic" class="col-span-2" />
      <BullshitSettingFrame
        name="word-count"
        title="字數"
        :model-value="String(settings.totalTextCount ?? '')"
        @update:model-value="settings.totalTextCount = $event ? Number($event) : undefined"
      />
      <BullshitSettingFrame
        name="paragraphs"
        title="段落數"
        :model-value="String(settings.paragraphs ?? '')"
        @update:model-value="settings.paragraphs = $event ? Number($event) : undefined"
      />
    </div>

    <!-- 產生按鈕 -->
    <div class="flex justify-end p-4 pt-0">
      <Button
        class="flex justify-center gap-1"
        variant="default"
        @click="generateBullshit(settings)"
      >
        <Pilcrow class="h-4 w-4" />
        產生
      </Button>
    </div>

    <!-- 產生結果 -->
    <div class="flex flex-1 flex-col gap-1 p-2">
      <Label class="text-xs font-medium tracking-widest text-brown-400" for="result">結果</Label>
      <Textarea v-model="result" id="result" readonly class="h-full w-full resize-none" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { Pilcrow } from "@lucide/vue";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import BullshitSettingFrame from "./BullshitSettingFrame.vue";

import { type GenerateOptions, generateBullshit } from "@/lib/bullshit/bullshitGenerator.ts";

const settings = ref({
  topic: "義大利麵",
  totalTextCount: 300,
  paragraphs: 1,
} as GenerateOptions);
const result = ref("");
</script>
