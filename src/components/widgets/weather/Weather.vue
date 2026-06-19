<template>
  <HoverCard>
    <HoverCardTrigger>
      <WeatherTrigger />
    </HoverCardTrigger>
    <HoverCardContent class="w-[300px]">
      <WeatherCard />
    </HoverCardContent>
  </HoverCard>
</template>

<script setup lang="ts">
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { WeatherCard, WeatherTrigger } from "./index";
</script>