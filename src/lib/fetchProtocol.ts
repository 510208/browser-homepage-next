// Chrome 訊息使用 JSON 序列化，因此以數字陣列傳遞二進位內容。
export const FETCH_MESSAGE = "samhacker:fetch";
export const ABORT_FETCH_MESSAGE = "samhacker:abort-fetch";
const API_ORIGIN = "https://api.samhacker.xyz";

export function isApiUrl(url: string): boolean {
  return new URL(url).origin === API_ORIGIN;
}

export type FetchMessage = {
  type: typeof FETCH_MESSAGE;
  id: string;
  url: string;
  init: Pick<
    RequestInit,
    | "method"
    | "cache"
    | "credentials"
    | "integrity"
    | "keepalive"
    | "mode"
    | "redirect"
    | "referrer"
    | "referrerPolicy"
  > & {
    headers: [string, string][];
    body: number[] | null;
  };
};

export type AbortFetchMessage = {
  type: typeof ABORT_FETCH_MESSAGE;
  id: string;
};

export type FetchReply =
  | {
      ok: true;
      status: number;
      statusText: string;
      headers: [string, string][];
      body: number[] | null;
      url: string;
      redirected: boolean;
      type: ResponseType;
    }
  | { ok: false; error: { name: string; message: string } };
