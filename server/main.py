import ctypes
import logging
import sys
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import service
import smtc
import click
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction

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
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000

is_console_visible = True
tray_icon_instance = None


def start_flask_server(port):
    # 啟動 Flask 伺服器並停用 reloader
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.INFO)
    flask_app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


def set_console_taskbar_visible(visible):
    # 控制終端機視窗在 Windows 工作列（Taskbar）上的顯示或完全隱藏
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if not hwnd:
        return

    # 獲取目前的擴充視窗樣式
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

    if visible:
        # 顯示於工作列：移除工具視窗屬性，加上應用程式視窗屬性
        style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        ctypes.windll.user32.ShowWindow(hwnd, 5)
    else:
        # 從工作列完全消失：移除應用程式視窗屬性，加上工具視窗屬性，並隱藏視窗
        style = (style & ~WS_EX_APPWINDOW) | WS_EX_TOOLWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        ctypes.windll.user32.ShowWindow(hwnd, 0)


def toggle_console():
    # 供工作列選單點擊切換顯示/隱藏終端機狀態
    global is_console_visible
    if is_console_visible:
        set_console_taskbar_visible(False)
        is_console_visible = False
    else:
        set_console_taskbar_visible(True)
        is_console_visible = True


def setup_tray_icon(app_instance):
    # 建立系統工作列圖示與右鍵選單
    global tray_icon_instance
    tray_icon_instance = QSystemTrayIcon(app_instance)

    # 請確保 icon.png 存在於目錄中
    tray_icon_instance.setIcon(QIcon("icon.png"))

    menu = QMenu()

    toggle_action = QAction("顯示/隱藏終端機", menu)
    toggle_action.triggered.connect(toggle_console)
    menu.addAction(toggle_action)

    exit_action = QAction("退出程式", menu)
    exit_action.triggered.connect(QApplication.quit)
    menu.addAction(exit_action)

    tray_icon_instance.setContextMenu(menu)
    tray_icon_instance.show()
    return tray_icon_instance


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
@click.option(
    "--port", default=5000, type=int, help="指定 Flask 伺服器的連接埠（預設 5000）"
)
def main(is_dev_mode, is_silent_mode, port):
    # 主程式入口，分配執行緒以利 Qt 事件循環正常運作
    global is_console_visible

    # 輸出歡迎訊息
    print(
        r"""
 /$$$$$$$                                                                        /$$   /$$                                                                        
| $$__  $$                                                                      | $$  | $$                                                                        
| $$  \ $$ /$$$$$$   /$$$$$$  /$$  /$$  /$$ /$$$$$$$  /$$$$$$   /$$$$$$         | $$  | $$ /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$$$$$$/ /$$__  $$ /$$__  $$| $$ | $$ | $$ /$$_____/ /$$__  $$ /$$__  $$        | $$$$$$$$ /$$__  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$
| $$__  $$| $$  \__/| $$  \ $$| $$ | $$ | $$|  $$$$$$ | $$$$$$$$| $$  \__/        | $$__  $$| $$  \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$
| $$  \ $$| $$      | $$  | $$| $$ | $$ | $$ \____  $$| $$_____/| $$              | $$  | $$| $$  | $$| $$ | $$ | $$| $$_____/| $$  | $$ /$$__  $$| $$  \ $$| $$_____/
| $$$$$$$/| $$      |  $$$$$$/|  $$$$$/$$$$/ /$$$$$$$/|  $$$$$$$| $$              | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$
|_______/ |__/       \______/  \_____/\___/ |_______/  \_______/|__/              |__/  |__/ \______/ |__/ |__/ |__/ \_______/| $$____/  \_______/ \____  $$ \_______/
"""
    )
    logging.info("啟動伺服器中...")

    # 初始化 Qt 應用程式
    qt_app = QApplication(sys.argv)

    # 設定工作列圖示（一律建立，確保功能可用）
    _tray = setup_tray_icon(qt_app)

    # 處理靜默模式下的視窗完全隱藏
    if is_silent_mode:
        set_console_taskbar_visible(False)
        is_console_visible = False

    # 啟動 Flask 背景執行緒
    flask_thread = threading.Thread(
        target=start_flask_server, args=(port,), daemon=True
    )
    flask_thread.start()

    if is_dev_mode:
        from tui_panels import MockControlApp

        tui_app = MockControlApp()

        # 關鍵修改：將會阻塞主執行緒的 TUI 放到背景執行緒執行
        tui_thread = threading.Thread(target=tui_app.run, daemon=True)
        tui_thread.start()

    # 主執行緒一律交由 Qt 事件循環接管，確保滑鼠點擊工作列選單時能即時響應
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore
    main()
