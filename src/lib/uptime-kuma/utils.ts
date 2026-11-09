import type {
  UptimeKumaHeartbeat,
  UptimeKumaHeartbeatList,
  UptimeKumaHeartbeatResponse,
  UptimeKumaMonitor,
  UptimeKumaPublicGroup,
} from "@/types/uptimeKuma";

export type UptimeStatus = "up" | "down" | "pending" | "maintenance" | "unknown";

export interface UptimeMonitorData {
  id: number;
  name: string;
  status: UptimeStatus;
  heartbeats: UptimeKumaHeartbeat[];
  uptime: number | null;
}

export interface UptimeGroupData {
  id: number;
  name: string;
  status: UptimeStatus;
  monitors: UptimeMonitorData[];
  heartbeats: UptimeKumaHeartbeat[];
  uptime: number | null;
}

export interface UptimeSummaryData {
  total: number;
  up: number;
  down: number;
  pending: number;
  maintenance: number;
  unknown: number;
  status: UptimeStatus;
}

export const statusLabels: Record<UptimeStatus, string> = {
  up: "線上",
  down: "離線",
  pending: "待確認",
  maintenance: "維護",
  unknown: "未知",
};

export const statusColors: Record<UptimeStatus, { color: string; foreground: string }> = {
  up: { color: "#77c977", foreground: "#004b00" },
  down: { color: "#c97777", foreground: "#4b0000" },
  pending: { color: "#c9c977", foreground: "#4b4500" },
  maintenance: { color: "#777bc9", foreground: "#05004b" },
  unknown: { color: "var(--color-brown-500)", foreground: "var(--color-brown-950)" },
};

export function heartbeatStatus(status?: number): UptimeStatus {
  switch (status) {
    case 0:
      return "down";
    case 1:
      return "up";
    case 2:
      return "pending";
    case 3:
      return "maintenance";
    default:
      return "unknown";
  }
}

/** 離線優先；缺少紀錄時不能判定整個群組正常。 */
export function aggregateStatus(statuses: UptimeStatus[]): UptimeStatus {
  if (!statuses.length) return "unknown";
  for (const status of ["down", "pending", "unknown", "maintenance"] as const) {
    if (statuses.includes(status)) return status;
  }
  return "up";
}

export function sortedHeartbeats(heartbeats: UptimeKumaHeartbeat[] = []) {
  return [...heartbeats].sort((a, b) => a.time.localeCompare(b.time));
}

function monitorData(
  monitor: UptimeKumaMonitor,
  heartbeat: UptimeKumaHeartbeatResponse,
): UptimeMonitorData {
  const heartbeats = sortedHeartbeats(heartbeat.heartbeatList[String(monitor.id)]);
  const uptime = heartbeat.uptimeList[`${monitor.id}_24`];
  return {
    id: monitor.id,
    name: monitor.name,
    status: heartbeatStatus(heartbeats.at(-1)?.status),
    heartbeats,
    uptime:
      typeof uptime === "number" && Number.isFinite(uptime)
        ? Math.min(1, Math.max(0, uptime))
        : null,
  };
}

/** 依 UTC 分鐘對齊各監視器，避免將不同時間的心跳以陣列索引合併。 */
export function groupHeartbeats(
  monitors: UptimeKumaMonitor[],
  heartbeatList: UptimeKumaHeartbeatList,
) {
  const minutes = new Map<string, Map<number, UptimeKumaHeartbeat>>();
  for (const monitor of monitors) {
    for (const heartbeat of sortedHeartbeats(heartbeatList[String(monitor.id)])) {
      const minute = heartbeat.time.slice(0, 16);
      if (!minutes.has(minute)) minutes.set(minute, new Map());
      minutes.get(minute)!.set(monitor.id, heartbeat);
    }
  }

  const statusCodes: Record<UptimeStatus, number> = {
    down: 0,
    up: 1,
    pending: 2,
    maintenance: 3,
    unknown: -1,
  };
  return [...minutes.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([minute, entries]): UptimeKumaHeartbeat => ({
      time: `${minute}:00.000`,
      status:
        statusCodes[
          aggregateStatus(
            monitors.map((monitor) => heartbeatStatus(entries.get(monitor.id)?.status)),
          )
        ],
      ping: null,
      msg: "",
    }));
}

