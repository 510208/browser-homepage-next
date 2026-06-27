import logging
import platform
import sys
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import cpuinfo
import service

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
