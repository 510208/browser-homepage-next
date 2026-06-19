<script setup lang="ts">
import { computed } from "vue";
import { PencilIcon, TrashIcon } from "@lucide/vue";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@components/ui/context-menu";
import { Tooltip, TooltipContent, TooltipTrigger } from "@components/ui/tooltip";
import type { Bookmark } from "./types";

const props = defineProps<{
  bookmark: Bookmark;
}>();

const emit = defineEmits<{
  (e: "edit", bookmark: Bookmark): void;
  (e: "delete", id: string): void;
}>();

const faviconUrl = computed(() => {
  try {
    const domain = new URL(props.bookmark.url).hostname;
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=128`;
  } catch (e) {
    return `https://www.google.com/s2/favicons?domain=${props.bookmark.url}&sz=128`;
  }
});

const displayDomain = computed(() => {
  try {
    return new URL(props.bookmark.url).hostname;
  } catch (e) {
    return props.bookmark.url;
  }
});

function handleDelete() {
  const confirmDelete = window.confirm("確定要刪除此書籤嗎？");
  if (confirmDelete) {
    emit("delete", props.bookmark.id);
  }
}
</script>

<template>
  <div class="cursor-grab active:cursor-grabbing">
    <ContextMenu>
      <ContextMenuTrigger as-child>
        <div>
          <Tooltip>
            <TooltipTrigger as-child>
              <a
                :href="props.bookmark.url"
                target="_blank"
                rel="noopener noreferrer"
                class="flex w-full items-center gap-3 rounded-lg border bg-card p-3 text-card-foreground shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground"
              >
                <img
                  :src="faviconUrl"
                  alt="favicon"
                  class="h-6 w-6 rounded-sm object-contain"
                  loading="lazy"
                />
                <span class="truncate text-sm font-medium">
                  {{ displayDomain }}
                </span>
              </a>
            </TooltipTrigger>
            <TooltipContent side="left">
              <p>{{ props.bookmark.url }}</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </ContextMenuTrigger>

      <ContextMenuContent class="w-32">
        <ContextMenuItem @select="emit('edit', props.bookmark)">
          <PencilIcon class="mr-2 h-4 w-4" />
          <span>編輯</span>
        </ContextMenuItem>
        <ContextMenuItem variant="destructive" @select="handleDelete">
          <TrashIcon class="mr-2 h-4 w-4" />
          <span>移除</span>
        </ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  </div>
</template>
