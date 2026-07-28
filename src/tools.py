"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
Mốc 2: Chuẩn hóa Tool Specs & Docstrings cho LLM Agent
"""

from typing import Dict, Any, Callable


def analyze_personality(personality_trait: str) -> str:
    """
    Phân tích đặc điểm tính cách (MBTI/Sở thích/Phong cách) và đưa ra gợi ý gu quà tặng phù hợp.

    Args:
        personality_trait (str): Nhóm tính cách MBTI (INTJ, ENFP, ISFJ...) hoặc từ khóa sở thích
                                (Ví dụ: 'INTJ', 'Hướng nội', 'Thích công nghệ', 'Yêu nghệ thuật', 'Sáng tạo')

    Returns:
        str: Phân tích đặc điểm tâm lý & danh mục món quà gợi ý phù hợp nhất.
             Trả về thông báo hướng dẫn nếu đầu vào trống hoặc không hợp lệ.

    Example:
        >>> analyze_personality("INTJ")
        "Đặc điểm: Tư duy logic, thích sự tiện ích & tối giản..."
    """
    if not personality_trait or not isinstance(personality_trait, str):
        return "LỖI THAM SỐ: Vui lòng cung cấp nhóm tính cách hoặc sở thích (Ví dụ: 'INTJ', 'Hướng nội', 'Thích công nghệ')."

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


def search_gift_catalog(category: str, max_budget: int = 1000000) -> str:
    """
    Tra cứu danh sách các món quà khả dụng trong kho theo danh mục/sở thích và ngân sách tối đa.

    Args:
        category (str): Danh mục món quà hoặc sở thích (Ví dụ: 'công nghệ', 'sách', 'nến thơm', 'handmade')
        max_budget (int): Ngân sách tối đa tính bằng VNĐ (Mặc định: 1,000,000 VNĐ). Phải lớn hơn 0.

    Returns:
        str: Danh sách món quà tìm thấy kèm mã quà, giá tiền thực tế.
             Trả về báo lỗi nếu ngân sách không hợp lệ.

    Example:
        >>> search_gift_catalog("công nghệ", 1000000)
        "Danh sách quà [Công nghệ] (Ngân sách <= 1,000,000 VNĐ)..."
    """
    if not category or not isinstance(category, str):
        return "LỖI THAM SỐ: Danh mục tìm kiếm không được để trống."

    try:
        max_budget = int(max_budget)
        if max_budget <= 0:
            return "LỖI THAM SỐ: Ngân sách tối đa phải lớn hơn 0 VNĐ."
    except (ValueError, TypeError):
        return f"LỖI THAM SỐ: Ngân sách '{max_budget}' không đúng định dạng số nguyên."

    cat_lower = category.strip().lower()

    if any(k in cat_lower for k in ["công nghệ", "tai nghe", "bàn phím", "phụ kiện"]):
        return (
            f"Danh sách quà [Công nghệ] trong kho (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Tai nghe Bluetooth Earbuds - Giá: 750,000 VNĐ\n"
            f"2. Bàn phím cơ Bluetooth Keychron - Giá: 1,800,000 VNĐ\n"
            f"3. Sạc dự phòng Anker 10000mAh - Giá: 450,000 VNĐ"
        )
    elif any(k in cat_lower for k in ["nến thơm", "tinh dầu", "chăm sóc", "thư giãn"]):
        return (
            f"Danh sách quà [Chăm sóc / Thư giãn] trong kho (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Set Nến thơm & Tinh dầu thư giãn Organic - Giá: 350,000 VNĐ\n"
            f"2. Bình giữ nhiệt Lock&Lock 500ml - Giá: 280,000 VNĐ"
        )
    else:
        return (
            f"Danh sách quà [Tổng hợp] trong kho theo chủ đề '{category}' (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Sách bestseller về phát triển bản thân - Giá: 180,000 VNĐ\n"
            f"2. Khung ảnh kỉ niệm kèm đèn LED - Giá: 250,000 VNĐ"
        )


def check_gift_stock(gift_name: str) -> str:
    """
    Kiểm tra tình trạng tồn kho thực tế và khả năng giao hàng của một món quà cụ thể.

    Args:
        gift_name (str): Tên cụ thể của món quà cần kiểm tra tồn kho (Ví dụ: 'Tai nghe Bluetooth Earbuds', 'Bàn phím cơ')

    Returns:
        str: Trạng thái tồn kho (✅ CÒN HÀNG hoặc ❌ HẾT HÀNG) và thời gian giao hàng dự kiến.

    Example:
        >>> check_gift_stock("Tai nghe Bluetooth Earbuds")
        "Tình trạng 'Tai nghe Bluetooth Earbuds': ✅ CÒN HÀNG (Sẵn sàng giao trong 24h)."
    """
    if not gift_name or not isinstance(gift_name, str):
        return "LỖI THAM SỐ: Tên món quà cần kiểm tra không được để trống."

    name_lower = gift_name.strip().lower()

    if "bàn phím" in name_lower:
        return f"Tình trạng '{gift_name}': ❌ HẾT HÀNG (Dự kiến nhập kho bổ sung sau 7 ngày)."
    else:
        return f"Tình trạng '{gift_name}': ✅ CÒN HÀNG (Sẵn sàng giao ngay trong 24h)."


# Registration Dictionary phục vụ Agent Tool Registry
AVAILABLE_TOOLS: Dict[str, Callable[..., str]] = {
    "analyze_personality": analyze_personality,
    "search_gift_catalog": search_gift_catalog,
    "check_gift_stock": check_gift_stock,
}


def get_tool_specs() -> str:
    """
    Hàm hỗ trợ trích xuất toàn bộ Tool Specifications chuẩn hóa dạng văn bản cho Role 3 & Role 4.
    """
    specs = []
    for name, func in AVAILABLE_TOOLS.items():
        doc = func.__doc__.strip() if func.__doc__ else "Không có mô tả"
        specs.append(f"- {name}: {doc.splitlines()[0]}")
    return "\n".join(specs)


