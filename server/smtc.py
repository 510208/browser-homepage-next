import asyncio
import json
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager


class MediaController:
    """
    一個用於控制媒體播放狀態的元件
    """

    def __init__(self):
        # 初始化會話管理器與當前會話變數
        self.manager = None
        self.current_session = None

    async def _init_session(self):
        # 異步初始化 Windows 媒體控制管理器
        if not self.manager:
            self.manager = (
                await GlobalSystemMediaTransportControlsSessionManager.request_async()
            )
        # 取得當前活躍的媒體會話
        self.current_session = self.manager.get_current_session()

    async def fetch_media_info_json(self):
        """獲取當前播放的音樂資訊並回傳 JSON 字串"""
        await self._init_session()

        info_dict = {
            "status": "No session active",
            "title": "Unknown",
            "artist": "Unknown",
            "album": "Unknown",
        }

        if not self.current_session:
            return json.dumps(info_dict, ensure_ascii=False)

        # 讀取媒體屬性
        try:
            properties = await self.current_session.try_get_media_properties_async()
            playback_info = self.current_session.get_playback_info()

            # 轉換播放狀態為文字描述
            status_mapping = {
                0: "Closed",
                1: "Opened",
                2: "Changing",
                3: "Stopped",
                4: "Paused",
                5: "Playing",
            }
            playback_status = status_mapping.get(
                playback_info.playback_status, "Unknown"
            )

            info_dict = {
                "status": playback_status,
                "title": properties.title,
                "artist": properties.artist,
                "album": properties.album_title,
            }
        except Exception as e:
            info_dict["status"] = f"Error: {str(e)}"

        return json.dumps(info_dict, ensure_ascii=False)

    async def play_next(self):
        """控制媒體切換至下一首"""
        await self._init_session()
        if self.current_session:
            return await self.current_session.try_skip_next_async()
        return False

    async def play_previous(self):
        """控制媒體切換至上一首"""
        await self._init_session()
        if self.current_session:
            return await self.current_session.try_skip_previous_async()
        return False

    async def toggle_play_pause(self):
        """控制媒體切換播放或暫停狀態"""
        await self._init_session()
        if self.current_session:
            return await self.current_session.try_toggle_play_pause_async()
        return False


# 提供同步調用的包裝函數，方便不熟悉 async 的外部程式調用
def get_media_info():
    controller = MediaController()
    return asyncio.run(controller.fetch_media_info_json())


def next_track():
    controller = MediaController()
    return asyncio.run(controller.play_next())


def previous_track():
    controller = MediaController()
    return asyncio.run(controller.play_previous())


def toggle_play():
    controller = MediaController()
    return asyncio.run(controller.toggle_play_pause())
