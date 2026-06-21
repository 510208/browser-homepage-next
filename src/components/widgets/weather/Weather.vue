<template>
  <HoverCard :open="true">
    <HoverCardTrigger>
      <WeatherTrigger />
    </HoverCardTrigger>
    <HoverCardContent class="w-[400px] overflow-hidden px-0 py-0" align="start">
      <WeatherCard />
    </HoverCardContent>
  </HoverCard>
</template>

<script setup lang="ts">
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { WeatherCard, WeatherTrigger } from "./index";
</script>