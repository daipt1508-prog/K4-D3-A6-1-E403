"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import json
import os
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS, execute_tool_safely
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

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")

    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["test_cases"]


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT, )
    print(f"🤖 Chatbot trả lời:\n{response}")


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    scratchpad = ""
    step = 0

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        prompt = f"Câu hỏi của người dùng: {user_query}\n{scratchpad}"
        if step == MAX_ITERATIONS:
            prompt += (
                "\n⚠️ ĐÂY LÀ LƯỢT SUY LUẬN CUỐI CÙNG. KHÔNG được gọi thêm Action. "
                "Dựa trên các Observation đã có ở trên, bắt buộc phải trả lời ngay bằng Final Answer."
            )
        llm_output = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)

        thought, tool_name, tool_args = parse_action_line(llm_output)
        if thought:
            print(f"🧠 Thought: {thought}")

        final_answer = has_final_answer(llm_output)
        if final_answer:
            print(f"🏁 Final Answer: {final_answer}")
            return final_answer

        if step == MAX_ITERATIONS:
            break

        if not tool_name:
            print(f"⚠️ Không nhận diện được Action hợp lệ trong phản hồi LLM:\n{llm_output}")
            scratchpad += (
                "\nObservation: LỖI ĐỊNH DẠNG - Không tìm thấy Action hợp lệ. "
                "Hãy trả lời đúng định dạng 'Action: ten_tool[tham_so]'.\n"
            )
            continue

        args = parse_tool_args(tool_args)
        print(f"🛠️ Action: {tool_name}[{tool_args}]")

        obs = execute_tool_safely(tool_name, *args)
        print(f"👁️ Observation: {obs}")

        scratchpad += f"\nThought: {thought}\nAction: {tool_name}[{tool_args}]\nObservation: {obs}\n"

    print(GUARDRAIL_FALLBACK_MESSAGE)
    return None


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Chạy thử toàn bộ Test Cases
    for i in range(len(tests)):
        sample_query = tests[i]["input"]
        
        print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
        run_baseline_chatbot(sample_query, provider)
        
        print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
        run_react_agent(sample_query, provider)
