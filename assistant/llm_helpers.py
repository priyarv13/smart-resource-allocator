import json
import re
from pathlib import Path

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_assignment_lines(assignments: list[dict[str, str]]) -> list[str]:
    lines = []
    for a in assignments:
        if a["resource_name"] == "UNASSIGNED":
            lines.append(f"{a['task_name']} ({a['task_id']}) is UNASSIGNED.")
        else:
            lines.append(f"{a['resource_name']} is assigned to {a['task_name']} ({a['task_id']}).")
    return lines

def build_prompt(query, assignment_lines, resource_lines, task_lines):
    context = (
        "Resources and their skills:\n" +
        "\n".join(f"- {line}" for line in resource_lines) +
        "\n\nTasks and required skills:\n" +
        "\n".join(f"- {line}" for line in task_lines) +
        "\n\nCurrent Assignments:\n" +
        "\n".join(f"- {line}" for line in assignment_lines)
    )
    prompt = (
        "You are an operations assistant. Use the skill and assignment data to answer questions accurately.\n\n"
        f"{context}\n\nUser question: {query}\nAnswer:"
    )
    return prompt

def direct_skill_check(query: str, resources, tasks):
    q = query.lower().strip().rstrip("?")

    # 1) Specific skill check
    match = re.search(r"(?:does|whether|can)?\s*(\w+)\s+(?:have|know|handle|do|has)?\s*(\w+)\s*skill", q)
    if match:
        name, skill = match.groups()
        res = next((r for r in resources if r["name"].lower() == name), None)
        if not res:
            return f"❓ I couldn't find a resource named '{name}'."
        if skill in map(str.lower, res.get("skills", [])):
            return f"✅ Yes — {res['name']} has the skill '{skill}'."
        else:
            return f"❌ No — {res['name']} does not have the skill '{skill}'."

    # 2) Skill listing
    match = re.search(r"(?:what|which)?\s*skills.*(?:does|has)?\s*(\w+)", q)
    if match:
        name = match.group(1)
        res = next((r for r in resources if r["name"].lower() == name), None)
        if not res:
            return f"❓ I couldn't find a resource named '{name}'."
        skills = ", ".join(res.get("skills", []))
        return f"🔎 {res['name']}'s skills: {skills or 'none listed'}."

    # 3) Task takeover check
    match = re.search(r"can (\w+) take over (t\d+)(?: instead of (\w+))?", q)
    if match:
        new_res_name, task_id, old_res_name = match.groups()
        new_res = next((r for r in resources if r["name"].lower() == new_res_name), None)
        task = next((t for t in tasks if t["id"].lower() == task_id.lower()), None)
        if not new_res:
            return f"❓ I couldn't find a resource named '{new_res_name}'."
        if not task:
            return f"❓ I couldn't find a task with ID '{task_id}'."
        required = task["required_skill"].lower()
        has_skill = required in map(str.lower, new_res.get("skills", []))
        if has_skill:
            return f"✅ Yes — {new_res['name']} has '{required}' skill and can take over {task_id}."
        else:
            return f"❌ No — {new_res['name']} does not have the skill '{required}' required for {task_id}."

    return None
