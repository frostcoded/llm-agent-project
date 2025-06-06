# agents/calendar_checker.py

from integrations.apple_calendar_client import AppleCalendarClient
from integrations.outlook_client import OutlookClient
from integrations.teams_client import TeamsClient
from config.settings import load_settings
from typing import List, Dict, Any


class CalendarChecker:
    """
    Checks calendar availability for individuals or teams and recommends optimal meeting times.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.apple = AppleCalendarClient(config.get("apple", {}))
        self.outlook = OutlookClient(config.get("outlook", {}))
        self.teams = TeamsClient(config.get("teams", {}))

    def find_available_slots(self, users: List[str], duration_minutes: int = 30) -> Dict[str, Any]:
        """
        Analyze calendars and find common open slots.
        """
        apple_availability = self.apple.get_availability(users, duration_minutes)
        outlook_availability = self.outlook.get_availability(users, duration_minutes)

        combined = list(set(apple_availability) & set(outlook_availability))
        return {
            "available_slots": combined,
            "source_details": {
                "apple": apple_availability,
                "outlook": outlook_availability
            }
        }

    def schedule_meeting(self, users: List[str], topic: str, preferred_slots: List[str]) -> Dict[str, Any]:
        """
        Book a meeting based on shared availability.
        """
        best_slot = preferred_slots[0] if preferred_slots else "No common slot found"
        return {
            "topic": topic,
            "scheduled_time": best_slot
        }
