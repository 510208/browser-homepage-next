import { fetch } from "@/lib/fetch";
import type { UptimeKumaHeartbeatResponse, UptimeKumaStatusPageResponse } from "@/types/uptimeKuma";

const API_BASE = "https://api.samhacker.xyz/uptime-kuma";

async function fetchJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API_BASE}/${path}`, { signal, cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Uptime Kuma ${path}: HTTP ${response.status}`);
  }
  return response.json();
}

export function fetchStatusPage(signal?: AbortSignal) {
  return fetchJson<UptimeKumaStatusPageResponse>("status-page", signal);
}

export function fetchHeartbeat(signal?: AbortSignal) {
  return fetchJson<UptimeKumaHeartbeatResponse>("heartbeat", signal);
}

export async function fetchUptimeKuma(signal?: AbortSignal) {
  const [statusPage, heartbeat] = await Promise.all([
    fetchStatusPage(signal),
    fetchHeartbeat(signal),
  ]);

  if (
    !statusPage?.config ||
    !Array.isArray(statusPage.publicGroupList) ||
    !heartbeat?.heartbeatList ||
    !heartbeat.uptimeList
  ) {
    throw new Error("Invalid Uptime Kuma response");
  }

  return { statusPage, heartbeat };
}
