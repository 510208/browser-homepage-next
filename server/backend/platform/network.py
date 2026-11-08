"""Platform-specific network details."""

import platform
import re
import subprocess
from pathlib import Path


def is_wireless(interface: str) -> bool:
    return (
        platform.system() == "Linux"
        and Path("/sys/class/net", interface, "wireless").is_dir()
    )


from typing import Any


def _get_windows_startupinfo() -> Any | None:
    """取得 Windows 隱藏命令視窗的設定。"""
    startupinfo_type = getattr(subprocess, "STARTUPINFO", None)
    show_window_flag = getattr(subprocess, "STARTF_USESHOWWINDOW", None)

    if startupinfo_type is None or show_window_flag is None:
        return None

    startup = startupinfo_type()
    startup.dwFlags |= show_window_flag

    return startup


def get_current_ssid(interface: str) -> str:
    system = platform.system()

    try:
        if system == "Windows":
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                startupinfo=_get_windows_startupinfo(),
                timeout=3,
            ).decode(errors="replace")

            match = re.search(
                r"^\s*SSID\s*:\s*(.*)$",
                output,
                re.MULTILINE,
            )

            return match.group(1).strip() if match else "None"

        elif system == "Linux":
            # 優先使用 NetworkManager
            try:
                output = subprocess.check_output(
                    [
                        "nmcli",
                        "--terse",
                        "--escape",
                        "no",
                        "--fields",
                        "IN-USE,SSID",
                        "device",
                        "wifi",
                        "list",
                        "ifname",
                        interface,
                    ],
                    stderr=subprocess.DEVNULL,
                    timeout=3,
                ).decode(errors="replace")

                for line in output.splitlines():
                    if line.startswith("*:"):
                        return line[2:].strip() or "None"

            except (OSError, subprocess.SubprocessError):
                pass

            # 備援：wireless_tools
            try:
                output = (
                    subprocess.check_output(
                        ["iwgetid", interface, "-r"],
                        stderr=subprocess.DEVNULL,
                        timeout=3,
                    )
                    .decode(errors="replace")
                    .strip()
                )

                if output:
                    return output

            except (OSError, subprocess.SubprocessError):
                pass

            return "None"

        elif system == "Darwin":
            output = subprocess.check_output(
                [
                    "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                    "-I",
                ],
                timeout=3,
            ).decode(errors="replace")

            match = re.search(
                r"^\s*SSID\s*:\s*(.*)$",
                output,
                re.MULTILINE,
            )

            return match.group(1).strip() if match else "None"

    except (OSError, subprocess.SubprocessError):
        return "Unknown/Error"

    return "Unsupported OS"
