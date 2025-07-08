Smart Resource Allocator with LLM-Powered Assistant
This project assigns tasks to available resources (workers/machines) based on skill and availability, and provides a chatbot assistant powered by Together.ai to answer task-related queries.


Project Files & Structure

smart_resource_allocator/
├── main.py                   # Entry point: runs task assignment and launches chatbot
├── gui.py                    # Optional: Streamlit GUI for chatbot
├── .env                      # API key file (user creates this)
│
├── logic/
│   └── task_assigner.py      # Core logic to assign tasks to resources
│
├── assistant/
│   ├── llm_chatbot.py        # Terminal-based chatbot
│   └── llm_helpers.py        # Common prompt & skill-checking logic
│
├── data/
│   ├── resources.json        # List of workers/machines with skills and availability
│   ├── tasks.json            # List of tasks with required skills
│   └── assignments.json      # Output: task-to-resource assignments (auto-generated)


Required Dependencies
Install everything using:
pip install openai==0.28.1 python-dotenv streamlit


API Setup
Create a .env file in the root folder with your Together.ai key:
OPENAI_API_KEY=your_together_ai_key_here
Get your free API key from https://console.together.ai


How to Run the Project
1. Run the full pipeline (CLI):
python main.py
- This will assign tasks and optionally launch the chatbot in your terminal.
2. (Optional) Launch the Web GUI:
streamlit run gui.py
- Opens the chatbot in your browser at http://localhost:8501

Done
You're now ready to interact with your resource allocation engine using natural language!
