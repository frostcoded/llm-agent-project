# tests/test_agents/test_calendar_checker.py

import unittest
from unittest.mock import patch
from agents.calendar_checker import CalendarChecker


class TestCalendarChecker(unittest.TestCase):

    def setUp(self):
        self.users = ["alice@example.com", "bob@example.com"]
        self.duration = 30
        self.topic = "Project Sync"
        self.preferred_slots = ["2025-06-15T10:00:00", "2025-06-15T14:00:00"]

    @patch("agents.calendar_checker.TeamsClient")
    @patch("agents.calendar_checker.OutlookClient")
    @patch("agents.calendar_checker.AppleCalendarClient")
    def test_find_available_slots_success(self, mock_apple, mock_outlook, mock_teams):
        mock_apple.return_value.get_availability.return_value = [
            "2025-06-15T10:00:00", "2025-06-15T14:00:00"
        ]
        mock_outlook.return_value.get_availability.return_value = [
            "2025-06-15T14:00:00", "2025-06-15T16:00:00"
        ]

        checker = CalendarChecker()
        result = checker.find_available_slots(self.users, self.duration)

        self.assertIn("available_slots", result)
        self.assertEqual(result["available_slots"], ["2025-06-15T14:00:00"])
        self.assertIn("source_details", result)

    @patch("agents.calendar_checker.TeamsClient")
    @patch("agents.calendar_checker.OutlookClient")
    @patch("agents.calendar_checker.AppleCalendarClient")
    def test_find_available_slots_with_empty_overlap(self, mock_apple, mock_outlook, mock_teams):
        mock_apple.return_value.get_availability.return_value = ["2025-06-15T09:00:00"]
        mock_outlook.return_value.get_availability.return_value = ["2025-06-15T16:00:00"]

        checker = CalendarChecker()
        result = checker.find_available_slots(self.users, self.duration)

        self.assertEqual(result["available_slots"], [])

    @patch("agents.calendar_checker.TeamsClient")
    @patch("agents.calendar_checker.OutlookClient")
    @patch("agents.calendar_checker.AppleCalendarClient")
    def test_schedule_meeting_success(self, mock_apple, mock_outlook, mock_teams):
        checker = CalendarChecker()
        result = checker.schedule_meeting(self.users, self.topic, self.preferred_slots)

        self.assertEqual(result["topic"], self.topic)
        self.assertEqual(result["scheduled_time"], self.preferred_slots[0])

    @patch("agents.calendar_checker.TeamsClient")
    @patch("agents.calendar_checker.OutlookClient")
    @patch("agents.calendar_checker.AppleCalendarClient")
    def test_schedule_meeting_with_empty_slots(self, mock_apple, mock_outlook, mock_teams):
        checker = CalendarChecker()
        result = checker.schedule_meeting(self.users, self.topic, [])

        self.assertEqual(result["topic"], self.topic)
        self.assertEqual(result["scheduled_time"], "No common slot found")


if __name__ == "__main__":
    unittest.main()
