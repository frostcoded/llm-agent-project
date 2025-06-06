# Plans which stories should be prioritized for automation
def prioritize_stories(stories):
    return sorted(stories, key=lambda s: s.get("impact", 0), reverse=True)
