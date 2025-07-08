import json
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESOURCES_FILE = DATA_DIR / "resource.json"
TASKS_FILE = DATA_DIR / "tasks.json"
ASSIGNMENTS_FILE = DATA_DIR / "assignments.json"

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def assign_tasks():
    resources = load_json(RESOURCES_FILE)
    tasks = load_json(TASKS_FILE)

    skill_map = defaultdict(list)
    load_counter = defaultdict(int)

    # 🔧 Only use available resources
    for res in resources:
        if not res.get("available", True):
            continue
        for skill in res.get("skills", []):
            skill_map[skill].append(res)

    assignments = []

    for task in tasks:
        skill = task["required_skill"]
        candidates = skill_map.get(skill, [])
        if not candidates:
            assignments.append({
                "task_id": task["id"],
                "task_name": task["name"],
                "resource_id": None,
                "resource_name": "UNASSIGNED"
            })
            continue

        candidates.sort(key=lambda r: (load_counter[r["id"]], r["name"]))
        selected = candidates[0]
        load_counter[selected["id"]] += 1

        assignments.append({
            "task_id": task["id"],
            "task_name": task["name"],
            "resource_id": selected["id"],
            "resource_name": selected["name"]
        })

    save_json(assignments, ASSIGNMENTS_FILE)
    return assignments

def print_summary(assignments):
    print("✅ Saved output to", ASSIGNMENTS_FILE)
    print("\nAssignment Summary:")
    for a in assignments:
        print(f"  {a['task_id']}: {a['task_name']} -> {a['resource_name']}")

def main():
    assignments = assign_tasks()
    print_summary(assignments)

if __name__ == "__main__":
    main()
