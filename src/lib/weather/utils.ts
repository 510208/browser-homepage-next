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

export function transformWeatherData(raw: WeatherResponse): SimplifiedWeatherResponse {
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
          const targetKey = ELEMENT_NAME_MAP[rawName];

          // 當成功比對到中文的天氣元素名稱時才進行轉換
          if (targetKey) {
            const timeMap: TimeValueMap = {};

            element.Time.forEach((t) => {
              const timeKey = t.DataTime || t.StartTime || t.EndTime || "unknown_time";
              const valObj = t.ElementValue[0];

              if (valObj) {
                // 優先取氣象署標準的 value 欄位，若無則依據原物件屬性動態取值
                const actualValue =
                  (valObj as any).value !== undefined
                    ? (valObj as any).value
                    : Object.values(valObj)[0];

                if (actualValue !== undefined && actualValue !== null) {
                  timeMap[timeKey] = String(actualValue);
                }
              }
            });

            // 確保該欄位有轉換出時間資料才進行寫入，避免產生空物件
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
