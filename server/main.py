import logging
import sys
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import MOCK_CONFIG
from services import (
    generate_mock_status,
    generate_real_status,
    get_system_base_info,
)

flask_app = Flask(__name__)
CORS(flask_app)

SERVER_START_TIME = time.time()

# 宣告全域的 TUI 實例參考，便於日誌處理器進行內容遞送
tui_instance = None

class TuiLogHandler(logging.Handler):
    """自訂日誌處理器，用於將 Werkzeug/Flask 的輸出重導向至 Textual Log"""
    def emit(self, record):
        log_entry = self.format(record)
        if tui_instance is not None:
            # 透過 Textual 內建的 thread-safe 機制呼叫更新
            tui_instance.call_from_thread(tui_instance.write_flask_log, log_entry)


@flask_app.route("/api/status", methods=["GET", "POST"])
def get_hardware_status_fast():
    request.get_json(force=True, silent=True)

    status = get_system_base_info(SERVER_START_TIME)

    if MOCK_CONFIG["enable_mock"]:
        status = generate_mock_status(status)
    else:
        status = generate_real_status(status)

    return jsonify(status), 200


def run_flask():
    # 設置日誌攔截，將 Flask 輸出引流至自訂的 TuiLogHandler
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.INFO)
    
    # 移除標準終端機輸出處理器，避免干擾 TUI 渲染
    for handler in log.handlers[:]:
        log.removeHandler(handler)
        
    tui_handler = TuiLogHandler()
    tui_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%H:%M:%S"))
    log.addHandler(tui_handler)
    
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    is_dev_mode = "-d" in args or "--dev" in args

    if is_dev_mode:
        from tui_panels import MockControlApp

        tui_app = MockControlApp()
        tui_instance = tui_app  # 註冊實例至全域

        # 啟動背景 Flask 執行緒
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # 啟動 TUI 主程式
        tui_app.run()
    else:
        print("正在以常規模式啟動伺服器 (連接埠: 5000)...")
        flask_app.run(host="0.0.0.0", port=5000)