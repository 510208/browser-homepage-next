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

export type { TownVillagePointResponse };
