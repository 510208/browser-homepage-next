import { XMLParser } from "fast-xml-parser";
import type { TownVillagePointResponse } from "@/types/weatherResponse";
import { CITY_NAME_TO_DATASET_ID } from "@/consts/weather/datasetToCity";

const CWA_OPENAPI_ENDPOINT = "https://api.samhacker.xyz/cwa/v1/rest/datastore"; // 天氣API轉換端點URL
const POSITION_TO_NAME_API = "https://api.nlsc.gov.tw/other/TownVillagePointQuery"; // 單點坐標回傳行政區

// 使用瀏覽器提供的API來取得當前位置
function getLattitudeLongitude(): Promise<{ latitude: number; longitude: number }> {
  // 使用瀏覽器的 Geolocation API 來取得使用者的經緯度
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation is not supported by this browser."));
    } else {
      navigator.geolocation.getCurrentPosition(
        // 成功時的回調
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        // 失敗時的回調
        (error) => {
          reject(new Error("Failed to get location, error: " + error));
        },
      );
    }
  });
}

async function convertLocationToLocationName(
  latitude: number,
  longitude: number,
): Promise<{ id: string; response: TownVillagePointResponse }> {
  // 將經緯度轉換為行政區代碼，回傳XML格式的資料，需解析XML
  //  https://api.nlsc.gov.tw/other/TownVillagePointQuery/120.698659/24.156250
  const url = `${POSITION_TO_NAME_API}/${longitude}/${latitude}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch location ID: ${response.status} ${response.statusText}`);
  }

  const data = await response.text();
  const parser = new XMLParser();
  const parsedData = parser.parse(data); // JSON格式
  console.log("[fetchWeather/convertLocationToLocationName] Parsed location data:", parsedData);

  let townVillageItem: TownVillagePointResponse;

  // 將資料解析成 TownVillagePointResponse 型別
  try {
    townVillageItem = parsedData?.townVillageItem;
    console.log(
      "[fetchWeather/convertLocationToLocationName] Parsed location object:",
      townVillageItem,
    );
  } catch (error) {
    console.error(
      "[fetchWeather/convertLocationToLocationName] Error parsing location data:",
      error,
    );
    throw new Error("Failed to parse location data");
  }

  // 映射地區名稱至資料集ID
  try {
    const cityName = townVillageItem?.ctyName;
    const datasetId = CITY_NAME_TO_DATASET_ID[cityName];
    if (!datasetId) {
      throw new Error(`No dataset ID found for city name: ${cityName}`);
    }
    console.log(
      "[fetchWeather/convertLocationToLocationName] Mapped city name to dataset ID:",
      cityName,
      datasetId,
    );
    return { id: datasetId, response: townVillageItem };
  } catch (error) {
    console.error(
      "[fetchWeather/convertLocationToLocationName] Error mapping city name to dataset ID:",
      error,
    );
    throw new Error("Failed to map city name to dataset ID");
  }
}