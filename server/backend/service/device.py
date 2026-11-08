# pyright: basic

"""Device and hardware status aggregation."""

import time

from config import MOCK_CONFIG

from ..service import hardware


def get_status(start_time: float) -> dict:
    if MOCK_CONFIG["enable_mock"]:
        MOCK_CONFIG["system"]["uptime_seconds"] = int(time.time() - start_time)
        status = dict(MOCK_CONFIG)
        status["battery"] = (
            None if MOCK_CONFIG["battery_is_null"] else MOCK_CONFIG["battery"]
        )
        status.pop("enable_mock", None)
        status.pop("battery_is_null", None)
        return status
    return {
        "system": hardware.get_system_info(start_time),
        "cpu": hardware.get_cpu_info(),
        "memory": hardware.get_memory_info(),
        "disk": hardware.get_disk_info(),
        "network": hardware.get_network_info(),
        "battery": hardware.get_battery_info(),
    }
