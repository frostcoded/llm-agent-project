# Automates grooming using the backlog_groomer agent
from agents.backlog_groomer import BacklogGroomer
from config.settings import load_settings

def groom_backlog(jira_issues):
    config = load_settings()
    groomer = BacklogGroomer(config)
    return groomer.groom_issues(jira_issues)
