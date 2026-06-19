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

// ======

export interface WeatherResponse {
  /** 是否成功 */
  success: string;
  /** 結果 */
  result: Result;
  /** 資料筆數 */
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

export type { TownVillagePointResponse, WeatherResponse };
