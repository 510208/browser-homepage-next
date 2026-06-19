<script setup lang="ts">
import { ref, watch } from "vue";
import { Button } from "@components/ui/button";
import { Input } from "@components/ui/input";
import { Label } from "@components/ui/label";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@components/ui/dialog";
import type { Bookmark } from "./types";

const props = defineProps<{
  open: boolean;
  mode: "add" | "edit";
  bookmark: Bookmark | null;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "submit", url: string): void;
}>();

const inputUrl = ref("");

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      inputUrl.value = props.mode === "edit" && props.bookmark ? props.bookmark.url : "";
    }
  },
);

function handleSubmit() {
  if (!inputUrl.value.trim()) return;

  let formattedUrl = inputUrl.value.trim();
  if (!/^https?:\/\//i.test(formattedUrl)) {
    formattedUrl = `https://${formattedUrl}`;
  }

  emit("submit", formattedUrl);
  emit("update:open", false);
}
</script>

<template>
  <Dialog :open="props.open" @update:open="emit('update:open', $event)">
    <DialogContent class="sm:max-w-[425px]">
      <form @submit.prevent="handleSubmit">
        <DialogHeader>
          <DialogTitle>{{ props.mode === "add" ? "新增書籤" : "編輯書籤" }}</DialogTitle>
          <DialogDescription>
            {{
              props.mode === "add" ? "請輸入想要加入書籤的網站網址。" : "請修改該書籤的網站網址。"
            }}
          </DialogDescription>
        </DialogHeader>
        <div class="grid gap-4 py-4">
          <div class="grid gap-3">
            <Label :for="props.mode + '-url'">網站網址</Label>
            <Input
              :id="props.mode + '-url'"
              v-model="inputUrl"
              placeholder="example.com 或 https://..."
              autocomplete="off"
              required
            />
          </div>
        </div>
        <DialogFooter>
          <DialogClose as-child>
            <Button type="button" variant="outline">取消</Button>
          </DialogClose>
          <Button type="submit">
            {{ props.mode === "add" ? "確認新增" : "儲存變更" }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
