# Uses sprint_planner agent to organize upcoming sprints
from agents.sprint_planner import SprintPlanner
from config.settings import load_settings

def create_sprint_plan(duration, availability, velocity, goals):
    planner = SprintPlanner(load_settings())
    return planner.plan_sprint(duration, availability, velocity, goals)
