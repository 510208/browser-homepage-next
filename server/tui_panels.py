from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Checkbox, Header, Label, Log
from textual_slider import Slider
from config import MOCK_CONFIG


class MockControlApp(App):
    """用於開發期控制硬體模擬資料的 TUI 面板"""

    # 調整 CSS 佈局，讓滑桿與數值標籤水平對齊並分配合適的寬度
    CSS = """
    Screen {
        align: center top;
        padding: 0 1;
    }
    .frame {
        border: round green;
        padding: 0 1;
        margin: 0;
        height: auto;
    }
    .field {
        margin: 0;
    }
    .slider-row {
        height: 3;
        align: left middle;
    }
    Slider {
        width: 85%;
        height: 3;
        margin: 0;
    }
    .value-lbl {
        width: 15%;
        margin: 1 0 0 1;
        text-align: right;
        color: $accent;
    }
    Checkbox {
        margin: 1 0 0 0;
    }
    Button {
        margin: 1 0 0 0;
        width: 100%;
    }
    #status_lbl {
        text-align: center;
        color: yellow;
        margin: 0;
        height: 1;
    }
    .log-title {
        margin: 1 0 0 0;
    }
    #flask_log {
        border: round blue;
        height: 20;
        background: $background;
    }
    """

    def _get_current_time_str(self) -> str:
        """取得目前時間的字串表示，格式為 HH:MM:SS"""
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return now

    def _update_status_label(self, text: str) -> None:
        lbl = self.query_one("#status_lbl", Label)
        # 取得現在時間
        now = self._get_current_time_str()
        
        # 更新 Label 內容，並加上時間戳記
        lbl.update(f"[{now}] {text}")

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Vertical(classes="frame"):
            yield Label("啟用模擬數據:", classes="field")
            yield Checkbox(value=MOCK_CONFIG["enable_mock"], id="chk_mock")

            yield Label("強制電池回傳 null (桌機模式):", classes="field")
            yield Checkbox(value=MOCK_CONFIG["battery_null"], id="chk_battery")

            # 使用 Horizontal 容器將滑桿與數值標籤並排
            yield Label("CPU 使用率 (%):", classes="field")
            with Horizontal(classes="slider-row"):
                yield Slider(
                    min=0, max=100, step=1, value=int(MOCK_CONFIG["cpu_usage"]), id="sld_cpu"
                )
                yield Label(f"{int(MOCK_CONFIG['cpu_usage'])}%", id="lbl_cpu_val", classes="value-lbl")

            yield Label("RAM 使用率 (%):", classes="field")
            with Horizontal(classes="slider-row"):
                yield Slider(
                    min=0, max=100, step=1, value=int(MOCK_CONFIG["ram_usage"]), id="sld_ram"
                )
                yield Label(f"{int(MOCK_CONFIG['ram_usage'])}%", id="lbl_ram_val", classes="value-lbl")

            yield Label("磁碟使用率 (%):", classes="field")
            with Horizontal(classes="slider-row"):
                yield Slider(
                    min=0,
                    max=100,
                    step=1,
                    value=int(MOCK_CONFIG["disk_usage"]),
                    id="sld_disk",
                )
                yield Label(f"{int(MOCK_CONFIG['disk_usage'])}%", id="lbl_disk_val", classes="value-lbl")

            yield Button("儲存並同步設定", variant="primary", id="btn_save")
            yield Label("", id="status_lbl")

        yield Label("Flask 伺服器輸出日誌:", classes="log-title")
        yield Log(id="flask_log")

    def on_slider_changed(self, event: Slider.Changed) -> None:
        """監聽滑桿數值變更事件，即時更新右側對應的 Label 內容"""
        if event.slider.id == "sld_cpu":
            self.query_one("#lbl_cpu_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_ram":
            self.query_one("#lbl_ram_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_disk":
            self.query_one("#lbl_disk_val", Label).update(f"{int(event.value)}%")

    def write_flask_log(self, message: str) -> None:
        try:
            log_widget = self.query_one("#flask_log", Log)
            log_widget.write_line(message.strip())
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            MOCK_CONFIG["enable_mock"] = self.query_one("#chk_mock", Checkbox).value
            MOCK_CONFIG["battery_null"] = self.query_one("#chk_battery", Checkbox).value
            MOCK_CONFIG["cpu_usage"] = float(self.query_one("#sld_cpu", Slider).value)
            MOCK_CONFIG["ram_usage"] = float(self.query_one("#sld_ram", Slider).value)
            MOCK_CONFIG["disk_usage"] = float(self.query_one("#sld_disk", Slider).value)

            # 檢查是否啟用模擬模式，並更新狀態標籤
            if MOCK_CONFIG["enable_mock"]:
                self._update_status_label("已啟用模擬模式，硬體狀態將回傳模擬數據")
                self.write_flask_log(f"{self._get_current_time_str()} - 已啟用模擬模式，硬體狀態將回傳模擬數據")
            else:
                self._update_status_label("已停用模擬模式，硬體狀態將回傳真實數據")
                self.write_flask_log(f"{self._get_current_time_str()} - 已停用模擬模式，硬體狀態將回傳真實數據")

            self._update_status_label("設定已成功同步至 Flask 後端")