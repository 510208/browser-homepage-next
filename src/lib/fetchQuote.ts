import type QuoteResponse from "@/types/quoteResponse.d";
import { Convert } from "@/types/quoteResponse.d";
import OpenCC from "opencc-js";

async function fetchQuote() {
  try {
    const quote = await fetch("https://v1.hitokoto.cn/");
    if (!quote.ok) {
      throw new Error(`HTTP error! status: ${quote.status}`);
    }
    const quoteResponse = Convert.toQuoteResponse(await quote.text());

    const converter = OpenCC.Converter({ from: "cn", to: "tw" });
    const result = converter(quoteResponse.hitokoto);

    return result;
  } catch (error) {
    console.error("Error fetching quote:", error);
    throw error;
  }
}

export { fetchQuote, type QuoteResponse };