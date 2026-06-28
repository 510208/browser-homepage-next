<center><img src="/docs/assets/wordmarks.svg" alt="Logo" width="300" align="right" /></center>

# Browser Homepage Next Server side

這是一個簡單的Flask伺服器，提供一個API來獲取瀏覽器首頁的數據、控制音樂播放的相關本地服務。本地服務。對於抓取天氣、一言等數據的原始碼，請參考[510208/personal-website-route](https://github.com/510208/personal-website-route/blob/main/src/routes/cwa.js)與[Hitokoto 一言](https://developer.hitokoto.cn/sentence/)；對於前端靜態網站的生成，請參考[510208/browser-homepage-next](https://github.com/510208/browser-homepage-next)

## 功能

- **結構化硬體數據採集**：透過 `psutil` 與 `py-cpuinfo` 等庫，獨立模組化採集 CPU（各核心與整體使用率）、實體記憶體（RAM）、交換空間（Swap）、磁碟空間（Disk）及電池狀態。
- **實體網路連線智能過濾**：自動識別並過濾虛擬機（VMware、Hyper-V）、WSL 子系統及 VPN（如 Tailscale）創建的虛擬硬體網卡，精確鎖定並回傳當前主要上網的實體 Wi-Fi 或有線網路之連線類型與網卡名稱。
- **Textual TUI 開發者面板**：內建功能完整的終端機 UI（TUI）控制面板，開發者可在不影響前端請求的情況下，即時透過下拉式選單與滑桿（Slider）模擬修改全域硬體指標數據。
- **Windows 靜默整合與托盤控制**：透過 `pystray` 與 `PIL`，將伺服器整合至 Windows 系統托盤（System Tray），隱藏終端機視窗則由 Pyinstaller 打包後的執行檔自動完成，並提供右鍵選單退出程式功能。

## 資料夾架構

```
server/
├── config.py            # 全域組態設定、Flask 模擬數據快取 (MOCK_CONFIG) 及訊息模型定義
├── service.py           # 真實硬體採集核心（包含各硬體獨立函數與主要實體網卡判定邏輯）
├── main.py              # 程式主入口，負責 Flask API 路由、系統托盤、CLI 參數解析與日誌代理
├── tui_panels.py        # 基於 Textual 的 TUI 控制面板實作（包含下拉選單與數據同步寫回邏輯）
├── smtc.py              # 系統媒體傳輸控制（System Media Transport Controls）整合模組
├── styles.tcss          # TUI 面板的樣式表檔案
├── icon.png             # 系統工作列（Tray Icon）使用的圖示檔案
├── main.spec            # PyInstaller 打包組態設定檔
├── pyproject.toml       # 專案相依性管理（基於 uv 規格）
└── uv.lock              # 相依性精確鎖定檔
```

## 技術棧

- **網頁框架**：[Flask](https://flask.palletsprojects.com/en/stable/), [Flask-CORS](https://pypi.org/project/flask-cors/)
- **硬體指標採集**：[psutil](https://pypi.org/project/psutil/), [py-cpuinfo](https://pypi.org/project/py-cpuinfo/)
- **終端機 UI**：[Textual](https://textual.textualize.io/), [textual-slider](https://github.com/TomJGooding/textual-slider)
- **Windows 整合**：[PySide6](https://pypi.org/project/PySide6/) (QSystemTrayIcon, QAction, QMenu), [ctypes](https://docs.python.org/3/library/ctypes.html), [winreg](https://docs.python.org/3/library/winreg.html), [pystray](https://pypi.org/project/pystray/), [Pillow](https://pypi.org/project/Pillow/)
- **CLI 解析**：[Click](https://pypi.org/project/Click/)
- **套件管理**：[uv](https://github.com/astral-sh/uv)

## 安裝與執行

此專案的預編譯版本目前僅有Windows x64，請至[Releases](https://github.com/510208/browser-homepage-next/releases/latest)下載。如需自行編譯，請安裝uv套件管理器，並使用以下指令安裝相依性：

```bash
$ uv install
```

安裝相依性後，可直接在本地啟動Flask伺服器，並透過瀏覽器訪問 `http://localhost:5000` 來查看API回傳的JSON數據。若要啟動TUI控制面板，請在終端機中執行：

```bash
$ uv run main.py
```

如需手動編譯可用的執行檔，請參考以下指令。相關設定可在 `main.spec` 中修改，並確保已安裝 [PyInstaller](https://pyinstaller.org/en/stable/)。

```bash
$ uv run pyinstaller .\main.spec
```

`examples`資料夾中包含了可用於測試的LigHTTP JSON範例，您可以使用LigHTTP來模擬API請求。該資料夾中的LigHTTP JSON是由[`LigHTTP v0.4.2-hotfix1`](https://github.com/510208/lighttp/releases/tag/app-v0.4.2)生成，應可被[`LigHTTP v0.2.0`](https://github.com/510208/lighttp/releases/tag/app-v0.2.0)以上版本正確解析。若您使用的是舊版本的LigHTTP，請升級至最新版本以確保兼容性。

各端點的curl請求範例亦可在 `examples` 資料夾中找到，如有在原始碼中修改Flask端口，請確保在使用LigHTTP或curl時指定正確的端口號。

## 注意事項

- 本專案僅支援Windows x64平台，其他平台的相容性未經測試。
- 此伺服器應且僅應在本地網路環境中使用，請勿將其暴露於網際網路，以避免潛在的安全風險。
- 如有更新建議或問題，歡迎透過GitHub Issues提交，我們將盡快回應。

---

<div align="center">
  <img height="60" src="https://api.moedog.org/count/@browser-homepage-next?theme=asoul" alt="訪客人數統計" />
  <br />
  <small>由 SamHacker 製作 ｜ 透過 ❤️ 建立</small>
</div>