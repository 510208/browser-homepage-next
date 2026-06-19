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