# tests/test_agents/test_automated_code_review.py

import unittest
from unittest.mock import patch, MagicMock
from agents.automated_code_review import AutomatedCodeReviewer


class TestAutomatedCodeReviewer(unittest.TestCase):
    def setUp(self):
        self.sample_code = """
def add(a, b):
    return a + b
"""
        self.context = "Simple addition function"
        self.mock_response = {
            "summary": "Function is clean but lacks input validation. Consider type checking and docstrings."
        }

    @patch("agents.automated_code_review.LLMCollator")
    def test_review_code_returns_expected_summary(self, MockCollator):
        mock_instance = MockCollator.return_value
        mock_instance.summarize_responses.return_value = self.mock_response

        reviewer = AutomatedCodeReviewer(config={"provider": "openai"})
        result = reviewer.review_code(self.sample_code, language="python", context=self.context)

        self.assertIn("suggestions", result)
        self.assertIn("review_style", result)
        self.assertEqual(result["suggestions"], self.mock_response["summary"])
        self.assertEqual(result["review_style"], "general")

        mock_instance.summarize_responses.assert_called_once()

    @patch("agents.automated_code_review.LLMCollator")
    def test_review_code_handles_empty_summary(self, MockCollator):
        mock_instance = MockCollator.return_value
        mock_instance.summarize_responses.return_value = {}

        reviewer = AutomatedCodeReviewer()
        result = reviewer.review_code(self.sample_code)

        self.assertIn("No suggestions returned.", result["suggestions"])

    def test_review_code_raises_no_errors_on_valid_input(self):
        with patch("agents.automated_code_review.LLMCollator") as MockCollator:
            instance = MockCollator.return_value
            instance.summarize_responses.return_value = {"summary": "Looks good."}

            reviewer = AutomatedCodeReviewer()
            result = reviewer.review_code(self.sample_code)

            self.assertIsInstance(result, dict)
            self.assertIn("suggestions", result)


if __name__ == "__main__":
    unittest.main()
