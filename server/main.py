import logging
import platform
import sys
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil

from config import MOCK_CONFIG, FlaskLogMessage

flask_app = Flask(__name__)
CORS(flask_app)

SERVER_START_TIME = time.time()
tui_instance = None

# 掛載services、Flask與TUI的整合日誌處理器
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
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

    # 常規真實數據採集邏輯
    cpu_per_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    logical_cores = psutil.cpu_count(logical=True) or 1
    physical_cores = psutil.cpu_count(logical=False) or 1
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    disk_usage = psutil.disk_usage("/")
    net_io = psutil.net_io_counters()
    battery = psutil.sensors_battery()

    status = {
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "uptime_seconds": int(time.time() - SERVER_START_TIME),
        },
        "cpu": {
            "model": platform.processor(),
            "physical_cores": physical_cores,
            "total_cores": logical_cores,
            "overall_usage_percent": sum(cpu_per_cpu_percent) / len(cpu_per_cpu_percent)
            if cpu_per_cpu_percent
            else 0,
            "per_core_usage_percent": cpu_per_cpu_percent
            if cpu_per_cpu_percent
            else [0] * logical_cores,
        },
        "memory": {
            "ram": {
                "total_bytes": virtual_mem.total,
                "available_bytes": virtual_mem.available,
                "used_bytes": virtual_mem.used,
                "usage_percent": virtual_mem.percent,
            },
            "swap": {
                "total_bytes": swap_mem.total,
                "used_bytes": swap_mem.used,
                "free_bytes": swap_mem.free,
                "usage_percent": swap_mem.percent,
            },
        },
        "disk": {
            "total_bytes": disk_usage.total,
            "used_bytes": disk_usage.used,
            "free_bytes": disk_usage.free,
            "usage_percent": disk_usage.percent,
        },
        "network": {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
        },
        "battery": {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
        }
        if battery is not None
        else None,
    }

    return jsonify(status), 200


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


if __name__ == "__main__":
    args = sys.argv[1:]
    is_dev_mode = "-d" in args or "--dev" in args

    # 輸出歡迎訊息
    print(
        r"""
 /$$$$$$$                                                                        /$$   /$$                                                                          
| $$__  $$                                                                      | $$  | $$                                                                          
| $$  \ $$  /$$$$$$   /$$$$$$  /$$  /$$  /$$  /$$$$$$$  /$$$$$$   /$$$$$$       | $$  | $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$$$$$$  /$$__  $$ /$$__  $$| $$ | $$ | $$ /$$_____/ /$$__  $$ /$$__  $$      | $$$$$$$$ /$$__  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$
| $$__  $$| $$  \__/| $$  \ $$| $$ | $$ | $$|  $$$$$$ | $$$$$$$$| $$  \__/      | $$__  $$| $$  \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$
| $$  \ $$| $$      | $$  | $$| $$ | $$ | $$ \____  $$| $$_____/| $$            | $$  | $$| $$  | $$| $$ | $$ | $$| $$_____/| $$  | $$ /$$__  $$| $$  | $$| $$_____/
| $$$$$$$/| $$      |  $$$$$$/|  $$$$$/$$$$/ /$$$$$$$/|  $$$$$$$| $$            | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$
|_______/ |__/       \______/  \_____/\___/ |_______/  \_______/|__/            |__/  |__/ \______/ |__/ |__/ |__/ \_______/| $$____/  \_______/ \____  $$ \_______/
                                                                                                                            | $$                 /$$  \ $$          
                                                                                                                            | $$                |  $$$$$$/          
                                                                                                                            |__/                 \______/           
  /$$$$$$                                                                                                                                                           
 /$$__  $$                                                                                                                                                          
| $$  \__/  /$$$$$$   /$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$                                                                                                         
|  $$$$$$  /$$__  $$ /$$__  $$|  $$  /$$//$$__  $$ /$$__  $$                                                                                                        
 \____  $$| $$$$$$$$| $$  \__/ \  $$/$$/| $$$$$$$$| $$  \__/                                                                                                        
 /$$  \ $$| $$_____/| $$        \  $$$/ | $$_____/| $$                                                                                                              
|  $$$$$$/|  $$$$$$$| $$         \  $/  |  $$$$$$$| $$                                                                                                              
 \______/  \_______/|__/          \_/    \_______/|__/                                                                                                              
                                                                                                                                                                    
"""
    )
    logging.info("啟動伺服器中...")

    if is_dev_mode:
        from tui_panels import MockControlApp

        tui_app = MockControlApp()
        tui_instance = tui_app
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        tui_app.run()
    else:
        print("正在以常規模式啟動伺服器 (連接埠: 5000)...")
        flask_app.run(host="0.0.0.0", port=5000)
