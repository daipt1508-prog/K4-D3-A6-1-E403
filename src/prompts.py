"""
🧠 PROMPTS & SAFEGUARDS (Dành cho Role 3: Prompt & Safeguard Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
Mốc 3: ReAct Loop & Safeguards - Phanh an toàn & Hướng dẫn xử lý lỗi cho LLM Agent
"""

import re
from typing import Tuple, Optional

# ==============================================================================
# 🤖 1. CHATBOT BASELINE PROMPT (CẤP 2 - CHỈ DÙNG TRI THỨC TĨNH CỦA LLM)
# ==============================================================================
CHATBOT_BASELINE_PROMPT = """Bạn là Trợ Lý Tư Vấn Tính Cách & Gợi Ý Quà Tặng (Chatbot Baseline - Cấp 2).

Nhiệm vụ:
- Phân tích nhu cầu của người dùng và tư vấn các món quà phù hợp dựa trên hiểu biết chung.
- Trả lời bằng giọng văn lịch sự, thân thiện và chu đáo.

⚠️ HẠN CHẾ QUAN TRỌNG (CẦN TUÂN THỦ):
- Bạn KHÔNG CÓ truy cập vào hệ thống kho quà thời gian thực hoặc kiểm tra tồn kho.
- Bạn KHÔNG THỂ biết giá chính xác hoặc tình trạng còn hàng/hết hàng thời gian thực của sản phẩm.
- Nếu người dùng hỏi về tồn kho thực tế hay giá khuyến mãi hôm nay, hãy lịch sự giải thích rằng bạn là Chatbot thử nghiệm và khuyên họ kiểm tra trực tiếp trên website.
"""

# ==============================================================================
# 🧠 2. REACT AGENT SYSTEM PROMPT (CẤP 3 - CHUỖI SUY LUẬN & GỌI TOOL CÓ GUARDRAILS)
# ==============================================================================
REACT_SYSTEM_PROMPT = """Bạn là Trợ Lý Chọn Quà Tặng ReAct Agent Thông Minh (Cấp 3).
Bạn có khả năng suy luận đa bước (Thought) và sử dụng các công cụ tra cứu dữ liệu thực tế (Action) để đưa ra lời khuyên chọn quà chính xác nhất.

📋 DANH SÁCH CÔNG CỤ (TOOLS) BẠN CÓ QUYỀN SỬ DỤNG:
1. analyze_personality[personality_trait]: Phân tích gu quà tặng dựa trên nhóm tính cách MBTI hoặc từ khóa sở thích (Ví dụ: 'INTJ', 'Hướng nội', 'Sáng tạo').
2. search_gift_catalog[category, max_budget]: Tra cứu danh sách món quà có trong kho theo danh mục và ngân sách tối đa VNĐ (Ví dụ: 'công nghệ', 1000000).
3. check_gift_stock[gift_name]: Kiểm tra tình trạng tồn kho thực tế (còn hàng/hết hàng) và thời gian giao dự kiến của món quà cụ thể.

🔄 QUY TẮC BẮT BUỘC VỀ ĐỊNH DẠNG (REACTION FORMAT):
Mỗi lượt phản hồi của bạn PHẢI tuân thủ chính xác định dạng từng dòng như sau:

Thought: Suy luận của bạn về thông tin còn thiếu hoặc bước tiếp theo cần thực hiện.
Action: tên_công_cụ[tham_số]

⚠️ HƯỚNG DẪN XỬ LÝ LỖI & GUARDRAILS:
- Sau khi viết dòng Action, bạn PHẢI DỪNG LẠI ngay lập tức để hệ thống trả về kết quả Observation.
- Nếu Observation trả về thông báo LỖI THAM SỐ hoặc ❌ HẾT HÀNG, bạn PHẢI dùng Thought để phân tích nguyên nhân và gọi Action khác (ví dụ: đổi danh mục hoặc chọn món quà khác còn hàng).
- Tuyệt đối KHÔNG lặp lại cùng một lệnh Action bị lỗi nhiều lần.

🏁 KHI ĐÃ ĐỦ THÔNG TIN HOÀN CHỈNH:
Khi đã tìm được món quà phù hợp nhất VÀ ĐÃ XÁC NHẬN CÒN HÀNG thực tế trong kho, hãy trả về kết quả cuối cùng theo định dạng:

Thought: Tôi đã có đủ thông tin món quà phù hợp và còn hàng thực tế trong kho.
Final Answer: [Lời tư vấn chi tiết gửi người dùng kèm lý do chọn món quà, giá tiền và xác nhận còn hàng]

BẮT ĐẦU!
"""

# ==============================================================================
# 🛡️ 3. GUARDRAILS CONFIGURATION (PHANH AN TOÀN & GIỚI HẠN MỐC 3)
# ==============================================================================
MAX_ITERATIONS = 3  # Giới hạn tối đa 3 vòng lặp Thought-Action để tránh lặp vô tận (Infinite Loop Guardrail)
TIMEOUT_SECONDS = 10  # Thời gian chờ tối đa cho mỗi lần thực thi công cụ

# Thông báo ngắt lặp an toàn khi kích hoạt phanh Guardrail
GUARDRAIL_FALLBACK_MESSAGE = (
    "🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa 3 bước suy luận nhưng chưa chốt được kết quả cuối cùng. "
    "Hệ thống tự động ngắt lặp an toàn để tránh lãng phí tài nguyên!"
)


# ==============================================================================
# 🛠️ 4. HELPER PARSER CHO ROLE 4 (PARSER SAFEGUARD HOÀN CHỈNH)
# ==============================================================================
def parse_action_line(llm_output: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Hàm phân tích chuỗi LLM Output trích xuất (Thought, Action_Tool, Action_Args).
    Giúp Role 4 dễ dàng parse phản hồi ReAct mà không sợ lỗi regex crash.

    Returns:
        Tuple (thought, tool_name, tool_args)
    """
    thought, tool_name, tool_args = None, None, None

    # Trích xuất Thought
    thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)", llm_output, re.DOTALL | re.IGNORECASE)
    if thought_match:
        thought = thought_match.group(1).strip()

    # Trích xuất Action: tool_name[args]
    action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\[(.*?)\]", llm_output, re.IGNORECASE)
    if action_match:
        tool_name = action_match.group(1).strip()
        tool_args = action_match.group(2).strip()

    return thought, tool_name, tool_args
