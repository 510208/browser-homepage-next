"""Compatibility exports for the hardware service."""

from .backend.service.hardware import (  # noqa: F401
    get_battery_info,
    get_cpu_info,
    get_disk_info,
    get_memory_info,
    get_network_info,
    get_system_info,
)
