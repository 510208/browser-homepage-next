const WEATHER_ICON_SET: Record<string, string> = {
  // weather code -> icon file name
  // FUCK CWA
  "01": "sunny", // 晴天
  "02": "sunny_multi_cloud",
  "03": "few_clouds",
  "04": "scattered_clouds",
  "05": "scattered_clouds",
  "06": "scattered_clouds",
  "07": "broken_clouds",
  "08": "rain",
  "09": "shower_rain",
  "10": "shower_rain",
  "11": "rain",
  "12": "rain",
  "13": "shower_rain",
  "14": "shower_rain",
  "15": "thunderstorm",
  "16": "thunderstorm",
  "17": "thunderstorm",
  "18": "thunderstorm",
  "19": "sunny", // 晴午後多雲局部雨
  "20": "broken_clouds", // 多雲午後局部雨
  "21": "sunny",
  "22": "broken_clouds",
  "23": "shower_rain",
  "24": "mist",
  "25": "mist",
  "26": "mist",
  "27": "mist",
  "28": "mist",
  "29": "shower_rain",
  "30": "shower_rain",
  "31": "mist",
  "32": "mist",
  "33": "thunder",
  "34": "thunder",
  "35": "thunder",
  "36": "thunder",
  "37": "snow",
  "38": "mist",
  "39": "mist",
  "40": "mist",
  "41": "mist",
  "42": "snow",
};

// 所有天氣圖示種類
const WEATHER_ICON_TYPES = Object.values(WEATHER_ICON_SET);

/**
 * 根據天氣代碼與時間，取得 Vite 優化後的 SVG 圖片路徑
 * @param weatherCode CWA 天氣代碼 (e.g., "01")
 * @param time "day" 或 "night"
 */
function getWeatherIcon(weatherCode: string, time: "day" | "night"): string {
  const iconName = WEATHER_ICON_SET[weatherCode] || "sunny";

  const fileName = `${iconName}_${time}.svg`;

  const imageUrl = new URL(`../assets/weather-icons/${fileName}`, import.meta.url).href;

  return imageUrl;
}

export { WEATHER_ICON_SET, WEATHER_ICON_TYPES, getWeatherIcon };