<script setup lang="ts">
import { CirclePlus } from "@lucide/vue";
import { VueDraggable } from "vue-draggable-plus";
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
  <div
    class="fixed top-1/2 right-6 flex w-[50px] -translate-y-1/2 flex-col items-center gap-2.5 p-0"
  >
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
      <button
        type="button"
        class="flex h-11 w-11 items-center justify-center rounded-full border-muted-foreground/60 bg-transparent text-muted-foreground transition-all hover:scale-115 hover:border-foreground hover:text-foreground"
        @click="openAddDialog"
      >
        <CirclePlus class="h-5 w-5" />
      </button>
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