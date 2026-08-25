import type QuoteResponse from "@/types/quoteResponse.d";
import { Convert } from "@/types/quoteResponse.d";

let converterInstance: ((text: string) => string) | null = null;
let openCCPromise: Promise<void> | null = null;

// 非同步載入
async function getConverter() {
  if (converterInstance) return converterInstance;

  if (!openCCPromise) {
    openCCPromise = (async () => {
      // 離線動態導入，不會打包進首屏 main chunk
      const OpenCC = await import("opencc-js");
      converterInstance = OpenCC.Converter({ from: "cn", to: "tw" });
    })();
  }

  await openCCPromise;
  return converterInstance!;
}

// 提早呼叫預載入
export function preloadOpenCC() {
  getConverter();
}

async function fetchQuote() {
  try {
    // 同步送出請求
    const quotePromise = fetch("https://v1.hitokoto.cn/");
    const converterPromise = getConverter();

    const [quote, converter] = await Promise.all([quotePromise, converterPromise]);

    if (!quote.ok) {
      throw new Error(`HTTP error! status: ${quote.status}`);
    }

    const quoteResponse = Convert.toQuoteResponse(await quote.text());
    return converter(quoteResponse.hitokoto);
  } catch (error) {
    console.error("Error fetching quote:", error);
    throw error;
  }
}

export { fetchQuote, type QuoteResponse };
