# tests/test_agents/test_calendar_blocker.py

import unittest
from unittest.mock import MagicMock, patch
from agents.calendar_blocker import CalendarBlocker


class TestCalendarBlocker(unittest.TestCase):

    def setUp(self):
        self.user = "test@example.com"
        self.start_time = "2025-06-15T10:00:00"
        self.end_time = "2025-06-15T11:00:00"
        self.reason = "Unavailable"
        self.time_range = "2025-06-15T10:00:00/2025-06-15T11:00:00"

    @patch("agents.calendar_blocker.AppleCalendarClient")
    @patch("agents.calendar_blocker.OutlookClient")
    def test_block_time_success(self, mock_outlook, mock_apple):
        mock_outlook.return_value.block_time.return_value = {"status": "success"}
        mock_apple.return_value.block_time.return_value = {"status": "success"}

        blocker = CalendarBlocker()
        result = blocker.block_time(self.user, self.start_time, self.end_time, self.reason)

        self.assertEqual(result["outlook"]["status"], "success")
        self.assertEqual(result["apple"]["status"], "success")

    @patch("agents.calendar_blocker.AppleCalendarClient")
    @patch("agents.calendar_blocker.OutlookClient")
    def test_unblock_time_success(self, mock_outlook, mock_apple):
        mock_outlook.return_value.unblock_time.return_value = {"status": "unblocked"}
        mock_apple.return_value.unblock_time.return_value = {"status": "unblocked"}

        blocker = CalendarBlocker()
        result = blocker.unblock_time(self.user, self.time_range)

        self.assertEqual(result["outlook"]["status"], "unblocked")
        self.assertEqual(result["apple"]["status"], "unblocked")

    @patch("agents.calendar_blocker.AppleCalendarClient")
    @patch("agents.calendar_blocker.OutlookClient")
    def test_block_time_partial_failure(self, mock_outlook, mock_apple):
        mock_outlook.return_value.block_time.side_effect = Exception("Outlook down")
        mock_apple.return_value.block_time.return_value = {"status": "ok"}

        blocker = CalendarBlocker()
        result = blocker.block_time(self.user, self.start_time, self.end_time, self.reason)

        self.assertIn("error", result["outlook"])
        self.assertEqual(result["apple"]["status"], "ok")

    @patch("agents.calendar_blocker.AppleCalendarClient")
    @patch("agents.calendar_blocker.OutlookClient")
    def test_unblock_time_partial_failure(self, mock_outlook, mock_apple):
        mock_outlook.return_value.unblock_time.return_value = {"status": "ok"}
        mock_apple.return_value.unblock_time.side_effect = Exception("Apple error")

        blocker = CalendarBlocker()
        result = blocker.unblock_time(self.user, self.time_range)

        self.assertEqual(result["outlook"]["status"], "ok")
        self.assertIn("error", result["apple"])


if __name__ == "__main__":
    unittest.main()
