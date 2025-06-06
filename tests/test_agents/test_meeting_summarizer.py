# tests/test_agents/test_meeting_summarizer.py

import pytest
from agents.meeting_summarizer import MeetingSummarizer

@pytest.fixture
def summarizer():
    return MeetingSummarizer(config={"openai": {"enabled": False}})

def test_summarize_meeting(summarizer):
    transcript = "John: We need to ship the new release by Friday. Jane: I’ll write the tests."
    result = summarizer.summarize_meeting(transcript)
    assert "summary" in result
