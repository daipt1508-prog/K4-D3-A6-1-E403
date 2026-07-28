"""
🎨 DEMO WEB UI (Streamlit) - Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
So sánh trực quan Chatbot Baseline vs ReAct Agent.
Chạy: streamlit run src/streamlit_app.py
"""

import json
import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import execute_tool_safely
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_SYSTEM_PROMPT,
    MAX_ITERATIONS,
    GUARDRAIL_FALLBACK_MESSAGE,
    parse_action_line,
    parse_tool_args,
    has_final_answer,
)
from providers import get_llm_provider


def load_test_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["test_cases"]


def run_baseline(query: str, provider) -> str:
    return provider.generate(query, system_prompt=CHATBOT_BASELINE_PROMPT)


def run_react(query: str, provider):
    """Chạy vòng lặp ReAct Agent, trả về (danh sách các bước, final_answer)."""
    scratchpad = ""
    steps = []

    for step in range(1, MAX_ITERATIONS + 1):
        prompt = f"Câu hỏi của người dùng: {query}\n{scratchpad}"
        if step == MAX_ITERATIONS:
            prompt += (
                "\n⚠️ ĐÂY LÀ LƯỢT SUY LUẬN CUỐI CÙNG. KHÔNG được gọi thêm Action. "
                "Dựa trên các Observation đã có ở trên, bắt buộc phải trả lời ngay bằng Final Answer."
            )
        llm_output = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
        thought, tool_name, tool_args = parse_action_line(llm_output)

        final_answer = has_final_answer(llm_output)
        if final_answer:
            steps.append({"step": step, "thought": thought, "final": final_answer})
            return steps, final_answer

        if step == MAX_ITERATIONS:
            break

        if not tool_name:
            steps.append({
                "step": step,
                "thought": thought,
                "error": "Không nhận diện được Action hợp lệ trong phản hồi LLM.",
                "raw": llm_output,
            })
            scratchpad += (
                "\nObservation: LỖI ĐỊNH DẠNG - Không tìm thấy Action hợp lệ. "
                "Hãy trả lời đúng định dạng 'Action: ten_tool[tham_so]'.\n"
            )
            continue

        args = parse_tool_args(tool_args)
        obs = execute_tool_safely(tool_name, *args)
        steps.append({
            "step": step,
            "thought": thought,
            "action": tool_name,
            "args": tool_args,
            "observation": obs,
        })
        scratchpad += f"\nThought: {thought}\nAction: {tool_name}[{tool_args}]\nObservation: {obs}\n"

    return steps, None


# ============================== STREAMLIT UI ==============================

st.set_page_config(page_title="Trợ Lý Chọn Quà Tặng", page_icon="🎁", layout="wide")

st.title("🎁 Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp")
st.caption("Demo so sánh Chatbot Baseline (Cấp 2) vs ReAct Agent (Cấp 3) — Bài Lab VinUni")

provider = get_llm_provider()
model_name = getattr(provider, "model_name", "Offline Mock Mode")

with st.sidebar:
    st.subheader("⚙️ Cấu hình đang chạy")
    st.write(f"**Provider:** `{provider.__class__.__name__}`")
    st.write(f"**Model:** `{model_name}`")
    st.write(f"**Max Iterations (Guardrail):** {MAX_ITERATIONS}")

    st.divider()
    st.subheader("📋 Test Cases mẫu")
    test_cases = load_test_cases()
    labels = [f"[{tc['category']}] {tc['input']}" for tc in test_cases]
    choice = st.selectbox("Chọn nhanh 1 câu test có sẵn:", ["-- Tự nhập câu hỏi --"] + labels)

default_query = ""
if choice != "-- Tự nhập câu hỏi --":
    default_query = test_cases[labels.index(choice)]["input"]

query = st.text_area("💬 Nhập câu hỏi của bạn:", value=default_query, height=80,
                      placeholder="Ví dụ: Tôi muốn tìm quà sinh nhật cho bạn gái, ngân sách 500 nghìn, bạn ấy hướng nội thích đọc sách.")

run_clicked = st.button("🚀 Chạy Demo", type="primary", use_container_width=True)

if run_clicked and not query.strip():
    st.warning("Vui lòng nhập câu hỏi trước khi chạy demo.")

if run_clicked and query.strip():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💬 Chatbot Baseline")
        with st.spinner("Đang gọi LLM..."):
            baseline_response = run_baseline(query, provider)
        st.info(baseline_response)

    with col2:
        st.subheader("🤖 ReAct Agent")
        with st.spinner("Đang suy luận theo vòng lặp ReAct..."):
            steps, final_answer = run_react(query, provider)

        for s in steps:
            with st.expander(f"🔄 Vòng lặp {s['step']}/{MAX_ITERATIONS}", expanded=True):
                if s.get("thought"):
                    st.markdown(f"**🧠 Thought:** {s['thought']}")
                if "action" in s:
                    st.markdown(f"**🛠️ Action:** `{s['action']}[{s['args']}]`")
                    st.markdown(f"**👁️ Observation:** {s['observation']}")
                if "final" in s:
                    st.markdown(f"**🏁 Final Answer:** {s['final']}")
                if "error" in s:
                    st.warning(s["error"])

        if final_answer:
            st.success(f"🏁 **Final Answer:** {final_answer}")
        else:
            st.error(GUARDRAIL_FALLBACK_MESSAGE)
