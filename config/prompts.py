# config/prompts.py

PROMPTS = {
    'code_generation': "Generate Python code for the following task: {task_description}",
    'meeting_summary': "Summarize the following meeting transcript: {transcript}",
    # Add other prompts
}

def get_prompt(template_name, **kwargs):
    return PROMPTS[template_name].format(**kwargs)
