import streamlit as st
from assistant.llm_helpers import (
    load_json,
    direct_skill_check,
    build_assignment_lines,
    build_prompt,
)
from assistant.llm_chatbot import ask_together
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
assignments = load_json(DATA_DIR / "assignments.json")
resources    = load_json(DATA_DIR / "resource.json")
tasks        = load_json(DATA_DIR / "tasks.json")

assign_lines = build_assignment_lines(assignments)
res_lines    = [f"{r['name']}: {', '.join(r['skills'])}" for r in resources]
task_lines   = [f"{t['id']} requires {t['required_skill']}" for t in tasks]

st.title("Smart Resource Allocator Chatbot")

user_q = st.text_input("Ask a question about resources / tasks:")

if user_q:
    skill_ans = direct_skill_check(user_q, resources, tasks)
    if skill_ans:
        st.success(skill_ans)
    else:
        prompt = build_prompt(user_q, assign_lines, res_lines, task_lines)
        with st.spinner("Thinking..."):
            answer = ask_together(prompt)
        st.info(answer)
