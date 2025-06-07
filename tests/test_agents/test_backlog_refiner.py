# tests/test_agents/test_backlog_refiner.py

import unittest
from unittest.mock import patch
from agents.backlog_refiner import BacklogRefiner


class TestBacklogRefiner(unittest.TestCase):

    def setUp(self):
        self.sample_issues = [
            {"id": "PROJ-1", "summary": "Fix login bug", "description": "Fails on Safari", "priority": "Medium"},
            {"id": "PROJ-2", "summary": "", "description": "", "priority": "High"}
        ]

        self.mock_summary = "Issue PROJ-1 is valid but lacks browser matrix. PROJ-2 is unclear and incomplete."
        self.mock_response = {
            "summary": self.mock_summary,
            "suggestions": [
                {"id": "PROJ-1", "action": "Add browser compatibility details"},
                {"id": "PROJ-2", "action": "Complete title and description"}
            ],
            "confidence": 0.92
        }

    @patch("agents.backlog_refiner.get_collator")
    def test_refine_issues_returns_suggestions(self, mock_get_collator):
        mock_collator = mock_get_collator.return_value
        mock_collator.summarize_responses.return_value = self.mock_response

        refiner = BacklogRefiner()
        result = refiner.refine_issues(self.sample_issues)

        self.assertIn("summary", result)
        self.assertIn("suggestions", result)
        self.assertEqual(len(result["suggestions"]), 2)

    @patch("agents.backlog_refiner.get_collator")
    def test_refine_issues_with_empty_list(self, mock_get_collator):
        refiner = BacklogRefiner()
        result = refiner.refine_issues([])

        self.assertEqual(result["summary"], "No issues provided.")
        self.assertEqual(result["suggestions"], [])


if __name__ == "__main__":
    unittest.main()
