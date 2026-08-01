"""Thin wrapper around notifypy so a failed notification never crashes etanbloxxed."""
import notifypy

from .utils import logger


class Notifier:
    def __init__(self, title: str = "etanbloxxed"):
        self._notification = notifypy.Notify()
        self._notification.title = title

    def notify(self, message: str) -> None:
        self._notification.message = message
        try:
            self._notification.send()
        except Exception:
            logger.debug("Failed to send notification", exc_info=True)
