import platform
import time
import psutil
from config import MOCK_CONFIG

# 全域初始化呼叫，提供非阻塞呼叫基準點
psutil.cpu_percent(interval=None, percpu=True)


def get_system_base_info(server_start_time):
    # 獲取系統基本資訊
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "uptime_seconds": int(time.time() - server_start_time),
    }


def generate_mock_status(status):
    # 依據控制面板設定生成模擬資料
    cores_count = psutil.cpu_count(logical=True) or 1
    status["cpu"] = {
        "model": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False) or 1,
        "total_cores": cores_count,
        "overall_usage_percent": MOCK_CONFIG["cpu_usage"],
        "per_core_usage_percent": [MOCK_CONFIG["cpu_usage"]] * cores_count,
    }

    total_ram = psutil.virtual_memory().total
    used_ram = int(total_ram * (MOCK_CONFIG["ram_usage"] / 100.0))
    status["memory"] = {
        "ram": {
            "total_bytes": total_ram,
            "available_bytes": total_ram - used_ram,
            "used_bytes": used_ram,
            "usage_percent": MOCK_CONFIG["ram_usage"],
        },
        "swap": {
            "total_bytes": 0,
            "used_bytes": 0,
            "free_bytes": 0,
            "usage_percent": 0.0,
        },
    }

    total_disk = psutil.disk_usage("/").total
    used_disk = int(total_disk * (MOCK_CONFIG["disk_usage"] / 100.0))
    status["disk"] = {
        "total_bytes": total_disk,
        "used_bytes": used_disk,
        "free_bytes": total_disk - used_disk,
        "usage_percent": MOCK_CONFIG["disk_usage"],
    }

    status["network"] = {"bytes_sent": 0, "bytes_recv": 0}

    if MOCK_CONFIG["battery_null"]:
        status["battery"] = None
    else:
        status["battery"] = {"percent": 100, "power_plugged": True}

    return status


def generate_real_status(status):
    # 讀取真實系統硬體狀態 (非阻塞模式)
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

    disk_usage = psutil.disk_usage("/")
    status["disk"] = {
        "total_bytes": disk_usage.total,
        "used_bytes": disk_usage.used,
        "free_bytes": disk_usage.free,
        "usage_percent": disk_usage.percent,
    }

    net_io = psutil.net_io_counters()
    status["network"] = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
    }

    battery = psutil.sensors_battery()
    if battery is None:
        status["battery"] = None
    else:
        status["battery"] = {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
        }

    return status