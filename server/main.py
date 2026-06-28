import ctypes
import logging
import os
import sys
import threading
import time
import winreg
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import service
import smtc
import click
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import win32api
import win32gui

from config import MOCK_CONFIG, FlaskLogMessage

flask_app = Flask(__name__)
CORS(flask_app)

SERVER_START_TIME = time.time()
tui_instance = None

# 掛載services、Flask與TUI的整合日誌處理器
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.getLogger("werkzeug").setLevel(logging.INFO)

psutil.cpu_percent(interval=None, percpu=True)


# region utils
def _get_primary_network_info():
    """精確篩選實體主要網卡並回傳類型與名稱"""
    net_type = "沒有連線"
    net_name = "N/A"

    try:
        if_addrs = psutil.net_if_addrs()
        if_stats = psutil.net_if_stats()

        VIRTUAL_KEYWORDS = [
            "vmnet",
            "wsl",
            "vbox",
            "virtual",
            "tailscale",
            "pseudo",
            "loopback",
            "vEthernet",
        ]
        primary_interface = None

        for interface, stats in if_stats.items():
            if not stats.isup or interface == "lo":
                continue

            name_lower = interface.lower()
            if any(kw.lower() in name_lower for kw in VIRTUAL_KEYWORDS):
                continue

            has_valid_ipv4 = False
            if interface in if_addrs:
                for addr in if_addrs[interface]:
                    if addr.family == 2:  # AF_INET (IPv4)
                        if not addr.address.startswith("127."):
                            has_valid_ipv4 = True
                            break

            if has_valid_ipv4:
                primary_interface = interface
                break

        if primary_interface:
            net_name = primary_interface
            name_lower = primary_interface.lower()

            if (
                "wlan" in name_lower
                or "wi-fi" in name_lower
                or "wireless" in name_lower
                or "區域連線" in name_lower
            ):
                net_type = "Wi-Fi"
            elif (
                "ethernet" in name_lower
                or "eth" in name_lower
                or "en" in name_lower
                or "乙太網路" in name_lower
            ):
                net_type = "有線網路"
            else:
                net_type = "有線網路"
    except Exception as e:
        logging.error(f"採集網路資訊時發生異常: {e}")

    return net_type, net_name


# endregion


class ColoredTuiLogHandler(logging.Handler):
    """自訂日誌處理器，透過 post_message 將日誌非同步投遞給主事件迴圈"""

    def emit(self, record):
        log_entry = self.format(record)
        if tui_instance is not None:
            tui_instance.post_message(FlaskLogMessage(log_entry))


class TuiAnsiFormatter(logging.Formatter):
    """自訂格式化工具，為不同的日誌層級加上 ANSI 顏色代碼"""

    COLOR_PREFIX = {
        logging.DEBUG: "\033[36m[DEBUG]\033[0m",
        logging.INFO: "\033[32m[INFO ]\033[0m",
        logging.WARNING: "\033[33m[WARN ]\033[0m",
        logging.ERROR: "\033[31m[ERROR]\033[0m",
        logging.CRITICAL: "\033[1;31m[CRIT ]\033[0m",
    }

    def format(self, record):
        time_str = self.formatTime(record, "%H:%M:%S")
        prefix = self.COLOR_PREFIX.get(record.levelno, "[LOG]")
        message = record.getMessage()
        if "GET" in message or "POST" in message:
            message = f"\033[35m{message}\033[0m"
        return f"{time_str} {prefix} {message}"


