"""Media control service and platform selection."""

import platform


class MediaUnavailable(Exception):
    pass


def controller():
    if platform.system() != "Windows":
        raise MediaUnavailable("Media control is currently supported only on Windows")
    from ..platform import windows_media

    return windows_media
