type YouTubeData = {
  id: string;
  statistics: {
    viewCount: number;
    subscriberCount: number;
    hiddenSubscriberCount: boolean;
    videoCount: number;
  };
};

async function fetchData() {
  const apiUrl =
    "https://api.samhacker.xyz/youtube/v3/channels?id=UC6orwHdQNVzwHsA6M7HYD9g&part=statistics,id";

  const res = await fetch(apiUrl);

  if (!res.ok) {
    console.error(`Failed to fetch YouTube data: ${res.status} ${res.statusText}`);
    return null;
  }

  const data = await res.json();
  const ytData = data.items[0] as YouTubeData;
  return ytData;
}

async function parseResponse(): Promise<YouTubeData> {
  const data = await fetchData();
  if (!data) {
    throw new Error("Failed to fetch YouTube data");
  }

  return data as YouTubeData;
}

export { type YouTubeData, fetchData, parseResponse };