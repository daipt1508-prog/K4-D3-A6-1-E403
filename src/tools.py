"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
Mốc 3: ReAct Loop Safeguards - Xử lý ngoại lệ an toàn & Chống crash ứng dụng
"""

from typing import Dict, Any, Callable
import traceback


def analyze_personality(personality_trait: str) -> str:
    """
    Phân tích đặc điểm tính cách (MBTI/Sở thích/Phong cách) và đưa ra gợi ý gu quà tặng phù hợp.

    Args:
        personality_trait (str): Nhóm tính cách MBTI (INTJ, ENFP, ISFJ...) hoặc từ khóa sở thích
                                (Ví dụ: 'INTJ', 'Hướng nội', 'Thích công nghệ', 'Yêu nghệ thuật', 'Sáng tạo')

    Returns:
        str: Phân tích đặc điểm tâm lý & danh mục món quà gợi ý phù hợp nhất.
             Trả về thông báo lỗi thay vì crash nếu gặp ngoại lệ.
    """
    try:
        if personality_trait is None or not isinstance(personality_trait, str) or not personality_trait.strip():
            return "LỖI THAM SỐ [analyze_personality]: Vui lòng cung cấp nhóm tính cách hoặc sở thích hợp lệ (Ví dụ: 'INTJ', 'Hướng nội')."

        trait_lower = personality_trait.strip().lower()

        if any(k in trait_lower for k in ["intj", "công nghệ", "lập trình", "logic", "istj"]):
            return (
                "Phân tích tính cách [Hướng nội - Logic - Tiện ích]:\n"
                "- Đặc điểm: Tư duy phân tích, thích sự ngăn nắp, tối giản và tính ứng dụng cao.\n"
                "- Gu quà phù hợp: Thiết bị công nghệ, phụ kiện máy tính, sách chuyên ngành, tai nghe chống ồn."
            )
        elif any(k in trait_lower for k in ["enfp", "sáng tạo", "nghệ thuật", "hướng ngoại", "esfp"]):
            return (
                "Phân tích tính cách [Hướng ngoại - Sáng tạo - Cảm xúc]:\n"
                "- Đặc điểm: Thích sự độc đáo, trải nghiệm mới mẻ, trân trọng giá trị tinh thần.\n"
                "- Gu quà phù hợp: Đồ handmade cá nhân hóa, máy chụp ảnh lấy liền, vé workshop trải nghiệm."
            )
        elif any(k in trait_lower for k in ["isfj", "tinh tế", "chăm sóc", "ấm áp", "infj"]):
            return (
                "Phân tích tính cách [Tinh tế - Chu đáo - Chăm sóc]:\n"
                "- Đặc điểm: Quan tâm chi tiết, yêu thích sự thư giãn và không gian ấm cúng.\n"
                "- Gu quà phù hợp: Set nến thơm tinh dầu, bộ pha trà/coffee, bình giữ nhiệt cao cấp, khăn quàng."
            )
        else:
            return (
                f"Phân tích tổng quan cho nhóm '{personality_trait}':\n"
                "- Đặc điểm: Phong cách linh hoạt, trân trọng sự chân thành.\n"
                "- Gu quà phù hợp: Chọn món quà có tính thực tế cao hoặc đồ trang trí cá nhân hóa."
            )
    except Exception as e:
        return f"LỖI THỰC THI TOOL [analyze_personality]: Bắt được ngoại lệ ngoài dự kiến - {str(e)}"


def search_gift_catalog(category: str, max_budget: int = 1000000) -> str:
    """
    Tra cứu danh sách các món quà khả dụng trong kho theo danh mục/sở thích và ngân sách tối đa.

    Args:
        category (str): Danh mục món quà hoặc sở thích (Ví dụ: 'công nghệ', 'sách', 'nến thơm', 'handmade')
        max_budget (int): Ngân sách tối đa tính bằng VNĐ (Mặc định: 1,000,000 VNĐ). Phải lớn hơn 0.

    Returns:
        str: Danh sách món quà tìm thấy kèm giá tiền thực tế.
             Trả về thông báo lỗi thay vì crash nếu ngân sách hoặc tham số không hợp lệ.
    """
    try:
        if category is None or not isinstance(category, str) or not category.strip():
            return "LỖI THAM SỐ [search_gift_catalog]: Danh mục tìm kiếm không được để trống."

        try:
            max_budget_val = int(max_budget)
            if max_budget_val <= 0:
                return "LỖI THAM SỐ [search_gift_catalog]: Ngân sách tối đa phải lớn hơn 0 VNĐ."
        except (ValueError, TypeError):
            return f"LỖI THAM SỐ [search_gift_catalog]: Ngân sách '{max_budget}' không đúng định dạng số nguyên."

        cat_lower = category.strip().lower()

        if any(k in cat_lower for k in ["công nghệ", "tai nghe", "bàn phím", "phụ kiện"]):
            return (
                f"Danh sách quà [Công nghệ] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Tai nghe Bluetooth Earbuds - Giá: 750,000 VNĐ\n"
                f"2. Bàn phím cơ Bluetooth Keychron - Giá: 1,800,000 VNĐ\n"
                f"3. Sạc dự phòng Anker 10000mAh - Giá: 450,000 VNĐ"
            )
        elif any(k in cat_lower for k in ["nến thơm", "tinh dầu", "chăm sóc", "thư giãn"]):
            return (
                f"Danh sách quà [Chăm sóc / Thư giãn] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Set Nến thơm & Tinh dầu thư giãn Organic - Giá: 350,000 VNĐ\n"
                f"2. Bình giữ nhiệt Lock&Lock 500ml - Giá: 280,000 VNĐ"
            )
        else:
            return (
                f"Danh sách quà [Tổng hợp] trong kho theo chủ đề '{category}' (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Sách bestseller về phát triển bản thân - Giá: 180,000 VNĐ\n"
                f"2. Khung ảnh kỉ niệm kèm đèn LED - Giá: 250,000 VNĐ"
            )
    except Exception as e:
        return f"LỖI THỰC THI TOOL [search_gift_catalog]: Bắt được ngoại lệ ngoài dự kiến - {str(e)}"


def check_gift_stock(gift_name: str) -> str:
    """
    Kiểm tra tình trạng tồn kho thực tế và khả năng giao hàng của một món quà cụ thể.

    Args:
        gift_name (str): Tên cụ thể của món quà cần kiểm tra tồn kho (Ví dụ: 'Tai nghe Bluetooth Earbuds', 'Bàn phím cơ')

    Returns:
        str: Trạng thái tồn kho (✅ CÒN HÀNG hoặc ❌ HẾT HÀNG) và thời gian giao hàng dự kiến.
             Trả về thông báo lỗi thay vì crash nếu gặp ngoại lệ.
    """
    try:
        if gift_name is None or not isinstance(gift_name, str) or not gift_name.strip():
            return "LỖI THAM SỐ [check_gift_stock]: Tên món quà cần kiểm tra không được để trống."

        name_lower = gift_name.strip().lower()

        if "bàn phím" in name_lower:
            return f"Tình trạng '{gift_name}': ❌ HẾT HÀNG (Dự kiến nhập kho bổ sung sau 7 ngày)."
        else:
            return f"Tình trạng '{gift_name}': ✅ CÒN HÀNG (Sẵn sàng giao ngay trong 24h)."
    except Exception as e:
        return f"LỖI THỰC THI TOOL [check_gift_stock]: Bắt được ngoại lệ ngoài dự kiến - {str(e)}"


# Registration Dictionary phục vụ Agent Tool Registry
AVAILABLE_TOOLS: Dict[str, Callable[..., str]] = {
    "analyze_personality": analyze_personality,
    "search_gift_catalog": search_gift_catalog,
    "check_gift_stock": check_gift_stock,
}


def execute_tool_safely(tool_name: str, *args, **kwargs) -> str:
    """
    Hàm thực thi Tool an toàn tuyệt đối (Safety Guardrail Execution Wrapper).
    Giúp Role 4 gọi bất kỳ tool nào theo tên chuỗi mà không lo crash chương trình khi tool gặp lỗi.

    Args:
        tool_name (str): Tên tool cần thực thi ('analyze_personality', 'search_gift_catalog', 'check_gift_stock')

    Returns:
        str: Kết quả Observation thực tế hoặc chuỗi thông báo lỗi an toàn.
    """
    try:
        if tool_name not in AVAILABLE_TOOLS:
            return f"LỖI HỆ THỐNG: Công cụ '{tool_name}' không tồn tại trong Registry. Các công cụ khả dụng: {list(AVAILABLE_TOOLS.keys())}"

        tool_func = AVAILABLE_TOOLS[tool_name]
        return tool_func(*args, **kwargs)
    except Exception as e:
        return f"LỖI THỰC THI AN TOÀN [{tool_name}]: {str(e)}"


def get_tool_specs() -> str:
    """
    Hàm hỗ trợ trích xuất toàn bộ Tool Specifications chuẩn hóa dạng văn bản cho Role 3 & Role 4.
    """
    specs = []
    for name, func in AVAILABLE_TOOLS.items():
        doc = func.__doc__.strip() if func.__doc__ else "Không có mô tả"
        specs.append(f"- {name}: {doc.splitlines()[0]}")
    return "\n".join(specs)



