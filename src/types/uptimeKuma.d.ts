/** Uptime Kuma Status Page 設定 */
export interface UptimeKumaStatusPageConfig {
  slug: string;
  title: string;
  description: string;
  icon: string;
  autoRefreshInterval: number;
  theme: string;
  published: boolean;
  showTags: boolean;
  customCSS: string;
  footerText: string;
  showPoweredBy: boolean;
  analyticsId: string | null;
  analyticsScriptUrl: string | null;
  analyticsType: string | null;
  showCertificateExpiry: boolean;
  showOnlyLastHeartbeat: boolean;
  rssTitle: string;
}

/** Status Page Incident */
export interface UptimeKumaIncident {
  id: number;
  title: string;
  content: string;
  style: string;
  timestamp: string;
  pin: boolean;
  createdDate: string;
  lastUpdatedDate: string;
}

/** Monitor Tag */
export interface UptimeKumaTag {
  id: number;
  name: string;
  color: string;
}

/** Monitor */
export interface UptimeKumaMonitor {
  id: number;
  name: string;
  sendUrl: number;
  type: string;
  tags: UptimeKumaTag[];
  certExpiryDaysRemaining: string;
  validCert: boolean;
}

/** Status Page Monitor Group */
export interface UptimeKumaPublicGroup {
  id: number;
  name: string;
  weight: number;
  monitorList: UptimeKumaMonitor[];
}

/** GET /api/status-page/:slug */
export interface UptimeKumaStatusPageResponse {
  config: UptimeKumaStatusPageConfig;
  incidents: UptimeKumaIncident[];
  publicGroupList: UptimeKumaPublicGroup[];
}

// ===

/** 單筆 Heartbeat */
export interface UptimeKumaHeartbeat {
  status: number;
  time: string;
  msg: string;
  ping: number | null;
}

/**
 * Heartbeat List
 * Key: Monitor ID（字串）
 */
export type UptimeKumaHeartbeatList = Record<string, UptimeKumaHeartbeat[]>;

/**
 * Uptime List
 * Key: Monitor ID_統計時數
 * Value: Uptime 百分比
 *
 * 例如：
 * {
 *     "1_24": 1,
 *     "1_720": 0.998
 * }
 */
export type UptimeKumaUptimeList = Record<string, number>;

/** GET /api/status-page/heartbeat/:slug */
export interface UptimeKumaHeartbeatResponse {
  heartbeatList: UptimeKumaHeartbeatList;
  uptimeList: UptimeKumaUptimeList;
}
