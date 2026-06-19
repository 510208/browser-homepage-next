export interface Bookmark {
  id: string;
  url: string;
}

export interface DialogState {
  open: boolean;
  mode: "add" | "edit";
  selectedBookmark: Bookmark | null;
}
