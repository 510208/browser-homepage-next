import platform
import time
from flask import Flask, jsonify, request
import psutil
from flask_cors import CORS  # 匯入 CORS 套件

app = Flask(__name__)
CORS(app)

SERVER_START_TIME = time.time()

# 進行全域初始化呼叫，讓下一次非阻塞呼叫有基準點可以比對
psutil.cpu_percent(interval=None, percpu=True)


@app.route("/api/status", methods=["GET", "POST"])
def get_hardware_status_fast():
    # 保持對 LigHTTP 的相容性
    request.get_json(force=True, silent=True)

    status = {}

    # 系統基本資訊
    status["system"] = {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "uptime_seconds": int(time.time() - SERVER_START_TIME),
    }

    # CPU 狀態 (完全非阻塞)
    # 將 interval 設為 None，函數會立即返回，不進行等待
    cpu_per_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    status["cpu"] = {
        "model": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "overall_usage_percent": sum(cpu_per_cpu_percent)
        / len(cpu_per_cpu_percent)
        if cpu_per_cpu_percent
        else 0,
        "per_core_usage_percent": cpu_per_cpu_percent,
    }

    # RAM 與 Swap 狀態
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    status["memory"] = {
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
    }

    # 磁碟狀態 (主要根目錄)
    disk_usage = psutil.disk_usage("/")
    status["disk"] = {
        "total_bytes": disk_usage.total,
        "used_bytes": disk_usage.used,
        "free_bytes": disk_usage.free,
        "usage_percent": disk_usage.percent,
    }

    # 網路狀態
    net_io = psutil.net_io_counters()
    status["network"] = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
    }

    # 電池狀態
    battery = psutil.sensors_battery()
    if battery is None:
        status["battery"] = None
    else:
        status["battery"] = {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
        }

    return jsonify(status), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)