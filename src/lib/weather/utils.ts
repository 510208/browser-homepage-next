import { WEATHER_ICON_SET } from "@/consts/weather/weatherIconSet";
import type { WeatherResponse } from "@/types/weatherResponse";
import type {
  SimplifiedWeatherResponse,
  SimplifiedLocation,
  TimeValueMap,
} from "@/types/weatherResponse";

/**
 * 將原始 ElementName 映射到新結構的屬性名稱
 */
const ELEMENT_NAME_MAP: Record<string, keyof SimplifiedLocation> = {
  溫度: "temperature",
  露點溫度: "dewPoint",
  相對濕度: "relativeHumidity",
  體感溫度: "apparentTemperature",
  舒適度指數: "comfortIndex",
  舒適度指數說明: "comfortIndexDescription",
  風速: "windSpeed",
  蒲福風級: "beaufortScale",
  風向: "windDirection",
  降雨機率: "probabilityOfPrecipitation",
  天氣現象: "weather",
  天氣代碼: "weatherCode",
  天氣預報綜合描述: "weatherDescription",
};

function transformWeatherData(raw: WeatherResponse): SimplifiedWeatherResponse {
  return {
    success: raw.success,
    records: (raw.records?.Locations || []).map((locGroup) => ({
      datasetName: locGroup.DatasetDescription,
      locationsName: locGroup.LocationsName,
      dataId: locGroup.Dataid,
      locations: locGroup.Location.map((loc): SimplifiedLocation => {
        const resultLoc: SimplifiedLocation = {
          locationName: loc.LocationName,
          geocode: loc.Geocode,
          latitude: loc.Latitude,
          longitude: loc.Longitude,
        };

        loc.WeatherElement.forEach((element) => {
          const rawName = element.ElementName;

          // 🌟 特殊處理：當元素是「天氣現象」時，它同時包含 Weather 與 WeatherCode
          if (rawName === "天氣現象") {
            const weatherMap: TimeValueMap = {};
            const weatherCodeMap: TimeValueMap = {};

            element.Time.forEach((t) => {
              const timeKey = t.DataTime || t.StartTime || t.EndTime || "unknown_time";
              const valObj = t.ElementValue[0] as any;

              if (valObj) {
                // 明確抓取 Weather
                if (valObj.Weather !== undefined) {
                  weatherMap[timeKey] = String(valObj.Weather);
                }
                // 明確抓取 WeatherCode
                if (valObj.WeatherCode !== undefined) {
                  weatherCodeMap[timeKey] = String(valObj.WeatherCode);
                }
              }
            });

            if (Object.keys(weatherMap).length > 0) resultLoc.weather = weatherMap;
            if (Object.keys(weatherCodeMap).length > 0) resultLoc.weatherCode = weatherCodeMap;

            return; // 處理完天氣現象，直接跳過下方的一般邏輯
          }

          const targetKey = ELEMENT_NAME_MAP[rawName];

          if (targetKey) {
            const timeMap: TimeValueMap = {};

            element.Time.forEach((t) => {
              const timeKey = t.DataTime || t.StartTime || t.EndTime || "unknown_time";
              const valObj = t.ElementValue[0];

              if (valObj) {
                const actualValue =
                  (valObj as any).value !== undefined
                    ? (valObj as any).value
                    : Object.values(valObj)[0];

                if (actualValue !== undefined && actualValue !== null) {
                  timeMap[timeKey] = String(actualValue);
                }
              }
            });

            if (Object.keys(timeMap).length > 0) {
              (resultLoc as any)[targetKey] = timeMap;
            }
          }
        });

        return resultLoc;
      }),
    })),
  };
}

/**
 * 根據天氣代碼與時間，取得 Vite 優化後的 SVG 圖片路徑
 * @param weatherCode CWA 天氣代碼 (e.g., "01")
 * @param time "day" 或 "night"
 */
function getWeatherIcon(weatherCode: string, time: "day" | "night"): string {
  const iconName = WEATHER_ICON_SET[weatherCode] || "sunny";

  const fileName = `${iconName}_${time}`;
  const imageUrl = `/weather-icons/${fileName}.svg`;
  // console.log(`嘗試載入天氣圖示: ${fileName}，URL: ${imageUrl}`);

  if (fileName === undefined) {
    // console.warn(`找不到對應的天氣圖示，使用預設圖示: ${fileName}`);
    return new URL(`../assets/weather-icons/sunny_day.svg`, import.meta.url).href;
  }

  return imageUrl;
}

/**
 * 取得指定地點最接近現在時間的 weatherCode
 * @param location 簡化後的地點資料
 * @param targetDate 目標時間（預設為現在 `new Date()`）
 * @returns 最接近的 weatherCode，若無資料則回傳 null
 */
function getClosestWeatherCode(
  location: SimplifiedLocation,
  targetDate: Date = new Date(),
): string | null {
  const weatherCodeMap = location.weatherCode;

  // 1. 防禦機制：檢查該地點是否有 weatherCode 資料
  if (!weatherCodeMap || Object.keys(weatherCodeMap).length === 0) {
    return null;
  }

  const targetTime = targetDate.getTime();
  let closestCode: string | null = null;
  let minDifference = Infinity;

  // 2. 遍歷所有時間點，尋找與目標時間最接近的 Key
  for (const timeString of Object.keys(weatherCodeMap)) {
    // 將 API 的時間字串（例如 "2026-06-19 12:00:00"）轉為時間戳記
    // 注意：若時間字串格式非標準 ISO，可能需要將空白替換為 'T'，例如 timeString.replace(' ', 'T')
    const timeStamp = Date.parse(timeString.replace(" ", "T"));

    // 如果字串格式導致解析失敗，跳過該筆
    if (isNaN(timeStamp)) continue;

    // 計算絕對時間差
    const difference = Math.abs(targetTime - timeStamp);

    // 如果找到更小的時間差，更新結果
    if (difference < minDifference) {
      minDifference = difference;
      closestCode = weatherCodeMap[timeString];
    }
  }

  return closestCode;
}

export { transformWeatherData, getWeatherIcon, getClosestWeatherCode };
export type { SimplifiedWeatherResponse, SimplifiedLocation, TimeValueMap };
