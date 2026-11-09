import { computed, onMounted, onUnmounted, ref, shallowRef } from "vue";
import { fetchUptimeKuma } from "@/lib/uptime-kuma/fetchUptimeKuma";
import { buildGroups, summarizeGroups } from "@/lib/uptime-kuma/utils";

export function useUptimeMonitor() {
  const data = shallowRef<Awaited<ReturnType<typeof fetchUptimeKuma>> | null>(null);
  const isLoading = ref(true);
  const isRefreshing = ref(false);
  const error = ref<string | null>(null);
  const updatedAt = ref<Date | null>(null);
  const groups = computed(() =>
    data.value ? buildGroups(data.value.statusPage.publicGroupList, data.value.heartbeat) : [],
  );
  const summary = computed(() => summarizeGroups(groups.value));

  let timer: ReturnType<typeof setTimeout> | undefined;
  let controller: AbortController | undefined;
  let disposed = false;

  async function refresh() {
    if (disposed || isRefreshing.value) return;
    clearTimeout(timer);
    isRefreshing.value = true;
    controller = new AbortController();
    const requestController = controller;
    const timeout = setTimeout(() => requestController.abort(), 20_000);

    try {
      const result = await fetchUptimeKuma(requestController.signal);
      if (disposed) return;
      // 兩個端點都成功才替換資料，避免群組與心跳來自不同更新。
      data.value = result;
      error.value = null;
      updatedAt.value = new Date();
    } catch {
      if (!disposed) error.value = "無法更新監控資料";
    } finally {
      clearTimeout(timeout);
      requestController.abort();
      if (!disposed) {
        isLoading.value = false;
        isRefreshing.value = false;
        const seconds = data.value?.statusPage.config.autoRefreshInterval;
        const interval =
          typeof seconds === "number" && Number.isFinite(seconds) && seconds > 0
            ? Math.max(10, seconds) * 1000
            : 60_000;
        timer = setTimeout(refresh, interval);
      }
    }
  }

  onMounted(refresh);
  onUnmounted(() => {
    disposed = true;
    clearTimeout(timer);
    controller?.abort();
  });

  return { groups, summary, isLoading, isRefreshing, error, updatedAt, refresh };
}
