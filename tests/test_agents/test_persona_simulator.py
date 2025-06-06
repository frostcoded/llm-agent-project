import pytest
from agents.persona_simulator import PersonaSimulator

@pytest.fixture
def simulator():
    return PersonaSimulator(config={"openai": {"enabled": False}})

def test_simulate_persona_output(simulator):
    result = simulator.simulate_persona_output("empathetic", "onboarding doc", "how to ask for help")
    assert isinstance(result, dict)
