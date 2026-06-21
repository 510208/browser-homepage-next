<template>
  <div class="flex flex-wrap gap-2.5">
    <TrendingBadge v-for="badge in badges" :key="badge.name" :data="badge.content">
      <template #icon>
        <component :is="badge.icon" size="24px" class="text-brown-500" />
      </template>
    </TrendingBadge>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import TrendingBadge from "./TrendingBadge.vue";
import { GitHubIcon, YouTubeIcon } from "vue3-simple-icons";
import { github, youtube } from "@/lib/trending";

const badges = ref<any[]>([]);

onMounted(async () => {
  try {
    const githubContent = await github.parseResponse();
    const youtubeContent = await youtube.parseResponse();

    badges.value = [
      {
        name: "GitHub",
        icon: GitHubIcon,
        content: githubContent.followers.toString(),
      },
      {
        name: "YouTube",
        icon: YouTubeIcon,
        content: youtubeContent.statistics.subscriberCount.toString(),
      },
    ];
  } catch (error) {
    console.error("Failed to fetch GitHub data:", error);
  }
});
</script>
