<template>
  <Command>
    <CommandInput placeholder="搜尋你想搜的..." v-model="searchQuery" @keydown.enter="doSearch" />
    <CommandList>
      <CommandEmpty>等等...還在搜尋中！</CommandEmpty>
      <CommandGroup heading="Settings">
        <CommandItem value="profile">Profile</CommandItem>
        <CommandItem value="billing">Billing</CommandItem>
        <CommandItem value="settings">Settings</CommandItem>
      </CommandGroup>
    </CommandList>
  </Command>
</template>

<script setup lang="ts">
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { ref, onMounted } from "vue";

const searchQuery = ref("");

function doSearch() {
  window.open(`https://www.google.com/search?q=${searchQuery.value}`, "_blank");
}

onMounted(() => {
  searchQuery.value = "";
});
</script>
