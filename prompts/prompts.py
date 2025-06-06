# prompts/prompts.py

import os

PROMPT_DIR = os.path.join(os.path.dirname(__file__))

def render_prompt(template_name: str, context: dict) -> str:
    """
    Load a prompt template and render it with the provided context.

    Args:
        template_name (str): The filename of the prompt template.
        context (dict): A dictionary containing values to replace in the template.

    Returns:
        str: The rendered prompt.
    """
    template_path = os.path.join(PROMPT_DIR, template_name)
    with open(template_path, 'r') as file:
        template = file.read()
    return template.format(**context)