@flask_app.route("/api/status", methods=["GET", "POST"])
def get_hardware_status_fast():
    request.get_json(force=True, silent=True)

    if MOCK_CONFIG["enable_mock"]:
        # 實時更新模擬數據中的運作時間
        MOCK_CONFIG["system"]["uptime_seconds"] = int(time.time() - SERVER_START_TIME)

        # 處理電池可能為 null 的狀況
        response_data = dict(MOCK_CONFIG)
        if MOCK_CONFIG["battery_is_null"]:
            response_data["battery"] = None
        else:
            response_data["battery"] = MOCK_CONFIG["battery"]

        # 移除內部控制用的非標準欄位再行回傳
        response_data.pop("enable_mock", None)
        response_data.pop("battery_is_null", None)
        return jsonify(response_data), 200

    # 呼叫 service.py 中各硬體獨立的真實數據採集邏輯
    status = {
        "system": service.get_system_info(SERVER_START_TIME),
        "cpu": service.get_cpu_info(),
        "memory": service.get_memory_info(),
        "disk": service.get_disk_info(),
        "network": service.get_network_info(),
        "battery": service.get_battery_info(),
    }

    return jsonify(status), 200


# region 控制本地音訊播放的API端點
@flask_app.route("/api/media", methods=["GET"])
def get_media_info():
    media_info_json = smtc.get_media_info()
    return media_info_json, 200


@flask_app.route("/api/media/next", methods=["POST"])
def play_next_track():
    smtc.next_track()
    return jsonify({"message": "Success to play next track"}), 200


@flask_app.route("/api/media/previous", methods=["POST"])
def play_previous_track():
    smtc.previous_track()
    return jsonify({"message": "Success to play previous track"}), 200


@flask_app.route("/api/media/toggle", methods=["POST"])
def toggle_play_pause():
    smtc.toggle_play()
    return jsonify({"message": "Success to toggle play/pause"}), 200


# endregion


def setup_unified_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.propagate = True
    for handler in werkzeug_logger.handlers[:]:
        werkzeug_logger.removeHandler(handler)

    tui_handler = ColoredTuiLogHandler()
    tui_handler.setFormatter(TuiAnsiFormatter())
    root_logger.addHandler(tui_handler)


def run_flask():
    setup_unified_logging()
    logging.info("Flask 核心服務已全面切換至結構化配置架構...")
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# region Windows 控制台視窗顯示/隱藏功能
# 宣告全域變數以利工作列圖示控制
is_console_visible = True


def toggle_console():
    """切換 Windows 控制台視窗的顯示或完全隱藏狀態（包含工作列）"""
    try:
        # 取得目前的控制台視窗標題
        ct = win32api.GetConsoleTitle()
        # 尋找該視窗的 Handle
        hd = win32gui.FindWindow(None, ct)
        # 0 代表隱藏視窗（SW_HIDE）
        win32gui.ShowWindow(
            hd, 0 if is_console_visible else 5
        )  # 5 代表顯示視窗（SW_SHOW）
    except Exception:
        pass


def hide_console_permanently():
    """強制完全隱藏控制台視窗與工作列標籤"""
    global is_console_visible
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        # 隱藏視窗
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE

        # 修改視窗樣式：移除 WS_EX_APPWINDOW (0x00040000) 並加上 WS_EX_TOOLWINDOW (0x00000080)
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
        style = (style & ~0x00040000) | 0x00000080
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)

        is_console_visible = False


def handle_auto_launch():
    # 將目前執行的腳本寫入 Windows 註冊表以實現開機自動啟動
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "BrowserHomepageMediaServer"

    # 獲取當前執行檔路徑或 Python 腳本路徑
    if getattr(sys, "frozen", False):
        run_cmd = sys.executable
    else:
        run_cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}"'

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, run_cmd)
        winreg.CloseKey(key)
        logging.info("已成功設定開機自動啟動")
    except Exception as e:
        logging.error(f"無法設定開機自動啟動: {str(e)}")


def setup_tray_icon(app_instance):
    # 建立系統工作列圖示與右鍵選單
    tray = QSystemTrayIcon(app_instance)

    # 請替換為您專案中實際的圖示路徑
    tray.setIcon(QIcon("icon.png"))

    menu = QMenu()

    # 建立切換終端機顯示的動作
    toggle_action = QAction("顯示/隱藏終端機", menu)
    toggle_action.triggered.connect(toggle_console)
    menu.addAction(toggle_action)

    # 建立退出程式的動作
    exit_action = QAction("退出程式", menu)
    exit_action.triggered.connect(QApplication.quit)
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.show()
    return tray


