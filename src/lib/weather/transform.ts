import type { WeatherResponse } from "@/types/weatherResponse";
import type { SimplifiedWeatherResponse, SimplifiedLocation } from "@/types/weatherResponse";

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
  "3小時降雨機率": "probabilityOfPrecipitation",
  天氣現象: "weather",
  天氣代碼: "weatherCode",
  天氣預報綜合描述: "weatherDescription",
};

/**
 * 處理複合型或特殊欄位的天氣元素資料解析
 */
function handleSpecialElement(
  rawName: string,
  valObj: any,
  timeKey: string,
  resultLoc: SimplifiedLocation,
): boolean {
  if (rawName === "天氣現象") {
    if (valObj.Weather !== undefined) {
      resultLoc.weather = resultLoc.weather || {};
      resultLoc.weather[timeKey] = String(valObj.Weather);
    }
    if (valObj.WeatherCode !== undefined) {
      resultLoc.weatherCode = resultLoc.weatherCode || {};
      resultLoc.weatherCode[timeKey] = String(valObj.WeatherCode);
    }
    return true;
  }

  if (rawName === "舒適度指數") {
    if (valObj.ComfortIndex !== undefined) {
      resultLoc.comfortIndex = resultLoc.comfortIndex || {};
      resultLoc.comfortIndex[timeKey] = String(valObj.ComfortIndex);
    }
    if (valObj.ComfortIndexDescription !== undefined) {
      resultLoc.comfortIndexDescription = resultLoc.comfortIndexDescription || {};
      resultLoc.comfortIndexDescription[timeKey] = String(valObj.ComfortIndexDescription);
    }
    return true;
  }

  if (rawName === "風速") {
    if (valObj.WindSpeed !== undefined) {
      resultLoc.windSpeed = resultLoc.windSpeed || {};
      resultLoc.windSpeed[timeKey] = String(valObj.WindSpeed);
    }
    if (valObj.BeaufortScale !== undefined) {
      resultLoc.beaufortScale = resultLoc.beaufortScale || {};
      resultLoc.beaufortScale[timeKey] = String(valObj.BeaufortScale);
    }
    return true;
  }

  return false;
}

/**
 * 處理標準單一數值欄位的天氣元素資料解析
 */
function handleStandardElement(
  rawName: string,
  valObj: any,
  timeKey: string,
  resultLoc: SimplifiedLocation,
): void {
  const targetKey = ELEMENT_NAME_MAP[rawName];
  if (!targetKey) {
    return;
  }

  const actualValue =
    valObj[rawName] !== undefined
      ? valObj[rawName]
      : valObj.value !== undefined
        ? valObj.value
        : Object.values(valObj)[0];

  if (actualValue !== undefined && actualValue !== null) {
    if (!(resultLoc as any)[targetKey]) {
      (resultLoc as any)[targetKey] = {};
    }
    (resultLoc as any)[targetKey][timeKey] = String(actualValue);
  }
}

/**
 * 解析單一變數的時間陣列並寫入測站物件
 */
function processWeatherElement(element: any, resultLoc: SimplifiedLocation): void {
  const rawName = element.ElementName;

  element.Time.forEach((t: any) => {
    const timeKey = t.DataTime || t.StartTime || t.EndTime || "unknown_time";
    const valObj = t.ElementValue[0];

    if (!valObj) {
      return;
    }

    const isSpecial = handleSpecialElement(rawName, valObj, timeKey, resultLoc);
    if (isSpecial) {
      return;
    }

    handleStandardElement(rawName, valObj, timeKey, resultLoc);
  });
}

/**
 * 主轉換函式：將原始天氣資料結構轉化為展平後之資料結構
 */
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
          processWeatherElement(element, resultLoc);
        });

        return resultLoc;
      }),
    })),
  };
}

export { transformWeatherData };
