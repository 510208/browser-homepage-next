# pyright: basic

import ctypes
import logging
import multiprocessing
import os
import signal
import sys
import threading
import time

import click
from backend.api import create_api
from config import FlaskLogMessage
from flask import Flask
from flask_cors import CORS
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

multiprocessing.freeze_support()

flask_app = Flask(__name__)
CORS(flask_app)

SERVER_START_TIME = time.time()
tui_instance = None

# 掛載services、Flask與TUI的整合日誌處理器
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.getLogger("werkzeug").setLevel(logging.INFO)

flask_app.register_blueprint(create_api(SERVER_START_TIME))


def get_asset_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore[reportAttributeAccessIssue]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ColoredTuiLogHandler(logging.Handler):
    """自訂日誌處理器，透過 post_message 將日誌非同步投遞給主事件迴圈"""

    def emit(self, record):
        log_entry = self.format(record)
        if tui_instance is not None:
            tui_instance.post_message(FlaskLogMessage(log_entry))


class TuiAnsiFormatter(logging.Formatter):
    """自訂格式化工具，為不同的日誌層級加上 ANSI 顏色代碼"""

    def __init__(self):
        self.COLOR_PREFIX: dict[int, str] = {
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


def setup_tray_icon(app_instance):
    # 建立系統工作列圖示與右鍵選單
    global tray_icon_instance
    tray_icon_instance = QSystemTrayIcon(app_instance)

    # 請確保 icon.png 存在於目錄中
    tray_icon_instance.setIcon(QIcon(get_asset_path("icon.png")))

    menu = QMenu()

    exit_action = QAction("退出程式", menu)
    exit_action.triggered.connect(QApplication.quit)
    menu.addAction(exit_action)

    tray_icon_instance.setContextMenu(menu)
    tray_icon_instance.show()
    return tray_icon_instance


# endregion


@click.command(context_settings=dict(ignore_unknown_options=True))
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

    # 啟動 Flask 背景執行緒
    flask_thread = threading.Thread(
        target=start_flask_server, args=(port,), daemon=True
    )
    flask_thread.start()

    if is_dev_mode:
        from tui_panels import MockControlApp

        tui_app = MockControlApp()
        tui_thread = threading.Thread(target=tui_app.run, daemon=True)
        tui_thread.start()

    def sigint_handler(sig, frame):
        logging.info("接收到中斷訊號，正在安全關閉伺服器...")
        qt_app.quit()

    signal.signal(signal.SIGINT, sigint_handler)

    timer = QTimer()
    timer.start(100)
    timer.timeout.connect(lambda: None)

    # 主執行緒一律交由 Qt 事件循環接管，確保滑鼠點擊工作列選單時能即時響應
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    # 檢查標準輸出是否存在，避免在隱藏主控台時因 sys.stdout 為 None 導致崩潰
    if sys.stdout is not None:
        reconfigure = getattr(sys.stdout, "reconfigure", None)

    try:
        main()
    except KeyboardInterrupt:
        logging.info("伺服器已被使用者中斷，正在安全關閉...")
        sys.exit(0)
