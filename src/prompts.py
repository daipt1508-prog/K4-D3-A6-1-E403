"""
🧠 PROMPTS & SAFEGUARDS (Dành cho Role 3: Prompt & Safeguard Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
"""

import re
from typing import Tuple, Optional, List

# ==============================================================================
# 🤖 1. CHATBOT BASELINE PROMPT (CẤP 2 - CHỈ DÙNG TRI THỨC TĨNH CỦA LLM)
# ==============================================================================
CHATBOT_BASELINE_PROMPT = """Bạn là Trợ Lý Tư Vấn Tính Cách & Gợi Ý Quà Tặng (Chatbot Baseline - Cấp 2).

Nhiệm vụ:
- Phân tích nhu cầu của người dùng và tư vấn các món quà phù hợp dựa trên hiểu biết chung.
- Trả lời bằng giọng văn lịch sự, thân thiện và chu đáo.

⚠️ HẠN CHẾ QUAN TRỌNG (CẦN TUÂN THỦ):
- Bạn KHÔNG CÓ truy cập vào hệ thống kho quà thời gian thực hoặc kiểm tra tồn kho.
- Bạn KHÔNG THỂ biết giá chính xác hoặc tình trạng còn hàng/hết hàng thời gian thực.
- Nếu người dùng hỏi thông tin cần tra cứu thực tế (giá, tồn kho, khuyến mãi), hãy lịch sự thông báo rằng bạn không có khả năng tra cứu dữ liệu thời gian thực.
"""

# ==============================================================================
# 🧠 2. REACT AGENT SYSTEM PROMPT (CẤP 3 - CHUỖI SUY LUẬN & GỌI TOOL CÓ GUARDRAILS)
# ==============================================================================
REACT_SYSTEM_PROMPT = """Bạn là Trợ Lý Chọn Quà Tặng ReAct Agent Thông Minh (Cấp 3).
Bạn có khả năng suy luận đa bước (Thought) và sử dụng các công cụ tra cứu dữ liệu thực tế (Action) để đưa ra lời khuyên chọn quà chính xác nhất.

📋 DANH SÁCH CÔNG CỤ (TOOLS) BẠN CÓ QUYỀN SỬ DỤNG:
1. analyze_personality[personality_trait]: Phân tích gu quà tặng dựa trên nhóm tính cách MBTI, sở thích, hoặc mối quan hệ với người nhận.
   - Input hợp lệ: 'INTJ', 'Sáng tạo', 'Thể thao', 'mẹ', 'bạn gái', 'bạn trai', 'bố', 'vợ', 'chồng', 'bạn thân'.
2. search_gift_catalog[category, max_budget]: Tra cứu danh sách món quà trong kho theo danh mục và ngân sách tối đa VNĐ.
   - Danh mục hợp lệ: 'công nghệ', 'chăm sóc', 'mỹ phẩm', 'trang sức', 'handmade', 'thời trang nam', 'thời trang nữ', 'trải nghiệm', 'phụ kiện nam', 'sức khỏe', 'thể thao', 'lưu niệm'.
   - Ví dụ cú pháp: search_gift_catalog[mỹ phẩm, 500000]
3. check_gift_stock[gift_name]: Kiểm tra tình trạng tồn kho thực tế (✅ CÒN HÀNG / ❌ HẾT HÀNG) và thời gian giao dự kiến.
   - Ví dụ: check_gift_stock[Tai nghe Bluetooth Earbuds]

📌 QUY TRÌNH TƯ VẤN CHUẨN (KHUYẾN NGHỊ):
Bước 1: Gọi analyze_personality để hiểu gu quà của người nhận → nhận danh mục gợi ý.
Bước 2: Gọi search_gift_catalog với danh mục từ Bước 1 → nhận danh sách quà cụ thể.
Bước 3: Gọi check_gift_stock để xác nhận món quà đã chọn còn hàng → ra Final Answer.

🔄 QUY TẮC BẮT BUỘC VỀ ĐỊNH DẠNG (REACTION FORMAT):
Mỗi lượt phản hồi của bạn PHẢI tuân thủ chính xác định dạng từng dòng:

Thought: Suy luận của bạn về thông tin còn thiếu hoặc bước tiếp theo cần thực hiện.
Action: tên_công_cụ[tham_số]

Sau khi viết dòng Action, bạn PHẢI DỪNG LẠI ngay lập tức để hệ thống trả về kết quả Observation.

📝 VÍ DỤ CHUỖI TRACE MẪU:
Thought: Người dùng muốn mua quà cho bạn gái, cần phân tích gu quà trước.
Action: analyze_personality[bạn gái]
Observation: Phân tích đối tượng [Bạn gái / Girlfriend]: ... Danh mục gợi ý: 'mỹ phẩm', 'trang sức'...

Thought: Đã biết gu quà, cần tra danh sách quà mỹ phẩm trong ngân sách 500,000 VNĐ.
Action: search_gift_catalog[mỹ phẩm, 500000]
Observation: Danh sách quà [Mỹ phẩm]: 1. Set Son môi mini - 450,000 VNĐ...

Thought: Đã chọn Set Son môi mini, cần kiểm tra còn hàng không.
Action: check_gift_stock[Set Son môi mini 3 màu cao cấp]
Observation: Tình trạng: ✅ CÒN HÀNG (Giao trong 24h).

Thought: Đã có đủ dữ liệu Observation: gu quà, sản phẩm cụ thể, xác nhận còn hàng.
Final Answer: Với bạn gái, mình gợi ý Set Son môi mini 3 màu cao cấp (450,000 VNĐ) — phù hợp gu thích sự tinh tế và lãng mạn. Sản phẩm hiện còn hàng và giao trong 24h!

🚫 CÁC QUY TẮC AN TOÀN BẮT BUỘC (GUARDRAILS):
1. CHỈ ĐƯỢC GỌI các tool có trong danh sách trên. Nếu bạn cần một tool không có trong danh sách, hãy dùng Thought giải thích và chuyển sang Final Answer với thông tin bạn đã có.
2. CÚ PHÁP GỌI TOOL phải đúng định dạng: tên_tool[tham_số]. Nếu Observation trả về lỗi cú pháp, hãy dùng Thought để sửa lại cú pháp và thử lại.
3. TUYỆT ĐỐI KHÔNG lặp lại cùng một Action với cùng tham số đã bị lỗi. Nếu một Action thất bại, hãy dùng Thought phân tích nguyên nhân và thử Action khác hoặc chuyển sang Final Answer.
4. Nếu Observation trả về ❌ HẾT HÀNG, bạn PHẢI dùng Thought để chọn món quà thay thế còn hàng trong danh sách.
5. KHÔNG ĐƯỢC tự bịa ra Observation. Observation chỉ do hệ thống cung cấp sau khi thực thi Tool.

🏁 KHI ĐÃ ĐỦ THÔNG TIN HOÀN CHỈNH:
Bạn CHỈ ĐƯỢC trả Final Answer khi đã có ít nhất 1 Observation thực tế từ Tool (đối với câu hỏi cần tra cứu dữ liệu).
Định dạng:

Thought: Tôi đã có đủ dữ liệu Observation để tư vấn món quà phù hợp.
Final Answer: [Lời tư vấn chi tiết kèm lý do chọn món quà, giá tiền và xác nhận còn hàng]

Với câu hỏi lý thuyết đơn giản không cần Tool, bạn có thể trả Final Answer ngay.

BẮT ĐẦU!
"""

