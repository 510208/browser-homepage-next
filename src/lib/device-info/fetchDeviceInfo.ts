import type { DeviceDataResponse } from "@/types/deviceDataResponse";

const LOCAL_SERVER_URL = "http://127.0.0.1:5000";

function fetchDeviceInfo() {
  // 抓取裝置狀態
  return fetch(`${LOCAL_SERVER_URL}/device-info`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json() as Promise<DeviceDataResponse>;
    })
    .catch((error) => {
      console.error("Error fetching device info:", error);
      throw error;
    });
}

export { fetchDeviceInfo, LOCAL_SERVER_URL };
