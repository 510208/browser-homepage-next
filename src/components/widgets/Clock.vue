<template>
  <div class="flex items-end justify-center">
    <p id="sh-clock-text" class="font-800 text-title font-bold text-brown-500">{{ time }}</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

const time = ref("00:00");

function updateTime() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  time.value = `${hours}:${minutes}`;
}

onMounted(() => {
  updateTime();
  setInterval(updateTime, 10000); // 每10秒更新一次
});
</script>