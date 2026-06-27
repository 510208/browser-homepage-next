import asyncio
import logging
import platform
import re
import subprocess
import time
import psutil
import cpuinfo


def get_system_info(server_start_time: float) -> dict:
    """採集作業系統基本資訊與運作時間"""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "uptime_seconds": int(time.time() - server_start_time),
    }


def get_cpu_info() -> dict:
    """採集 CPU 型號、核心數與各核心使用率"""
    cpu_per_cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
    logging.debug(f"CPU per-core usage percent: {cpu_per_cpu_percent}")

    logical_cores = psutil.cpu_count(logical=True) or 1
    physical_cores = psutil.cpu_count(logical=False) or 1

    return {
        "model": cpuinfo.get_cpu_info().get("brand_raw", "Unknown CPU"),
        "physical_cores": physical_cores,
        "total_cores": logical_cores,
        "overall_usage_percent": sum(cpu_per_cpu_percent) / len(cpu_per_cpu_percent)
        if cpu_per_cpu_percent
        else 0,
        "per_core_usage_percent": cpu_per_cpu_percent
        if cpu_per_cpu_percent
        else [0] * logical_cores,
    }


def get_memory_info() -> dict:
    """採集實體記憶體 (RAM) 與虛擬記憶體 (Swap) 狀態"""
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    return {
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


def get_disk_info() -> dict:
    """採集根目錄磁碟空間使用狀況"""
    disk_usage = psutil.disk_usage("/")
    return {
        "total_bytes": disk_usage.total,
        "used_bytes": disk_usage.used,
        "free_bytes": disk_usage.free,
        "usage_percent": disk_usage.percent,
    }


async def _get_current_ssid():
    os_name = platform.system()

    try:
        if os_name == "Windows":
            out = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"]
            ).decode("utf-8", errors="ignore")
            match = re.search(r"^\s*SSID\s*:\s*(.*)$", out, re.MULTILINE)
            return match.group(1).strip() if match else "None"

        elif os_name == "Darwin":  # macOS
            cmd = [
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                "-I",
            ]
            out = subprocess.check_output(cmd).decode("utf-8", errors="ignore")
            match = re.search(r"^\s*SSID\s*:\s*(.*)$", out, re.MULTILINE)
            return match.group(1).strip() if match else "None"

        elif os_name == "Linux":
            return subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()

    except Exception:
        return "Unknown/Error"

    return "Unsupported OS"


def _get_primary_network_info() -> tuple:
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
                net_name = asyncio.run(_get_current_ssid())  # 嘗試取得 SSID
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


def get_network_info() -> dict:
    """採集網路傳輸流量、連線類型與網卡名稱"""
    net_io = psutil.net_io_counters()
    net_type, net_name = _get_primary_network_info()

    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "type": net_type,
        "name": net_name,
    }


def get_battery_info() -> dict | None:
    """採集智慧型裝置電池狀態"""
    battery = psutil.sensors_battery()
    if battery is not None:
        return {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
        }
    return None
