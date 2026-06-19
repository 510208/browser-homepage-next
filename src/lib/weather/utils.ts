import type { WeatherResponse, ElementValue } from "@/types/weatherResponse"; // 假設舊型別在此
import type {
  SimplifiedWeatherResponse,
  SimplifiedLocation,
  TimeValueMap,
} from "@/types/weatherResponse";

/**
 * 將原始 ElementName 映射到新結構的屬性名稱
 */
const ELEMENT_NAME_MAP: Record<string, keyof SimplifiedLocation> = {
  Temperature: "temperature",
  DewPoint: "dewPoint",
  RelativeHumidity: "relativeHumidity",
  ApparentTemperature: "apparentTemperature",
  ComfortIndex: "comfortIndex",
  ComfortIndexDescription: "comfortIndexDescription",
  WindSpeed: "windSpeed",
  BeaufortScale: "beaufortScale",
  WindDirection: "windDirection",
  ProbabilityOfPrecipitation: "probabilityOfPrecipitation",
  Weather: "weather",
  WeatherCode: "weatherCode",
  WeatherDescription: "weatherDescription",
};

export function transformWeatherData(raw: WeatherResponse): SimplifiedWeatherResponse {
  return {
    success: raw.success,
    records: (raw.records?.Locations || []).map((locGroup) => ({
      datasetName: locGroup.DatasetDescription,
      locationsName: locGroup.LocationsName,
      dataId: locGroup.Dataid,
      locations: locGroup.Location.map((loc): SimplifiedLocation => {
        // 初始化基本資訊
        const resultLoc: SimplifiedLocation = {
          locationName: loc.LocationName,
          geocode: loc.Geocode,
          latitude: loc.Latitude,
          longitude: loc.Longitude,
        };

        // 處理天氣元素
        loc.WeatherElement.forEach((element) => {
          const rawName = element.ElementName;
          const targetKey = ELEMENT_NAME_MAP[rawName];

          // 如果這個天氣元素是我們需要的，就進行轉換
          if (targetKey) {
            const timeMap: TimeValueMap = {};

            element.Time.forEach((t) => {
              // 優先取 DataTime，若無則取 StartTime（因預報格式可能不同）
              const timeKey = t.DataTime || t.StartTime || t.EndTime || "unknown_time";

              // 取得該時間點的第一個值 (ElementValueBase 中不為空的那個值)
              const valObj = t.ElementValue[0];
              if (valObj) {
                // 找出這個物件裡真正有值的欄位（例如 valObj.Temperature）
                const actualValue = Object.values(valObj)[0];
                if (actualValue !== undefined) {
                  timeMap[timeKey] = String(actualValue);
                }
              }
            });

            // 動態指派到結果物件中
            (resultLoc as any)[targetKey] = timeMap;
          }
        });

        return resultLoc;
      }),
    })),
  };
}
