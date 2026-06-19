import { ref, watch, onMounted } from "vue";
import type { Bookmark, DialogState } from "./types";

export function useBookmarks() {
  const LOCAL_STORAGE_KEY = "sam-hacker-bookmarks";
  const bookmarks = ref<Bookmark[]>([]);

  const dialogState = ref<DialogState>({
    open: false,
    mode: "add",
    selectedBookmark: null,
  });

  onMounted(() => {
    const savedData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedData) {
      try {
        bookmarks.value = JSON.parse(savedData);
      } catch (e) {
        console.error("Failed to parse bookmarks from localStorage", e);
      }
    }
  });

  watch(
    bookmarks,
    (newBookmarks) => {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(newBookmarks));
    },
    { deep: true },
  );

  function openAddDialog() {
    dialogState.value = {
      open: true,
      mode: "add",
      selectedBookmark: null,
    };
  }

  function openEditDialog(bookmark: Bookmark) {
    dialogState.value = {
      open: true,
      mode: "edit",
      selectedBookmark: bookmark,
    };
  }

  function handleDialogSubmit(url: string) {
    if (dialogState.value.mode === "add") {
      if (bookmarks.value.length >= 10) return;
      bookmarks.value.push({
        id: crypto.randomUUID(),
        url,
      });
    } else if (dialogState.value.mode === "edit" && dialogState.value.selectedBookmark) {
      const id = dialogState.value.selectedBookmark.id;
      const index = bookmarks.value.findIndex((b) => b.id === id);
      if (index !== -1) {
        bookmarks.value[index].url = url;
      }
    }
  }

  function handleDeleteBookmark(id: string) {
    bookmarks.value = bookmarks.value.filter((b) => b.id !== id);
  }

  function updateDialogOpen(value: boolean) {
    dialogState.value.open = value;
  }

  return {
    bookmarks,
    dialogState,
    openAddDialog,
    openEditDialog,
    handleDialogSubmit,
    handleDeleteBookmark,
    updateDialogOpen,
  };
}
