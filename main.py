"""
main.py – Entry point for Smart Resource Allocator

Runs:
1. Task assignment (logic/task_assigner.py)
2. Optionally launches the Together.ai‑powered chatbot (assistant/llm_chatbot.py)
"""

import os
import sys
import subprocess
from logic import task_assigner


def run_task_assignment() -> None:
    """Generate assignments.json and print a summary."""
    print("🔄 Assigning tasks to available resources...")
    task_assigner.main()  # prints its own summary


def run_chatbot() -> None:
    """Launch the chatbot in a subprocess that uses the same Python interpreter/venv."""
    chatbot_path = os.path.join("assistant", "llm_chatbot.py")
    print("\n🤖 Launching Together.ai chatbot...\n")
    try:
        subprocess.run([sys.executable, chatbot_path], check=True)
    except subprocess.CalledProcessError as err:
        print(f"❌ Chatbot exited with code {err.returncode}. See above for details.")


def main() -> None:
    run_task_assignment()

    choice = input("\n👉 Do you want to chat with the assistant? (y/n): ").strip().lower()
    if choice == "y":
        run_chatbot()
    else:
        print("✅ Done. You can view assignments in data/assignments.json")


if __name__ == "__main__":
    main()
