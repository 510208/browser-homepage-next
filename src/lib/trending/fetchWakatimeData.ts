type WakaTimeData = {
  total_seconds: number;
  text: string;
  decimal: string;
  digital: string;
  daily_average: number;
  is_up_to_date: boolean;
  percent_calculated: boolean;
  range: {
    start: string;
    start_date: string;
    start_text: string;
    end: string;
    end_date: string;
    end_text: string;
    timezone: string;
  };
  timeout: number;
};

async function fetchData() {
  const apiUrl =
    "https://api.samhacker.xyz/wakatime_sh?path=/api/v1/users/SamHacker/all_time_since_today";

  const res = await fetch(apiUrl);

  if (!res.ok) {
    throw new Error(`Failed to fetch WakaTime data: ${res.status} ${res.statusText}`);
  }
  const data = (await res.json()).data as WakaTimeData;
  return data;
}

async function parseResponse(): Promise<WakaTimeData> {
  try {
    const data = await fetchData();
    return data as WakaTimeData;
  } catch (error) {
    console.error("Error fetching WakaTime data:", error);
    throw error;
  }
}

export { type WakaTimeData, fetchData, parseResponse };
