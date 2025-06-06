# Generates a report from backlog grooming
def generate_report(grooming_output):
    summary = "\n".join([
        f"- [{item['key']}] Suggest: {item.get('suggestion', 'none')}"
        for item in grooming_output.get("results", [])
    ])
    return f"# Backlog Health Report\n\n{summary}"
