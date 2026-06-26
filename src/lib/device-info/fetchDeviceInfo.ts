import type { DeviceDataResponse } from "@/types/deviceDataResponse";

const LOCAL_SERVER_URL = "http://127.0.0.1:5000";

async function fetchDeviceInfo() {
  // 抓取裝置狀態
  try {
    const response = await fetch(`${LOCAL_SERVER_URL}/api/status`);
    if (!response.ok) {
      throw new Error("[fetchDeviceInfo] Network response was not ok");
    }

    console.log("[fetchDeviceInfo] Device info fetched successfully:", response);
    return await (response.json() as Promise<DeviceDataResponse>);
  } catch (error) {
    console.error("[fetchDeviceInfo] Error fetching device info:", error);
    throw error;
  }
}

export { fetchDeviceInfo, LOCAL_SERVER_URL };
