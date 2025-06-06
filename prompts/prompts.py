# prompts/prompts.py

import os
from jinja2 import Template

PROMPT_DIR = os.path.dirname(__file__)

def load_prompt(filename: str) -> str:
    """
    Load a raw prompt template file from the prompts directory.
    """
    path = os.path.join(PROMPT_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def render_prompt(filename: str, context: dict) -> str:
    """
    Load and render a Jinja2 prompt template with context.
    """
    template_str = load_prompt(filename)
    template = Template(template_str)
    return template.render(**context)
