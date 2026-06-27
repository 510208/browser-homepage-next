MOCK_CONFIG = {
    "enable_mock": False,
    "system": {
        "os": "Windows",
        "os_release": "11",
        "architecture": "AMD64",
        "uptime_seconds": 3600,
    },
    "cpu": {
        "model": "Intel Core i9-14900K",
        "physical_cores": 8,
        "total_cores": 16,
        "overall_usage_percent": 15.5,
    },
    "memory": {
        "ram": {
            "total_bytes": 34261172224,
            "available_bytes": 17130586112,
            "used_bytes": 17130586112,
            "usage_percent": 50.0,
        },
        "swap": {
            "total_bytes": 4194304000,
            "used_bytes": 1073741824,
            "free_bytes": 3120562176,
            "usage_percent": 25.5,
        },
    },
    "disk": {
        "total_bytes": 1000202272768,
        "used_bytes": 500101136384,
        "free_bytes": 500101136384,
        "usage_percent": 50.0,
    },
    "network": {
        "bytes_sent": 12547896,
        "bytes_recv": 98745231,
    },
    "battery": {
        "percent": 85,
        "power_plugged": True,
    },
    "battery_is_null": False,
}

from textual.message import Message

class FlaskLogMessage(Message):
    """自訂 Textual 訊息類別，用於執行緒安全地傳遞日誌文字"""
    def __init__(self, log_line: str) -> None:
        super().__init__()
        self.log_line = log_line