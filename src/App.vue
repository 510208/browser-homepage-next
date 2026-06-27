<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { animate, stagger } from "animejs";

import { Clock } from "@/components/widgets/clock";
import { SearchBox } from "@/components/widgets/search-box";
import { Quote } from "@/components/widgets/quote";
import { Avatar } from "@/components/widgets/avatar";
import { Weather } from "@/components/widgets/weather";
import Bookmarks from "@/components/widgets/bookmarks/Bookmarks.vue";
import { TrendingBadgeList } from "@/components/widgets/trending-badges";
import { DeviceBadgeList } from "@/components/widgets/device";

import { BottomCenter, RightTop, LeftTop, LeftBottom, RightBottom } from "@/components/container";

import "vue-sonner/style.css";
import { Toaster } from "@/components/ui/sonner";

// 宣告計時器變數，用於追蹤游標閒置時間
let idleTimer: ReturnType<typeof setTimeout> | null = null;

// 宣告狀態標記，避免重複觸發相同的動畫
let isHidden = false;

// 定義執行隱藏動畫的函式
const animateWidgetsHide = () => {
  if (isHidden) return;
  isHidden = true;

  // 直接傳入 ID 選擇器字串，由 Anime.js 內部去抓取對應的真實 DOM 元素
  animate("#sh-left-top-container", {
    x: { to: -100 },
    y: { to: -100 },
    opacity: { to: 0 },
    duration: 500,
    ease: "outQuad",
  });
  animate("#sh-right-top-container", {
    x: { to: 100 },
    y: { to: -100 },
    opacity: { to: 0 },
    duration: 500,
    delay: 50,
    ease: "outQuad",
  });
  animate("#sh-left-bottom-container", {
    x: { to: -100 },
    y: { to: 100 },
    opacity: { to: 0 },
    duration: 500,
    delay: 100,
    ease: "outQuad",
  });
  animate("#sh-right-bottom-container", {
    x: { to: 100 },
    y: { to: 100 },
    opacity: { to: 0 },
    duration: 500,
    delay: 150,
    ease: "outQuad",
  });
  animate("#sh-bottom-center-search-box", {
    y: { to: 100 },
    opacity: { to: 0 },
    duration: 500,
    delay: 200,
    ease: "outQuad",
  });
  // 下移時間和名言區塊，形成整體漸隱效果
  animate("#sh-bottom-center-time", {
    y: { to: 60 },
    duration: 500,
    delay: 250,
    ease: "outQuad",
    opacity: { to: 0.4 },
  });
};

// 定義執行顯示動畫的函式
const animateWidgetsShow = () => {
  if (!isHidden) return;
  isHidden = false;

  // 傳入由 ID 選擇器字串組成的陣列，集體回復初始狀態
  animate(
    [
      "#sh-left-top-container",
      "#sh-right-top-container",
      "#sh-left-bottom-container",
      "#sh-right-bottom-container",
      "#sh-bottom-center-search-box",
    ],
    {
      x: { to: 0 },
      y: { to: 0 },
      opacity: { to: 1 },
      duration: 300,
      delay: stagger(50), // 依序延遲顯示，形成漸進效果
      ease: "outQuad",
    },
  );

  // 移回時間和名言區塊，形成整體漸顯效果
  animate("#sh-bottom-center-time", {
    y: { to: 0 },
    opacity: { to: 1 },
    duration: 300,
    delay: 250,
    ease: "outQuad",
  });
};

// 重設閒置計時器的函式
const resetIdleTimer = () => {
  animateWidgetsShow();

  if (idleTimer) {
    clearTimeout(idleTimer);
  }

  idleTimer = setTimeout(() => {
    animateWidgetsHide();
  }, 5000);
};

// 元件掛載時註冊全域滑鼠移動監聽事件並初始化計時器
onMounted(() => {
  window.addEventListener("mousemove", resetIdleTimer);
  window.addEventListener("keydown", resetIdleTimer);

  // 由於改用 ID 選擇器，同樣建議在下一幀渲染時再進行首次初始化，確保 DOM 已存在於頁面上
  requestAnimationFrame(() => {
    resetIdleTimer();
  });
});

// 元件卸載時清除事件監聽與計時器，避免記憶體洩漏
onUnmounted(() => {
  window.removeEventListener("mousemove", resetIdleTimer);
  if (idleTimer) {
    clearTimeout(idleTimer);
  }
});
</script>

<template>
  <div id="sh-main" class="fixed top-0 left-0 z-10 h-screen w-screen">
    <BottomCenter>
      <div class="flex flex-col items-center gap-1" id="sh-bottom-center-time">
        <Clock />
        <Quote />
      </div>
      <div id="sh-bottom-center-search-box">
        <SearchBox />
      </div>
    </BottomCenter>

    <RightTop>
      <Avatar />
      <Bookmarks class="mt-30" />
    </RightTop>

    <LeftTop>
      <Weather />
    </LeftTop>

    <LeftBottom>
      <TrendingBadgeList />
    </LeftBottom>

    <RightBottom>
      <DeviceBadgeList />
    </RightBottom>
  </div>

  <div id="sh-background" class="pointer-events-none fixed top-0 left-0 -z-10 h-screen w-screen">
    <div
      class="absolute inset-0 bg-gradient-to-br from-[#FFFFFF] to-[#555555] mix-blend-soft-light"
    />
    <img
      src="@assets/bg-images/background.webp"
      alt="Background"
      class="h-full w-full object-cover"
    />
  </div>

  <Toaster />
</template>
