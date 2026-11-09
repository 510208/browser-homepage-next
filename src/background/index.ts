import {
  ABORT_FETCH_MESSAGE,
  FETCH_MESSAGE,
  isApiUrl,
  type AbortFetchMessage,
  type FetchMessage,
  type FetchReply,
} from "../lib/fetchProtocol";

const pendingRequests = new Map<string, AbortController>();

async function fetchApi(message: FetchMessage): Promise<FetchReply> {
  const controller = new AbortController();

  try {
    if (!isApiUrl(message.url)) {
      throw new TypeError(
        "Background fetch only supports https://api.samhacker.xyz",
      );
    }

    pendingRequests.set(message.id, controller);

    console.debug("[Background Fetch] Starting:", {
      id: message.id,
      url: message.url,
      origin: new URL(message.url).origin,
      method: message.init.method,
      mode: message.init.mode,
      credentials: message.init.credentials,
    });

    const response = await globalThis.fetch(message.url, {
      ...message.init,
      body:
        message.init.body === null ? null : new Uint8Array(message.init.body),
      signal: controller.signal,
    });

    console.debug("[Background Fetch] Response received:", {
      id: message.id,
      status: response.status,
      statusText: response.statusText,
      url: response.url,
      redirected: response.redirected,
      type: response.type,
      headers: Array.from(response.headers.entries()),
    });

    const body = response.body
      ? Array.from(new Uint8Array(await response.arrayBuffer()))
      : null;

    return {
      ok: true,
      status: response.status,
      statusText: response.statusText,
      headers: Array.from(response.headers.entries()),
      body,
      url: response.url,
      redirected: response.redirected,
      type: response.type,
    };
  } catch (error) {
    console.error("[Background Fetch] Failed:", {
      id: message.id,
      url: message.url,
      error,
      name: error instanceof Error ? error.name : typeof error,
      message: error instanceof Error ? error.message : String(error),
    });

    return {
      ok: false,
      error: {
        name: error instanceof Error ? error.name : "TypeError",
        message: error instanceof Error ? error.message : String(error),
      },
    };
  } finally {
    pendingRequests.delete(message.id);
  }
}

chrome.runtime.onMessage.addListener(
  (message: FetchMessage | AbortFetchMessage | null, sender, sendResponse) => {
    if (
      sender.id !== chrome.runtime.id ||
      !message ||
      typeof message.id !== "string"
    ) {
      return false;
    }
    if (message.type === ABORT_FETCH_MESSAGE) {
      pendingRequests.get(message.id)?.abort();
      sendResponse();
      return false;
    }
    if (message.type !== FETCH_MESSAGE) {
      return false;
    }

    void fetchApi(message).then(sendResponse);
    // Chrome 與 Firefox 的 chrome.* API 均以此保留非同步回覆通道。
    return true;
  },
);
