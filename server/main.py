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

# 初始化 Flask 應用程式
flask_app = Flask(__name__)
CORS(flask_app)

SERVER_START_TIME = time.time()


@flask_app.route("/api/status", methods=["GET", "POST"])
def get_hardware_status_fast():
    # 保持對 LigHTTP 的相容性
    request.get_json(force=True, silent=True)

    status = get_system_base_info(SERVER_START_TIME)

    if MOCK_CONFIG["enable_mock"]:
        status = generate_mock_status(status)
    else:
        status = generate_real_status(status)

    return jsonify(status), 200


def run_flask():
    # 關閉 Flask 預設的啟動提示文字以避免干擾終端機輸出
    import logging

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    # 解析命令列參數，檢查是否存在指定的開發期旗標
    args = sys.argv[1:]
    is_dev_mode = "-d" in args or "--dev" in args

    if is_dev_mode:
        # 延遲匯入 Textual 元件，常規生產模式運作時無需加載 Textual 套件
        from tui_panels import MockControlApp

        # 開啟開發模式：透過多執行緒在背景啟動 Flask，並在主執行緒執行 TUI
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # 啟動從 tui_panels 匯入的 TUI 面板
        tui_app = MockControlApp()
        tui_app.run()
    else:
        # 常規模式：直接在主執行緒啟動 Flask 伺服器
        print("正在以常規模式啟動伺服器 (連接埠: 5000)...")
        flask_app.run(host="0.0.0.0", port=5000)