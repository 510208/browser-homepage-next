<script setup lang="ts">
import { PlusIcon } from "@lucide/vue";
import { VueDraggable } from "vue-draggable-plus";
import { Button } from "@components/ui/button";
import { TooltipProvider } from "@components/ui/tooltip";
import BookmarkItem from "./BookmarkItem.vue";
import BookmarkDialog from "./BookmarkDialog.vue";
import { useBookmarks } from "./useBookmarks";

const {
  bookmarks,
  dialogState,
  openAddDialog,
  openEditDialog,
  handleDialogSubmit,
  handleDeleteBookmark,
  updateDialogOpen,
} = useBookmarks();
</script>

<template>
  <div class="mx-auto w-full max-w-md p-4">
    <TooltipProvider>
      <VueDraggable v-model="bookmarks" :animation="150" item-key="id" class="grid w-full gap-2">
        <BookmarkItem
          v-for="bookmark in bookmarks"
          :key="bookmark.id"
          :bookmark="bookmark"
          @edit="openEditDialog"
          @delete="handleDeleteBookmark"
        />
      </VueDraggable>
    </TooltipProvider>

    <div v-if="bookmarks.length < 10" class="mt-2">
      <Button
        variant="outline"
        class="flex h-12 w-full items-center justify-center gap-2 border-dashed"
        @click="openAddDialog"
      >
        <PlusIcon class="h-5 w-5" />
        <span>新增書籤 ({{ bookmarks.length }}/10)</span>
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
