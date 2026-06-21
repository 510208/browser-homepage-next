import { XMLParser } from "fast-xml-parser";
import type {
  TownVillagePointResponse,
  WeatherResponse,
  SimplifiedWeatherResponse,
} from "@/types/weatherResponse";
import { CITY_NAME_TO_DATASET_ID } from "@/consts/weather/datasetToCity";
import { transformWeatherData } from "./utils";
import { toast } from "vue-sonner";

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
          console.log(
            `[fetchWeather/getLattitudeLongitude] Obtained location: latitude=${position.coords.latitude}, longitude=${position.coords.longitude}`,
          );
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
  // console.log("[fetchWeather/convertLocationToLocationName] Parsed location data:", parsedData);

  let townVillageItem: TownVillagePointResponse;

  // 將資料解析成 TownVillagePointResponse 型別
  try {
    townVillageItem = parsedData?.townVillageItem;
    console.log(
      // "[fetchWeather/convertLocationToLocationName] Parsed location object:",
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
    // console.log(
    //   "[fetchWeather/convertLocationToLocationName] Mapped city name to dataset ID:",
    //   cityName,
    //   datasetId,
    // );
    return { id: datasetId, response: townVillageItem };
  } catch (error) {
    console.error(
      "[fetchWeather/convertLocationToLocationName] Error mapping city name to dataset ID:",
      error,
    );
    throw new Error("Failed to map city name to dataset ID");
  }
}

async function fetchWeather(): Promise<SimplifiedWeatherResponse> {
  // 取得使用者的經緯度
  const { latitude, longitude } = await getLattitudeLongitude();

  // 將經緯度轉換為行政區代碼
  const { id: datasetId, response: locationResponse } = await convertLocationToLocationName(
    latitude,
    longitude,
  );

  // 抓取天氣API
  const response = await fetch(
    `${CWA_OPENAPI_ENDPOINT}/F-D0047-093?locationId=${datasetId}&format=JSON&LocationName=${locationResponse.townName}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch weather data: ${response.status} ${response.statusText}`);
  }

  const weatherData: WeatherResponse = (await response.json()) as WeatherResponse;
  const simplifiedData = transformWeatherData(weatherData);

  console.log(
    `[fetchWeather] Fetched weather data for dataset ID: ${datasetId}, location: ${locationResponse.townName}, Response: `,
    simplifiedData,
  );
  console.debug(`[fetchWeather] Full weather response:`, weatherData);

  // 檢查轉換後的資料是否有dataId，若沒有則丟出錯誤
  if (
    !simplifiedData.records ||
    simplifiedData.records.length === 0 ||
    !simplifiedData.records[0].dataId
  ) {
    toast.error("取得天氣資料異常，請稍後再試或切換至精確定位網路");
  }
  return simplifiedData;
}

export { fetchWeather, getLattitudeLongitude, convertLocationToLocationName };
