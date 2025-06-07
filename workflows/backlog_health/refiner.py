# Automates refining using the backlog_refiner agent
from agents.backlog_refiner import BacklogRefiner
from config.settings import load_settings

def refine_backlog(jira_issues):
    config = load_settings()
    refiner = BacklogRefiner(config)
    return refiner.refine_issues(jira_issues)