export function buildGroups(
  publicGroups: UptimeKumaPublicGroup[],
  heartbeat: UptimeKumaHeartbeatResponse,
): UptimeGroupData[] {
  return [...publicGroups]
    .sort((a, b) => a.weight - b.weight)
    .map((group) => {
      const monitors = group.monitorList.map((monitor) => monitorData(monitor, heartbeat));
      // 完整群組的 24 小時平均可用率；缺值時顯示 N/A。
      const uptime =
        monitors.length && monitors.every((monitor) => monitor.uptime !== null)
          ? monitors.reduce((sum, monitor) => sum + monitor.uptime!, 0) / monitors.length
          : null;

      return {
        id: group.id,
        name: group.name,
        monitors,
        status: aggregateStatus(monitors.map((monitor) => monitor.status)),
        heartbeats: groupHeartbeats(group.monitorList, heartbeat.heartbeatList),
        uptime,
      };
    });
}

export function summarizeGroups(groups: UptimeGroupData[]): UptimeSummaryData {
  const monitors = new Map(
    groups.flatMap((group) => group.monitors).map((monitor) => [monitor.id, monitor]),
  );
  const summary: UptimeSummaryData = {
    total: monitors.size,
    up: 0,
    down: 0,
    pending: 0,
    maintenance: 0,
    unknown: 0,
    status: "unknown",
  };
  for (const monitor of monitors.values()) summary[monitor.status]++;
  summary.status = aggregateStatus([...monitors.values()].map((monitor) => monitor.status));
  return summary;
}

const percentFormatter = new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 1 });

export function formatUptime(uptime: number | null): string {
  return uptime === null ? "N/A" : `${percentFormatter.format(uptime * 100)}%`;
}

export function formatHeartbeatTime(time: string) {
  // Uptime Kuma 回傳沒有時區後綴的 UTC 時間。
  const date = new Date(`${time.replace(" ", "T")}Z`);
  return Number.isNaN(date.getTime()) ? time : date.toLocaleString("zh-TW");
}

/** 將完整歷史壓縮成 13 格，每格保留該時段最需關注的狀態。 */
export function heartbeatSegments(heartbeats: UptimeKumaHeartbeat[], count = 13) {
  const entries = sortedHeartbeats(heartbeats);
  return Array.from({ length: count }, (_, index) => {
    const start =
      entries.length < count
        ? index - (count - entries.length)
        : Math.floor((index * entries.length) / count);
    const end =
      entries.length < count ? start + 1 : Math.floor(((index + 1) * entries.length) / count);
    const bucket = start < 0 ? [] : entries.slice(start, end);
    const status = aggregateStatus(bucket.map((entry) => heartbeatStatus(entry.status)));
    const first = bucket[0];
    const last = bucket.at(-1);
    const label =
      first && last
        ? `${formatHeartbeatTime(first.time)}${first !== last ? ` – ${formatHeartbeatTime(last.time)}` : ""}：${statusLabels[status]}`
        : "尚無心跳紀錄";
    return { status, label };
  });
}

/** 延遲折線使用真實 ping；空值分段，避免補造延遲或跨過缺失紀錄。 */
export function pingSegments(heartbeats: UptimeKumaHeartbeat[]) {
  const entries = sortedHeartbeats(heartbeats).slice(-18);
  const values = entries
    .map((entry) => entry.ping)
    .filter(
      (ping): ping is number => typeof ping === "number" && Number.isFinite(ping) && ping >= 0,
    );
  if (!values.length) return [];
  const low = Math.min(...values);
  const high = Math.max(...values);
  const segments: string[][] = [];
  let segment: string[] = [];

  entries.forEach((entry, index) => {
    if (entry.ping === null || !Number.isFinite(entry.ping) || entry.ping < 0) {
      if (segment.length) segments.push(segment);
      segment = [];
      return;
    }
    const x = entries.length > 1 ? 1 + (index * 106) / (entries.length - 1) : 54;
    const y = high === low ? 8 : 14 - ((entry.ping - low) * 12) / (high - low);
    segment.push(`${x.toFixed(2)},${y.toFixed(2)}`);
  });
  if (segment.length) segments.push(segment);
  return segments.map((points) => points.join(" "));
}
