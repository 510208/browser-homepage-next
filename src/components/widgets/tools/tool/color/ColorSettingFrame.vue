<template>
  <div class="flex flex-col gap-1 p-3">
    <span class="text-xs font-medium tracking-widest text-brown-400">{{ props.title }}</span>
    <div class="flex gap-1">
      <Input
        v-model="localValue"
        class="w-full flex-1 border-brown-800"
        @blur="handleCommit"
        @keyup.enter="handleCommit"
      />
      <Button variant="ghost" size="icon" @click="handleCopy"><Copy /></Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Copy } from "@lucide/vue";
import { toast } from "vue-sonner";

const model = defineModel<string>({ default: "" });

const props = defineProps<{
  title?: string;
}>();

// 本地緩衝文字，防止即時觸發父組件驗證導致無法打字
const localValue = ref(model.value);

// 當外部色彩變更時（如從調色盤選色），同步更新內部文字
watch(
  model,
  (newVal) => {
    localValue.value = newVal;
  },
  { immediate: true },
);

// 僅在按下 Enter 或失去駐點 (Blur) 時才提交變更
const handleCommit = () => {
  if (localValue.value !== model.value) {
    model.value = localValue.value;
  }
};

function handleCopy() {
  navigator.clipboard.writeText(localValue.value).then(
    () => {
      console.log("Copied to clipboard:", localValue.value);
      toast.success("已複製到剪貼簿");
    },
    (err) => {
      console.error("Failed to copy text: ", err);
      toast.error("複製失敗");
    },
  );
}
</script>
