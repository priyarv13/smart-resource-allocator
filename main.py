"""main.py – Entry point for Smart Resource Allocator"""

import subprocess
import sys
import platform
from logic import task_assigner

def run_task_assignment():
    print("🔄 Assigning tasks to available resources...\n")
    assignments = task_assigner.main()
    print("✅ Task assignment complete.\n")

def run_chatbot():
    print("\n🤖 Launching Together.ai chatbot...\n")
    chatbot_path = "assistant/llm_chatbot.py" if platform.system() != "Windows" else "assistant\\llm_chatbot.py"
    try:
        subprocess.run([sys.executable, chatbot_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch chatbot: {e}")

def main():
    run_task_assignment()

    choice = input("👉 Do you want to chat with the assistant? (y/n): ").strip().lower()
    if choice == "y":
        run_chatbot()
    else:
        print("✅ Done. You can view assignments in data/assignments.json")

if __name__ == "__main__":
    main()
