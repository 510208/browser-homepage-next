import {
  ABORT_FETCH_MESSAGE,
  FETCH_MESSAGE,
  isApiUrl,
  type AbortFetchMessage,
  type FetchMessage,
  type FetchReply,
} from "./fetchProtocol";

function restoreResponseMetadata(
  response: Response,
  reply: Extract<FetchReply, { ok: true }>,
): Response {
  // 建構子不接受這些欄位；clone() 也需保留實際網路回應的資訊。
  Object.defineProperties(response, {
    url: { value: reply.url },
    redirected: { value: reply.redirected },
    type: { value: reply.type },
    clone: {
      value(this: Response) {
        return restoreResponseMetadata(
          Response.prototype.clone.call(this),
          reply,
        );
      },
    },
  });
  return response;
}

/**
 * 與原生 fetch 使用相同參數並回傳 Response。
 * 僅外掛中的 API 請求透過背景腳本；其他情境直接使用原生 fetch。
 * 外掛訊息會緩衝完整內容，因此不提供即時串流回應。
 */
export const fetch: typeof globalThis.fetch = async (input, init) => {
  const runtime = typeof chrome !== "undefined" ? chrome.runtime : undefined;
  if (!runtime?.id || typeof runtime.sendMessage !== "function") {
    return globalThis.fetch(input, init);
  }

  const url =
    input instanceof Request
      ? input.url
      : new URL(input, globalThis.location?.href).href;
  if (!isApiUrl(url)) {
    return globalThis.fetch(input, init);
  }

  console.debug("[SH Fetch] Intercepted:", {
    url,
    origin: globalThis.location?.origin,
    extensionId: runtime?.id,
    isApiUrl: isApiUrl(url),
  });

  // Request 統一處理 URL、headers、各種 BodyInit 及 init 覆寫。
  const request = new Request(input, init);
  request.signal.throwIfAborted();

  const message: FetchMessage = {
    type: FETCH_MESSAGE,
    id: crypto.randomUUID(),
    url: request.url,
    init: {
      method: request.method,
      headers: Array.from(request.headers.entries()),
      body: request.body
        ? Array.from(new Uint8Array(await request.arrayBuffer()))
        : null,
      cache: request.cache,
      credentials: request.credentials,
      integrity: request.integrity,
      keepalive: request.keepalive,
      mode: request.mode,
      redirect: request.redirect,
      referrer: request.referrer,
      referrerPolicy: request.referrerPolicy,
    },
  };
  request.signal.throwIfAborted();

  return new Promise<Response>((resolve, reject) => {
    const onAbort = () => {
      reject(request.signal.reason);
      const abortMessage: AbortFetchMessage = {
        type: ABORT_FETCH_MESSAGE,
        id: message.id,
      };
      try {
        runtime.sendMessage(abortMessage, () => {
          // 背景腳本可能已結束請求；讀取 lastError 避免未處理的訊息錯誤。
          void runtime.lastError;
        });
      } catch {
        // 外掛失效時仍維持上方已回傳給呼叫端的取消結果。
      }
    };

    request.signal.addEventListener("abort", onAbort, { once: true });
    try {
      runtime.sendMessage(message, (reply: FetchReply | undefined) => {
        request.signal.removeEventListener("abort", onAbort);
        const runtimeError = runtime.lastError;
        if (request.signal.aborted) {
          reject(request.signal.reason);
          return;
        }
        if (runtimeError || !reply) {
          reject(
            new TypeError(
              runtimeError?.message ?? "No background fetch response",
            ),
          );
          return;
        }
        if (!reply.ok) {
          const error =
            reply.error.name === "TypeError"
              ? new TypeError(reply.error.message)
              : new DOMException(reply.error.message, reply.error.name);
          reject(error);
          return;
        }

        try {
          // opaque / opaqueredirect 的 status 為 0，不能傳入 Response 建構子。
          const response =
            reply.status === 0
              ? Response.error()
              : new Response(
                  reply.body === null ? null : new Uint8Array(reply.body),
                  {
                    status: reply.status,
                    statusText: reply.statusText,
                    headers: reply.headers,
                  },
                );
          resolve(restoreResponseMetadata(response, reply));
        } catch (error) {
          reject(error);
        }
      });
    } catch (error) {
      request.signal.removeEventListener("abort", onAbort);
      reject(error);
    }
  });
};
