/**
 * 系統基本資訊
 */
interface SystemStatus {
  /** 運行作業系統名稱，例如 "Linux", "Windows", "Darwin" */
  os: string;
  /** 作業系統的發行版本號 */
  os_release: string;
  /** 硬體架構，例如 "x86_64", "AMD64", "arm64" */
  architecture: string;
  /** 伺服器自啟動以來運行的總秒數 */
  uptime_seconds: number;
}

/**
 * CPU 硬體與即時使用狀態
 */
interface CpuStatus {
  /** CPU 的型號名稱與規格字串 */
  model: string;
  /** 實體核心（Physical Cores）的數量 */
  physical_cores: number;
  /** 邏輯核心（Logical Cores / 執行緒）的總數量 */
  total_cores: number;
  /** CPU 整體平均使用率（百分比 0-100，非阻塞快速估算值） */
  overall_usage_percent: number;
  /** 每個邏輯核心的即時使用率列表（百分比 0-100） */
  per_core_usage_percent: number[];
}

/**
 * 單一記憶體區塊狀態（用於 RAM 與 Swap）
 */
interface MemoryMetrics {
  /** 總容量（位元組 Bytes） */
  total_bytes: number;
  /** 已使用容量（位元組 Bytes） */
  used_bytes: number;
  /** 記憶體使用率（百分比 0-100） */
  usage_percent: number;
  /** 可用或剩餘容量（位元組 Bytes）。在 RAM 為 available，在 Swap 為 free */
  available_bytes?: number;
  /** 剩餘可用容量（位元組 Bytes） */
  free_bytes?: number;
}

/**
 * 記憶體與虛擬記憶體完整狀態
 */
interface MemoryStatus {
  /** 實體記憶體狀態 */
  ram: MemoryMetrics & { available_bytes: number };
  /** 交換空間 / 虛擬記憶體狀態 */
  swap: MemoryMetrics & { free_bytes: number };
}

/**
 * 根目錄磁碟儲存空間狀態
 */
interface DiskStatus {
  /** 磁碟總容量（位元組 Bytes） */
  total_bytes: number;
  /** 已使用磁碟容量（位元組 Bytes） */
  used_bytes: number;
  /** 剩餘可用磁碟容量（位元組 Bytes） */
  free_bytes: number;
  /** 磁碟空間使用率（百分比 0-100） */
  usage_percent: number;
}

/**
 * 網路介面累計流量統計
 */
interface NetworkStatus {
  /** 自系統啟動以來累計發送的資料量（位元組 Bytes） */
  bytes_sent: number;
  /** 自系統啟動以來累計接收的資料量（位元組 Bytes） */
  bytes_recv: number;
}

/**
 * 裝置電池狀態
 */
interface BatteryStatus {
  /** 當前剩餘電量百分比（0-100） */
  percent: number;
  /** 是否已連接外部電源（充電中或電源線已接上） */
  power_plugged: boolean;
}

/**
 * 伺服器硬體與系統狀態 API 的主回應資料結構
 */
interface DeviceDataResponse {
  /** 系統基本資訊 */
  system: SystemStatus;
  /** CPU 硬體與即時使用狀態 */
  cpu: CpuStatus;
  /** 記憶體（RAM）與虛擬記憶體（Swap）狀態 */
  memory: MemoryStatus;
  /** 根目錄磁碟儲存空間狀態 */
  disk: DiskStatus;
  /** 網路介面累計流量統計 */
  network: NetworkStatus;
  /** 裝置電池狀態。若運行於桌上型電腦或無電池裝置，則整個欄位回傳 null */
  battery: BatteryStatus | null;
}

export type {
  SystemStatus,
  CpuStatus,
  MemoryMetrics,
  MemoryStatus,
  DiskStatus,
  NetworkStatus,
  BatteryStatus,
  DeviceDataResponse,
};
