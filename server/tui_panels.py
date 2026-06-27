import random

from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import (
    Button,
    Checkbox,
    Header,
    Label,
    Log,
    Input,
    TabPane,
    TabbedContent,
)
from textual_slider import Slider
from config import MOCK_CONFIG, FlaskLogMessage


class MockControlApp(App):
    """用於開發期控制與修改全域傳回數據的 TUI 面板"""

    CSS_PATH = "styles.tcss"

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

    def compose(self) -> ComposeResult:
        yield Header()

        # 外層使用外框包覆
        with Vertical(classes="frame"):
            # 引入分頁容器
            with TabbedContent():
                # 分頁 1：核心與系統基本資訊
                with TabPane("系統與控制", id="tab_system"):
                    with ScrollableContainer():
                        yield Label("核心控制設定", classes="field")
                        yield Label("啟用模擬數據:")
                        yield Checkbox(value=MOCK_CONFIG["enable_mock"], id="chk_mock")

                        yield Label("系統資訊控制", classes="field")
                        yield Label("作業系統名稱 (OS):")
                        yield Input(value=str(MOCK_CONFIG["system"]["os"]), id="inp_os")
                        yield Label("作業系統發行版本 (Release):")
                        yield Input(
                            value=str(MOCK_CONFIG["system"]["os_release"]),
                            id="inp_release",
                        )
                        yield Label("系統架構 (Architecture):")
                        yield Input(
                            value=str(MOCK_CONFIG["system"]["architecture"]),
                            id="inp_arch",
                        )

                # 分頁 2：硬體核心 (CPU & 記憶體)
                with TabPane("運算與記憶體", id="tab_hardware"):
                    with ScrollableContainer():
                        yield Label("CPU 數據控制", classes="field")
                        yield Label("CPU 型號名稱 (Model):")
                        yield Input(
                            value=str(MOCK_CONFIG["cpu"]["model"]), id="inp_cpu_model"
                        )
                        yield Label("物理核心數 (Physical Cores):")
                        yield Input(
                            value=str(MOCK_CONFIG["cpu"]["physical_cores"]),
                            id="inp_cpu_phys",
                        )
                        yield Label("邏輯核心數 (Total Cores):")
                        yield Input(
                            value=str(MOCK_CONFIG["cpu"]["total_cores"]),
                            id="inp_cpu_total",
                        )

                        yield Label("CPU 總體使用率 (%):")
                        with Horizontal(classes="slider-row"):
                            yield Slider(
                                min=0,
                                max=100,
                                step=1,
                                value=int(MOCK_CONFIG["cpu"]["overall_usage_percent"]),
                                id="sld_cpu",
                            )
                            yield Label(
                                f"{int(MOCK_CONFIG['cpu']['overall_usage_percent'])}%",
                                id="lbl_cpu_val",
                                classes="value-lbl",
                            )

                        yield Label("記憶體數據控制", classes="field")
                        yield Label("RAM 使用率 (%):")
                        with Horizontal(classes="slider-row"):
                            yield Slider(
                                min=0,
                                max=100,
                                step=1,
                                value=int(
                                    MOCK_CONFIG["memory"]["ram"]["usage_percent"]
                                ),
                                id="sld_ram",
                            )
                            yield Label(
                                f"{int(MOCK_CONFIG['memory']['ram']['usage_percent'])}%",
                                id="lbl_ram_val",
                                classes="value-lbl",
                            )

                        yield Label("Swap 使用率 (%):")
                        with Horizontal(classes="slider-row"):
                            yield Slider(
                                min=0,
                                max=100,
                                step=1,
                                value=int(
                                    MOCK_CONFIG["memory"]["swap"]["usage_percent"]
                                ),
                                id="sld_swap",
                            )
                            yield Label(
                                f"{int(MOCK_CONFIG['memory']['swap']['usage_percent'])}%",
                                id="lbl_swap_val",
                                classes="value-lbl",
                            )

                # 分頁 3：外部儲存與網路流量
                with TabPane("儲存與網路", id="tab_storage"):
                    with ScrollableContainer():
                        yield Label("磁碟數據控制", classes="field")
                        yield Label("磁碟使用率 (%):")
                        with Horizontal(classes="slider-row"):
                            yield Slider(
                                min=0,
                                max=100,
                                step=1,
                                value=int(MOCK_CONFIG["disk"]["usage_percent"]),
                                id="sld_disk",
                            )
                            yield Label(
                                f"{int(MOCK_CONFIG['disk']['usage_percent'])}%",
                                id="lbl_disk_val",
                                classes="value-lbl",
                            )

                        yield Label("網路數據控制", classes="field")
                        yield Label("傳送位元組 (Bytes Sent):")
                        yield Input(
                            value=str(MOCK_CONFIG["network"]["bytes_sent"]),
                            id="inp_net_sent",
                        )
                        yield Label("接收位元組 (Bytes Recv):")
                        yield Input(
                            value=str(MOCK_CONFIG["network"]["bytes_recv"]),
                            id="inp_net_recv",
                        )

                # 分頁 4：供電與電池狀態
                with TabPane("能源與電池", id="tab_battery"):
                    with ScrollableContainer():
                        yield Label("電池數據控制", classes="field")
                        yield Label("強制電池回傳 null (桌機模式):")
                        yield Checkbox(
                            value=MOCK_CONFIG["battery_is_null"], id="chk_battery_null"
                        )
                        yield Label("充電狀態 (Power Plugged):")
                        yield Checkbox(
                            value=MOCK_CONFIG["battery"]["power_plugged"],
                            id="chk_battery_plugged",
                        )
                        yield Label("電池電量百分比 (%):")
                        with Horizontal(classes="slider-row"):
                            yield Slider(
                                min=0,
                                max=100,
                                step=1,
                                value=int(MOCK_CONFIG["battery"]["percent"]),
                                id="sld_bat",
                            )
                            yield Label(
                                f"{int(MOCK_CONFIG['battery']['percent'])}%",
                                id="lbl_bat_val",
                                classes="value-lbl",
                            )

        # 保持全域儲存按鈕，不論切換到哪一個分頁都可以直接儲存
        yield Button("儲存並同步設定", variant="primary", id="btn_save")
        yield Label("", id="status_lbl")

        yield Label("輸出內容:", classes="log-title")
        yield Log(id="flask_log", highlight=True)

    def on_slider_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "sld_cpu":
            self.query_one("#lbl_cpu_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_ram":
            self.query_one("#lbl_ram_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_swap":
            self.query_one("#lbl_swap_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_disk":
            self.query_one("#lbl_disk_val", Label).update(f"{int(event.value)}%")
        elif event.slider.id == "sld_bat":
            self.query_one("#lbl_bat_val", Label).update(f"{int(event.value)}%")

    def on_flask_log_message(self, message: "FlaskLogMessage") -> None:
        try:
            log_widget = self.query_one("#flask_log", Log)
            log_widget.write_line(message.log_line.strip())
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            # 寫回模擬開關狀態
            MOCK_CONFIG["enable_mock"] = self.query_one("#chk_mock", Checkbox).value
            MOCK_CONFIG["battery_is_null"] = self.query_one(
                "#chk_battery_null", Checkbox
            ).value
            MOCK_CONFIG["battery"]["power_plugged"] = self.query_one(
                "#chk_battery_plugged", Checkbox
            ).value

            # 寫回系統基本資訊
            MOCK_CONFIG["system"]["os"] = self.query_one("#inp_os", Input).value
            MOCK_CONFIG["system"]["os_release"] = self.query_one(
                "#inp_release", Input
            ).value
            MOCK_CONFIG["system"]["architecture"] = self.query_one(
                "#inp_arch", Input
            ).value

            # 寫回 CPU 資訊
            MOCK_CONFIG["cpu"]["model"] = self.query_one("#inp_cpu_model", Input).value

            total_cores = 1
            try:
                MOCK_CONFIG["cpu"]["physical_cores"] = int(
                    self.query_one("#inp_cpu_phys", Input).value
                )
                total_cores = int(self.query_one("#inp_cpu_total", Input).value)
                MOCK_CONFIG["cpu"]["total_cores"] = total_cores
            except ValueError:
                if "total_cores" in MOCK_CONFIG["cpu"]:
                    total_cores = MOCK_CONFIG["cpu"]["total_cores"]

            overall_usage = float(self.query_one("#sld_cpu", Slider).value)
            MOCK_CONFIG["cpu"]["overall_usage_percent"] = overall_usage

            per_core_list = []
            for _ in range(total_cores):
                core_val = overall_usage + random.uniform(-10.0, 10.0)
                core_val = max(0.0, min(100.0, round(core_val, 1)))
                per_core_list.append(core_val)
            MOCK_CONFIG["cpu"]["per_core_usage_percent"] = per_core_list

            # 寫回記憶體百分比
            MOCK_CONFIG["memory"]["ram"]["usage_percent"] = float(
                self.query_one("#sld_ram", Slider).value
            )
            MOCK_CONFIG["memory"]["swap"]["usage_percent"] = float(
                self.query_one("#sld_swap", Slider).value
            )

            # 寫回磁碟百分比
            MOCK_CONFIG["disk"]["usage_percent"] = float(
                self.query_one("#sld_disk", Slider).value
            )

            # 寫回網路流量
            try:
                MOCK_CONFIG["network"]["bytes_sent"] = int(
                    self.query_one("#inp_net_sent", Input).value
                )
                MOCK_CONFIG["network"]["bytes_recv"] = int(
                    self.query_one("#inp_net_recv", Input).value
                )
            except ValueError:
                pass

            # 寫回電池狀態
            MOCK_CONFIG["battery"]["percent"] = int(
                self.query_one("#sld_bat", Slider).value
            )

            lbl = self.query_one("#status_lbl", Label)
            lbl.update(" [全量配置結構已成功同步至記憶體快取] ")
