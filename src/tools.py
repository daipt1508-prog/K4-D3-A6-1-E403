"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
"""

def analyze_personality(personality_trait: str) -> str:
    """
    Phân tích đặc điểm tính cách / MBTI / sở thích để đưa ra gợi ý gu quà tặng phù hợp.
    
    Args:
        personality_trait (str): Nhóm tính cách hoặc sở thích (Ví dụ: 'INTJ', 'Hướng nội', 'Thích công nghệ', 'Yêu thiên nhiên')
        
    Returns:
        str: Phân tích gu quà tặng & phong cách phù hợp
    """
    trait_lower = personality_trait.lower()
    if "intj" in trait_lower or "công nghệ" in trait_lower or "lập trình" in trait_lower:
        return "Đặc điểm: Tư duy logic, thích sự tiện ích & tối giản. Gu quà: Đồ công nghệ, bàn phím cơ, sách chuyên ngành, tai nghe chống ồn."
    elif "enfp" in trait_lower or "sáng tạo" in trait_lower or "nghệ thuật" in trait_lower:
        return "Đặc điểm: Hướng ngoại, thích sự độc đáo & cảm xúc. Gu quà: Đồ handmade, máy chụp ảnh lấy liền, vé workshop nghệ thuật."
    elif "isfj" in trait_lower or "tinh tế" in trait_lower or "chăm sóc" in trait_lower:
        return "Đặc điểm: Chu đáo, thích sự ấm áp & ứng dụng thực tế. Gu quà: Nến thơm, bộ pha trà/coffee, khăn quàng, bình giữ nhiệt cao cấp."
    else:
        return f"Phân tích cơ bản cho '{personality_trait}': Nên chọn quà có tính ứng dụng cao, thiết kế tinh tế hoặc theo sở thích cá nhân."


def search_gift_catalog(category: str, max_budget: int = 1000000) -> str:
    """
    Tra cứu danh sách quà tặng trong kho theo danh mục/sở thích và ngân sách tối đa.
    
    Args:
        category (str): Danh mục hoặc sở thích (Ví dụ: 'công nghệ', 'sách', 'nến thơm', 'handmade')
        max_budget (int): Ngân sách tối đa tính bằng VNĐ (Mặc định: 1,000,000 VNĐ)
        
    Returns:
        str: Danh sách các món quà phù hợp kèm giá tiền
    """
    cat_lower = category.lower()
    if "công nghệ" in cat_lower or "tai nghe" in cat_lower or "bàn phím" in cat_lower:
        return (
            f"Danh sách quà [Công nghệ] (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Tai nghe Bluetooth Earbuds - Giá: 750,000 VNĐ\n"
            f"2. Bàn phím cơ Bluetooth Keychron - Giá: 1,800,000 VNĐ\n"
            f"3. Sạc dự phòng Anker 10000mAh - Giá: 450,000 VNĐ"
        )
    elif "nến thơm" in cat_lower or "tinh dầu" in cat_lower or "chăm sóc" in cat_lower:
        return (
            f"Danh sách quà [Chăm sóc/Thư giãn] (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Set Nến thơm & Tinh dầu thư giãn Organic - Giá: 350,000 VNĐ\n"
            f"2. Bình giữ nhiệt Lock&Lock 500ml - Giá: 280,000 VNĐ"
        )
    else:
        return (
            f"Danh sách quà tổng hợp theo chủ đề '{category}' (Ngân sách <= {max_budget:,} VNĐ):\n"
            f"1. Sách bestseller về phát triển bản thân - Giá: 180,000 VNĐ\n"
            f"2. Khung ảnh kỉ niệm kèm đèn LED - Giá: 250,000 VNĐ"
        )


def check_gift_stock(gift_name: str) -> str:
    """
    Kiểm tra tình trạng tồn kho và giao hàng của một món quà cụ thể.
    
    Args:
        gift_name (str): Tên món quà cần kiểm tra (Ví dụ: 'Tai nghe Bluetooth Earbuds', 'Set Nến thơm')
        
    Returns:
        str: Tình trạng kho (Còn hàng / Hết hàng) và thời gian giao dự kiến
    """
    name_lower = gift_name.lower()
    if "bàn phím" in name_lower:
        return f"Tình trạng '{gift_name}': ❌ HẾT HÀNG (Dự kiến nhập hàng sau 7 ngày)."
    else:
        return f"Tình trạng '{gift_name}': ✅ CÒN HÀNG (Sẵn sàng giao trong 24h)."


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "analyze_personality": analyze_personality,
    "search_gift_catalog": search_gift_catalog,
    "check_gift_stock": check_gift_stock,
}

