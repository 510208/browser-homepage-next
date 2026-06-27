<script setup lang="ts">
import { CirclePlus } from "@lucide/vue";
import { VueDraggable } from "vue-draggable-plus";
import { TooltipProvider } from "@components/ui/tooltip";
import BookmarkItem from "./BookmarkItem.vue";
import BookmarkDialog from "./BookmarkDialog.vue";
import { useBookmarks } from "./useBookmarks";
import { cnUtils as cn } from "@/lib";
import type { Bookmark } from "./types";
import { Button } from "@/components/ui/button";

import { onMounted, onUnmounted } from "vue";
import hotkeys from "hotkeys-js";

const {
  bookmarks,
  dialogState,
  openAddDialog,
  openEditDialog,
  handleDialogSubmit,
  handleDeleteBookmark,
  updateDialogOpen,
} = useBookmarks();

// 接受參數style
const props = defineProps<{
  style?: Record<string, string>;
}>();

const emit = defineEmits<{
  (e: "update:bookmarks", bookmarks: Bookmark[]): void;
}>();

// 掛載時建立對數字鍵與加號鍵的監聽，數字鍵對應到書籤的索引位置，按下加號鍵則打開新增書籤對話框
onMounted(() => {
  bookmarks.value.forEach((bookmark, index) => {
    hotkeys(`${index + 1}`, () => {
      // 開啟該書籤對應的網址
      window.open(bookmark.url, "_blank");
    });
  });

  hotkeys("a", () => {
    openAddDialog();
  });
});

onUnmounted(() => {
  hotkeys.unbind();
});
</script>

<template>
  <div :class="cn('flex w-[50px] flex-col items-center gap-2.5 p-0', props.style)">
    <TooltipProvider>
      <VueDraggable
        v-model="bookmarks"
        :animation="150"
        item-key="id"
        class="flex w-full flex-col items-center gap-3"
      >
        <BookmarkItem
          v-for="bookmark in bookmarks"
          :key="bookmark.id"
          :bookmark="bookmark"
          @edit="openEditDialog"
          @delete="handleDeleteBookmark"
        />
      </VueDraggable>
    </TooltipProvider>

    <div v-if="bookmarks.length < 10" class="flex h-12 w-12 items-center justify-center">
      <Button
        variant="ghost"
        size="icon-lg"
        class="flex items-center justify-center rounded-full text-muted-foreground transition-all hover:scale-115 hover:border-foreground hover:text-foreground"
        @click="openAddDialog"
      >
        <CirclePlus />
      </Button>
    </div>

    <BookmarkDialog
      :open="dialogState.open"
      :mode="dialogState.mode"
      :bookmark="dialogState.selectedBookmark"
      @update:open="updateDialogOpen"
      @submit="handleDialogSubmit"
    />
  </div>
</template>