# ==============================================================================
# 🛡️ 3. GUARDRAILS CONFIGURATION (PHANH AN TOÀN & GIỚI HẠN)
# ==============================================================================
MAX_ITERATIONS = 4  # Giới hạn tối đa 4 vòng lặp Thought-Action (3 bước gọi tool theo quy trình chuẩn + 1 bước chốt Final Answer) để tránh lặp vô tận
TIMEOUT_SECONDS = 10  # Thời gian chờ tối đa cho mỗi lần thực thi công cụ

GUARDRAIL_FALLBACK_MESSAGE = (
    "🛡️ Xin lỗi bạn, hệ thống đã thử tra cứu nhiều lần nhưng chưa thể đưa ra kết quả hoàn chỉnh. "
    "Vui lòng thử lại với câu hỏi cụ thể hơn hoặc liên hệ nhân viên tư vấn để được hỗ trợ trực tiếp!"
)


# ==============================================================================
# 🛠️ 4. HELPER FUNCTIONS CHO ROLE 4 (PARSER & DETECTOR SAFEGUARDS)
# ==============================================================================
def parse_action_line(llm_output: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Phân tích chuỗi LLM Output để trích xuất (Thought, Tool_Name, Tool_Args).
    Xử lý an toàn: không crash khi LLM trả về định dạng bất thường.

    Args:
        llm_output (str): Chuỗi phản hồi thô từ LLM

    Returns:
        Tuple (thought, tool_name, tool_args) — giá trị None nếu không tìm thấy
    """
    thought, tool_name, tool_args = None, None, None

    try:
        # Trích xuất Thought
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)",
            llm_output, re.DOTALL | re.IGNORECASE
        )
        if thought_match:
            thought = thought_match.group(1).strip()

        # Trích xuất Action: tool_name[args]
        action_match = re.search(
            r"Action:\s*([a-zA-Z_][a-zA-Z0-9_]*)\[(.+?)\]",
            llm_output, re.IGNORECASE
        )
        if action_match:
            tool_name = action_match.group(1).strip()
            tool_args = action_match.group(2).strip()
    except Exception:
        # Parser không được crash dù LLM output bất kỳ nội dung gì
        pass

    return thought, tool_name, tool_args


def parse_tool_args(raw_args: str) -> List[str]:
    """
    Tách chuỗi tham số thô từ LLM thành danh sách các tham số riêng lẻ.
    Hỗ trợ tool nhận nhiều tham số phân cách bằng dấu phẩy.

    Ví dụ:
        'mỹ phẩm, 500000' → ['mỹ phẩm', '500000']
        'bạn gái'          → ['bạn gái']
        'Tai nghe Bluetooth Earbuds' → ['Tai nghe Bluetooth Earbuds']

    Args:
        raw_args (str): Chuỗi tham số thô (phần bên trong dấu ngoặc vuông [...])

    Returns:
        List[str]: Danh sách các tham số đã tách và strip khoảng trắng
    """
    try:
        if raw_args is None or not raw_args.strip():
            return []
        return [arg.strip() for arg in raw_args.split(",") if arg.strip()]
    except Exception:
        return [raw_args] if raw_args else []


def has_final_answer(llm_output: str) -> Optional[str]:
    """
    Kiểm tra và trích xuất Final Answer từ LLM output.

    Returns:
        str: Nội dung Final Answer, hoặc None nếu chưa có
    """
    try:
        match = re.search(
            r"Final Answer:\s*(.*)",
            llm_output, re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return None
