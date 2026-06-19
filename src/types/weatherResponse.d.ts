// #region 鄉鎮市區資料結構
interface TownVillagePointResponse {
  // <townVillageItem>
  // <ctyCode>B</ctyCode>
  // <ctyName>臺中市</ctyName>
  // <townCode>B05</townCode>
  // <townName>北區</townName>
  // <officeCode>BB</officeCode>
  // <officeName>中正</officeName>
  // <sectCode>1002</sectCode>
  // <sectName>錦村段</sectName>
  // <villageCode>66000050030</villageCode>
  // <villageName>建德里</villageName>
  // </townVillageItem>

  /** 縣市代碼 */
  ctyCode: string;
  /** 縣市名稱 */
  ctyName: string;

  /** 鄉鎮市區代碼 */
  townCode: string;
  /** 鄉鎮市區名稱 */
  townName: string;

  /** 地政事務所代碼 */
  officeCode: string;
  /** 地政事務所名稱 */
  officeName: string;

  /** 地段代碼 */
  sectCode: string;
  /** 地段名稱 */
  sectName: string;

  /** 鄰里代碼 */
  villageCode: string;
  /** 鄰里名稱 */
  villageName: string;
}

// #endregion

// #region 天氣資料結構
export interface WeatherResponse {
  /** 是否成功 */
  success: string;
  /** 結果 */
  result: Result;
  /** 資料 */
  records: Records;
}

interface Result {
  /** 欄位資訊 */
  fields: Field[];
}

interface Field {
  /** 欄位 ID */
  id: string;
  /** 欄位類型 */
  type: string;
}

interface Records {
  /** 資料集名稱 */
  Locations: Location[];
}

interface Location {
  /** 資料集描述 */
  DatasetDescription: string;
  /** 位置名稱 */
  LocationsName: string;
  /** 資料 ID */
  Dataid: string;
  /** 位置列表 */
  Location: Location2[];
}

interface Location2 {
  /** 位置名稱 */
  LocationName: string;
  /** 地理編碼 */
  Geocode: string;
  /** 緯度 */
  Latitude: string;
  /** 經度 */
  Longitude: string;
  /** 天氣元素列表 */
  WeatherElement: WeatherElement[];
}

interface WeatherElement {
  /** 天氣元素名稱 */
  ElementName: string;
  /** 時間列表 */
  Time: Time[];
}

interface Time {
  /** 資料時間 */
  DataTime?: string;
  /** 元素值列表 */
  ElementValue: ElementValue[];
  /** 開始時間 */
  StartTime?: string;
  /** 結束時間 */
  EndTime?: string;
}

interface ElementValueBase {
  /** 溫度 */
  Temperature?: string;
  DewPoint?: string;
  RelativeHumidity?: string;
  ApparentTemperature?: string;
  ComfortIndex?: string;
  ComfortIndexDescription?: string;
  WindSpeed?: string;
  BeaufortScale?: string;
  WindDirection?: string;
  ProbabilityOfPrecipitation?: string;
  Weather?: string;
  WeatherCode?: string;
  WeatherDescription?: string;
}
type AtLeastOne<T, U = { [K in keyof T]: Pick<T, K> }> = Partial<T> & U[keyof U];
export type ElementValue = AtLeastOne<ElementValueBase>;

// #endregion

// #region 展平後的天氣資料結構
export interface SimplifiedWeatherResponse {
  /** 是否成功 */
  success: string;
  /** 資料集列表 */
  records: SimplifiedRecord[];
}

interface SimplifiedRecord {
  /** 資料集名稱 (原本的 DatasetDescription) */
  datasetName: string;
  /** 位置名稱 (原本的 LocationsName) */
  locationsName: string;
  /** 資料 ID (原本的 Dataid) */
  dataId: string;
  /** 各地點的天氣狀態列表 */
  locations: SimplifiedLocation[];
}

/**
 * 將時間對應到數值的 Map 結構
 * 例如: { "2026-06-19 12:00:00": "32" }
 */
export type TimeValueMap = Record<string, string>;
export interface SimplifiedLocation {
  /** 地點名稱 (如：板橋區、西屯區) */
  locationName: string;
  /** 地理編碼 */
  geocode: string;
  /** 緯度 */
  latitude: string;
  /** 經度 */
  longitude: string;

  // 以下為展平後的天氣數據，若該測站沒提供則為 undefined
  temperature?: TimeValueMap;
  dewPoint?: TimeValueMap;
  relativeHumidity?: TimeValueMap;
  apparentTemperature?: TimeValueMap;
  comfortIndex?: TimeValueMap;
  comfortIndexDescription?: TimeValueMap;
  windSpeed?: TimeValueMap;
  beaufortScale?: TimeValueMap;
  windDirection?: TimeValueMap;
  probabilityOfPrecipitation?: TimeValueMap;
  weather?: TimeValueMap;
  weatherCode?: TimeValueMap;
  weatherDescription?: TimeValueMap;
}
// #endregion

export type { TownVillagePointResponse, WeatherResponse, SimplifiedWeatherResponse };