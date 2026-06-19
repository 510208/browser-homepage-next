import type QuoteResponse from "@/types/quoteResponse";
import { Convert } from "@/types/quoteResponse";

async function fetchQuote() {
  try {
    const quote = await fetch("https://v1.hitokoto.cn/");
    if (!quote.ok) {
      throw new Error(`HTTP error! status: ${quote.status}`);
    }
    const quoteResponse = Convert.toQuoteResponse(await quote.text());
    return quoteResponse.hitokoto;
  } catch (error) {
    console.error("Error fetching quote:", error);
    throw error;
  }
}

export { fetchQuote, type QuoteResponse };