# agents/calendar_blocker.py

from integrations.apple_calendar_client import AppleCalendarClient
from integrations.outlook_client import OutlookClient
from config.settings import load_settings
from utils.logger import logger
from typing import Dict, Any


class CalendarBlocker:
    """
    Blocks or unblocks user time in Apple and Outlook calendars.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.apple = AppleCalendarClient(config.get("apple", {}))
        self.outlook = OutlookClient(config.get("outlook", {}))

    def block_time(self, user: str, start_time: str, end_time: str, reason: str = "Unavailable") -> Dict[str, Any]:
        logger.info(f"[CalendarBlocker] Blocking time for {user} from {start_time} to {end_time}")
        result = {}
        try:
            result["outlook"] = self.outlook.block_time(user, start_time, end_time, reason)
        except Exception as e:
            logger.error(f"Outlook block failed: {e}")
            result["outlook"] = {"error": str(e)}

        try:
            result["apple"] = self.apple.block_time(user, start_time, end_time, reason)
        except Exception as e:
            logger.error(f"Apple block failed: {e}")
            result["apple"] = {"error": str(e)}

        return result

    def unblock_time(self, user: str, time_range: str = None) -> Dict[str, Any]:
        logger.info(f"[CalendarBlocker] Unblocking time for {user} range: {time_range}")
        result = {}
        try:
            result["outlook"] = self.outlook.unblock_time(user, time_range)
        except Exception as e:
            logger.error(f"Outlook unblock failed: {e}")
            result["outlook"] = {"error": str(e)}

        try:
            result["apple"] = self.apple.unblock_time(user, time_range)
        except Exception as e:
            logger.error(f"Apple unblock failed: {e}")
            result["apple"] = {"error": str(e)}

        return result
