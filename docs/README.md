<center><img src="/docs/assets/wordmarks.svg" alt="Logo" width="300" align="right" /></center>

# Browser Homepage Next

Browser Homepage Next是一個基於Vue、Vite及Tailwind CSS的純前端靜態網站，目標是提供一個自訂、與眾不同的瀏覽器首頁，並透過API與[本地伺服器](https://github.com/510208/browser-homepage-next/tree/main/server)進行數據交互。

## 功能

- **自訂化瀏覽器首頁**：使用者可以自由選擇背景圖片、主題色彩、字體樣式，並可自訂快捷方式與小工具。
- **即時數據顯示**：透過API與本地伺服器交互，顯示CPU、記憶體、磁碟空間、網路連線狀態等硬體資訊。
- **相容personal-website-route**：與[personal-website-route](https://github.com/510208/personal-website-route)專案無縫整合，以在無後端環境下運行並保護API金鑰。
- **響應式設計**：網站採用響應式設計，在不同裝置上均能提供良好的使用體驗。
- **輕量快速**：基於Vite構建，網站加載速度快，使用者可以將其安裝為桌面應用程式。
- **開源社群支持**：專案完全開源，歡迎社群貢獻代碼、提出問題或建議，並可透過GitHub Issues與Pull Requests參與專案開發。

## 專案結構說明

```text
browser-homepage-next/
├── public/              # 靜態資源（包含字型、圖示、背景圖片等）
├── dist/                # 本地打包產物（包含 assets、fonts 及 weather-icons）
├── docs/                # 靜態託管產物（預設用於 GitHub Pages 部署）
└───src                  # 前端源碼
  ├───components         # Vue元件（包含各種小工具、快捷方式、主題切換器等）
  │   ├───container      # 四角容器元件（包含快捷方式、天氣、時鐘等）
  │   ├───ui             # shadcn-vue UI元件（包含按鈕、下拉選單、滑桿等）
  │   └───widgets        # 小工具元件（包含天氣、時鐘、名言、書籤等）
  │       ├───avatar     # 使用者頭像元件
  │       ├───bookmarks  # 書籤元件
  │       ├───clock      # 時鐘元件
  │       ├───device     # 硬體資訊元件
  │       ├───quote      # 一言
  │       ├───search-box # 搜尋框元件
  │       ├───trending-badges # 熱門標籤元件
  │       └───weather    # 天氣元件
  ├───consts
  │   └───weather        # 天氣圖示與縣市對應資料集之對應表
  ├───lib
  │   ├───device-info    # 硬體資訊API封裝
  │   ├───trending       # 熱門標籤API封裝
  │   └───weather        # 天氣API封裝
  ├───stores             # Pinia狀態管理（包含天氣、硬體資訊、快捷方式等）
  └───types              # TypeScript型別定義（包含天氣、硬體資訊、快捷方式等）
```

## 技術棧

- **前端框架**：[Vue 3](https://vuejs.org/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/)
- **狀態管理**：[Pinia](https://pinia.vuejs.org/)
- **UI元件庫**：[shadcn-vue](https://shadcn-vue.com/)
- **API與數據交互**：[Browser Homepage Next/Server](https://github.com/510208/browser-homepage-next/tree/main/server), [personal-website-route](https://github.com/510208/personal-website-route)
- **部署與託管**：[GitHub Pages](https://pages.github.com/)

## 安裝與執行

此專案需在有Node.js環境下運行，請先安裝Node.js與pnpm（推薦使用fnm）。請在下載專案後，於專案根目錄下執行以下指令安裝相依性：

```bash
# 安裝fnm（若尚未安裝）
# https://github.com/Schniz/fnm
$ curl -fsSL https://fnm.vercel.app/install | bash  # Linux/macOS
$ iwr https://fnm.vercel.app/install | iex          # PowerShell（Windows）

# 安裝Node.js（若尚未安裝）
$ fnm install 24.3.0
$ fnm use 24.3.0

# 透過corepack安裝pnpm（若尚未安裝）
$ npm install -g corepack
$ corepack enable pnpm

# 安裝專案相依性
$ pnpm install

# 啟動開發伺服器
$ pnpm run dev

# --- 或使用antfu/ni ---
# 安裝antfu/ni（若尚未安裝）
# https://github.com/antfu-collective/ni
$ npm i -g @antfu/ni

# 安裝專案相依性
$ ni

# 啟動開發伺服器
$ nr dev
```

> [!IMPORTANT]
> 請確保已啟動[Server端](./server)

## 注意事項

> [!WARNING]
> 請勿盜連或盜用本專案的轉接API，開發者已對其進行限制。
>
> 若有需要請自行部署[API路由](https://github.com/510208/personal-website-route)以提供API服務。本專案所使用之一切API皆無須付費，請尊重開發者的心血與努力，勿盜連或盜用。

> [!WARNING]
> 字型與圖示等靜態資源皆為開源或免費素材，請勿盜用或商業化使用。
>
> 惟本專案之背景圖像係來自於網際網路，若有侵權請聯繫開發者以便移除。

- 目前系統的天氣資訊係由[中華民國 中央氣象署](https://opendata.cwa.gov.tw/)提供，僅支援台灣地區的縣市天氣資訊。若您位於其他國家或地區，請注意天氣資訊可能無法正確顯示並在終端機中報錯。
- 請確保已啟動[Server端](./server)以提供硬體資訊API，否則硬體資訊將無法正確顯示。
- 如有任何問題或建議，請透過[GitHub Issues](https://github.com/510208/browser-homepage-next/issues)提出，開發者將盡快回覆與處理。若您有興趣參與專案開發，歡迎透過[Pull Requests](https://github.com/510208/browser-homepage-next/pulls)協助專案的開發。
- 此工具原由開發者自行撰寫並給自己使用，如有不足之處請見諒，並歡迎提出建議或協助改善。

## 銘謝

- 感謝各框架的開發者與社群，提供了優秀的工具與資源，使得本專案得以順利完成。
- 感謝Pixiv作者[Bingwei 冰鮪](https://www.pixiv.net/users/32268297)繪製的[插畫作品](https://www.pixiv.net/artworks/81639719), Nice work!
- 感謝提供API服務的開發者與組織
  - [Hitokoto 一言](https://developer.hitokoto.cn/sentence/)
  - [personal-website-route](https://github.com/510208/personal-website-route)
  - [中央氣象署](https://opendata.cwa.gov.tw/)
- 感謝[LigHTTP專案](https://github.com/510208/lighttp)提供優秀的HTTP請求測試工具加快開發進程

---

<div align="center">
  <img height="60" src="https://api.moedog.org/count/@browser-homepage-next?theme=asoul" alt="訪客人數統計" />
  <br />
  <small>由 SamHacker 製作 ｜ 透過 ❤️ 建立</small>
</div>
```
