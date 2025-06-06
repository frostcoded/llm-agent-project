# agents/calendar_blocker.py

from integrations.apple_calendar_client import AppleCalendarClient
from integrations.outlook_client import OutlookClient
from config.settings import load_settings
from typing import Dict, Any


class CalendarBlocker:
    """
    Blocks calendar time based on user messages or direct instructions.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.apple = AppleCalendarClient(config.get("apple", {}))
        self.outlook = OutlookClient(config.get("outlook", {}))

    def block_time(self, user: str, start_time: str, end_time: str, reason: str = "Unavailable") -> Dict[str, Any]:
        """
        Block a calendar event in both Apple and Outlook.
        """
        result = {
            "outlook": self.outlook.block_time(user, start_time, end_time, reason),
            "apple": self.apple.block_time(user, start_time, end_time, reason)
        }
        return result

    def unblock_time(self, user: str, time_range: str = None) -> Dict[str, Any]:
        """
        Unblock previously reserved time.
        """
        result = {
            "outlook": self.outlook.unblock_time(user, time_range),
            "apple": self.apple.unblock_time(user, time_range)
        }
        return result