# endregion


@click.command()
@click.option(
    "-d", "--dev", "is_dev_mode", is_flag=True, help="啟動開發者模式（啟用 TUI 面板）"
)
@click.option(
    "-s",
    "--silent",
    "is_silent_mode",
    is_flag=True,
    help="啟動靜默模式（隱藏終端機並顯示工作列圖示）",
)
@click.option("--auto-launch", is_flag=True, help="設定程式開機自動啟動")
def main(is_dev_mode, is_silent_mode, auto_launch):
    # 主程式入口，處理所有 CLI 參數邏輯

    # 處理開機自動啟動註冊
    if auto_launch:
        handle_auto_launch()

    # 輸出歡迎訊息
    print(
        r"""
 /$$$$$$$                                                                        /$$   /$$                                                                        
| $$__  $$                                                                      | $$  | $$                                                                        
| $$  \ $$ /$$$$$$   /$$$$$$  /$$  /$$  /$$ /$$$$$$$  /$$$$$$   /$$$$$$         | $$  | $$ /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$$$$$$/ /$$__  $$ /$$__  $$| $$ | $$ | $$ /$$_____/ /$$__  $$ /$$__  $$        | $$$$$$$$ /$$__  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$
| $$__  $$| $$  \__/| $$  \ $$| $$ | $$ | $$|  $$$$$$ | $$$$$$$$| $$  \__/        | $$__  $$| $$  \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$
| $$  \ $$| $$      | $$  | $$| $$ | $$ | $$ \____  $$| $$_____/| $$              | $$  | $$| $$  | $$| $$ | $$ | $$| $$_____/| $$  | $$ /$$__  $$| $$  | $$| $$_____/
| $$$$$$$/| $$      |  $$$$$$/|  $$$$$/$$$$/ /$$$$$$$/|  $$$$$$$| $$              | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$
|_______/ |__/       \______/  \_____/\___/ |_______/  \_______/|__/              |__/  |__/ \______/ |__/ |__/ |__/ \_______/| $$____/  \_______/ \____  $$ \_______/
                                                                                                                              | $$                 /$$  \ $$          
                                                                                                                              | $$                |  $$$$$$/          
                                                                                                                              |__/                 \______/           
  /$$$$$$                                                                                                                                                             
 /$$__  $$                                                                                                                                                            
| $$  \__/ /$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$   /$$$$$$                                                                                                             
|  $$$$$$  /$$__  $$ /$$__  $$|  $$ /$$//$$__  $$ /$$__  $$                                                                                                             
 \____  $$| $$$$$$$$| $$  \__/ \  $$$/ /$$$$$$$$| $$  \__/                                                                                                             
 /$$  \ $$| $$_____/| $$        \  $/  | $$_____/| $$                                                                                                                 
|  $$$$$$/|  $$$$$$$| $$         \_/   |  $$$$$$$| $$                                                                                                                 
 \______/  \_______/|__/                \_______/|__/                                                                                                                 
"""
    )
    logging.info("啟動伺服器中...")

    # 處理靜默模式下的視窗隱藏與 Qt 事件循環
    qt_app = None
    if is_silent_mode:
        hide_console_permanently()
        qt_app = QApplication(sys.argv)
        _tray = setup_tray_icon(qt_app)

    if is_dev_mode:
        from tui_panels import MockControlApp

        tui_app = MockControlApp()

        # 修正：必須將全域變數 tui_instance 指向目前的 tui_app 實例
        global tui_instance
        tui_instance = tui_app

        # 確保呼叫的是 run_flask（其內部會執行 setup_unified_logging() 重新綁定 logger）
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # 啟動 TUI 主事件迴圈
        tui_app.run()
    else:
        print("正在以常規模式啟動伺服器 (連接埠: 5000)...")

        flask_app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
