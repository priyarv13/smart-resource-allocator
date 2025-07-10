"""llm_chatbot.py
Smart Resource Allocator – Together.ai-powered chatbot
-----------------------------------------------------
* Uses Together.ai (OpenAI-compatible) API.
* Loads your API key from a .env file using `python-dotenv`
* Model: "mistralai/Mistral-7B-Instruct-v0.2"
"""

from __future__ import annotations
import json
import os
import re
from pathlib import Path
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_base = "https://api.together.xyz/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

if not openai.api_key:
    raise RuntimeError(
        "⚠️ OPENAI_API_KEY is missing. Please create a .env file with your Together.ai key:\n"
        "OPENAI_API_KEY=your_key_here"
    )

# ----------------------------
# File paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
ASSIGNMENTS_FILE = DATA_DIR / "assignments.json"
RESOURCES_FILE = DATA_DIR / "resource.json"
TASKS_FILE = DATA_DIR / "tasks.json"

# ----------------------------
# Load data helpers
# ----------------------------
def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)

def build_assignment_lines(assignments: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    for a in assignments:
        if a["resource_name"] == "UNASSIGNED":
            lines.append(f"{a['task_name']} ({a['task_id']}) is UNASSIGNED.")
        else:
            lines.append(f"{a['resource_name']} is assigned to {a['task_name']} ({a['task_id']}).")
    return lines

def build_prompt(query: str, assignment_lines: list[str]) -> str:
    context = "Assignments:\n" + "\n".join(f"- {line}" for line in assignment_lines)
    prompt = (
        "You are an operations assistant. Answer questions using the assignments list.\n"
        f"{context}\n\nUser question: {query}\nAnswer:"
    )
    return prompt

# ----------------------------
# Rule-based skill reassignment check
# ----------------------------
def direct_skill_check(query, resources, tasks):
    q = query.lower()

    # Pattern: Can Bob take over T2 instead of Alice?
    pat_swap = re.search(r"can (\w+) take over (t\d+)(?: instead of (\w+))?", q)
    if pat_swap:
        new_res_name, task_id, old_res_name = pat_swap.groups()
        new_res = next((r for r in resources if r["name"].lower() == new_res_name.lower()), None)
        task = next((t for t in tasks if t["id"].lower() == task_id.lower()), None)

        if not new_res:
            return f"❓ I couldn't find a resource named '{new_res_name}'."
        if not task:
            return f"❓ I couldn't find a task with ID '{task_id}'."

        required = task["required_skill"].lower()
        if required in map(str.lower, new_res.get("skills", [])):
            return f"✅ Yes — {new_res['name']} has '{required}' skill and can take over {task_id}."
        else:
            return f"❌ No — {new_res['name']} does not have the skill '{required}' required for {task_id}."

    return None

# ----------------------------
# Call Together.ai
# ----------------------------
def ask_together(prompt: str, temperature: float = 0.2) -> str:
    response = openai.ChatCompletion.create(
        model=TOGETHER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

# ----------------------------
# Interactive chatbot loop
# ----------------------------
def chat():
    assignments = load_json(ASSIGNMENTS_FILE)
    assignment_lines = build_assignment_lines(assignments)
    resources = load_json(RESOURCES_FILE)
    tasks = load_json(TASKS_FILE)

    print("🤖 Together.ai Chatbot ready. Type 'exit' to quit.")
    while True:
        try:
            user_q = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_q.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        rule_answer = direct_skill_check(user_q, resources, tasks)
        if rule_answer:
            answer = rule_answer
        else:
            prompt = build_prompt(user_q, assignment_lines)
            try:
                answer = ask_together(prompt)
            except Exception as e:
                answer = f"❌ API error: {e}"

        print(f"\nAssistant: {answer}")

if __name__ == "__main__":
    chat()
