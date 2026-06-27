from textual.app import App, ComposeResult
from textual.widgets import Button, Checkbox, Header, Label
from textual_slider import Slider
from config import MOCK_CONFIG


class MockControlApp(App):
    """用於開發期控制硬體模擬資料的 TUI 面板"""

    # 定義終端機介面的樣式與佈局
    CSS = """
    Screen {
        align: center middle;
        padding: 1 2;
    }
    .field {
        margin: 1 0;
    }
    Slider {
        width: 100%;
    }
    Button {
        margin-top: 1;
        width: 100%;
    }
    #status_lbl {
        text-align: center;
        color: yellow;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Label("啟用模擬數據:", classes="field")
        yield Checkbox(value=MOCK_CONFIG["enable_mock"], id="chk_mock")

        yield Label("強制電池回傳 null (桌機模式):", classes="field")
        yield Checkbox(value=MOCK_CONFIG["battery_null"], id="chk_battery")

        yield Label("CPU 使用率 (%):", classes="field")
        yield Slider(
            min=0, max=100, step=1, value=int(MOCK_CONFIG["cpu_usage"]), id="sld_cpu"
        )

        yield Label("RAM 使用率 (%):", classes="field")
        yield Slider(
            min=0, max=100, step=1, value=int(MOCK_CONFIG["ram_usage"]), id="sld_ram"
        )

        yield Label("磁碟使用率 (%):", classes="field")
        yield Slider(
            min=0,
            max=100,
            step=1,
            value=int(MOCK_CONFIG["disk_usage"]),
            id="sld_disk",
        )

        yield Button("儲存並同步設定", variant="primary", id="btn_save")
        yield Label("", id="status_lbl")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            # 將 TUI 元件當前的數值寫回全域的 MOCK_CONFIG 字典
            MOCK_CONFIG["enable_mock"] = self.query_one("#chk_mock", Checkbox).value
            MOCK_CONFIG["battery_null"] = self.query_one("#chk_battery", Checkbox).value
            MOCK_CONFIG["cpu_usage"] = float(self.query_one("#sld_cpu", Slider).value)
            MOCK_CONFIG["ram_usage"] = float(self.query_one("#sld_ram", Slider).value)
            MOCK_CONFIG["disk_usage"] = float(self.query_one("#sld_disk", Slider).value)

            # 更新狀態提示文字
            lbl = self.query_one("#status_lbl", Label)
            lbl.update(" [設定已成功同步至 Flask 後端] ")