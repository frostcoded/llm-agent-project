# Converts Jira stories to code using code_generator
from agents.code_generator import CodeGenerator
from config.settings import load_settings

def generate_code_from_story(story_description):
    generator = CodeGenerator(load_settings())
    return generator.generate_code(story_description)
