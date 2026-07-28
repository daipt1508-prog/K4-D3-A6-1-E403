"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề 3: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp
"""

import unicodedata
from typing import Dict, Callable


def _normalize(text: str) -> str:
    """Chuẩn hóa chuỗi tiếng Việt: lowercase + bỏ dấu để khớp cả input có dấu và không dấu."""
    text = text.strip().lower()
    # Decompose unicode rồi loại bỏ combining marks (dấu)
    nfkd = unicodedata.normalize('NFKD', text)
    no_diacritics = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    # Xử lý đặc biệt: đ -> d
    no_diacritics = no_diacritics.replace('đ', 'd')
    return no_diacritics


# ==============================================================================
# 🔧 TOOL 1: analyze_personality
# ==============================================================================
def analyze_personality(personality_trait: str) -> str:
    """
    Phân tích đặc điểm tính cách, mối quan hệ hoặc sở thích để gợi ý gu quà tặng phù hợp.

    ── Tool Contract ──
    Name:         analyze_personality
    Purpose:      Dùng khi cần hiểu người nhận quà thuộc nhóm nào để gợi ý danh mục quà.
                  Hỗ trợ: MBTI, sở thích, và đối tượng theo mối quan hệ (mẹ, bạn gái, bạn trai, bố, vợ, chồng...).
                  KHÔNG dùng khi đã biết rõ danh mục quà cần tìm.
    Input:        personality_trait (str) — Nhóm MBTI, từ khóa sở thích, hoặc mối quan hệ
                  Ví dụ: 'INTJ', 'Thích công nghệ', 'mẹ', 'bạn gái', 'bạn trai', 'bố'
    Output:       Chuỗi phân tích đặc điểm & danh mục quà gợi ý theo từng đối tượng
    Error:        Trả chuỗi "LỖI THAM SỐ [...]" nếu đầu vào trống/sai kiểu — KHÔNG crash
    Side-effect:  Read-only, không thay đổi trạng thái
    Safety:       Toàn bộ logic bọc trong try-except, luôn trả về str
    """
    try:
        if personality_trait is None or not isinstance(personality_trait, str) or not personality_trait.strip():
            return (
                "LỖI THAM SỐ [analyze_personality]: Vui lòng cung cấp thông tin về người nhận quà.\n"
                "Ví dụ: 'INTJ', 'Thích công nghệ', 'mẹ', 'bạn gái', 'bạn trai', 'bố', 'Hướng nội'."
            )

        trait_raw = personality_trait.strip().lower()
        trait_norm = _normalize(personality_trait)

        def _match(keywords):
            """Khớp từ khóa trên cả bản có dấu và không dấu."""
            return any(k in trait_raw or k in trait_norm for k in keywords)

        # ── Phân tích theo MỐI QUAN HỆ (thứ tự ưu tiên: cụm dài trước) ──
        if _match(["bạn gái", "ban gai", "người yêu nữ", "girlfriend", "ny nu"]):
            return (
                "Phân tích đối tượng [Bạn gái / Girlfriend]:\n"
                "- Đặc điểm chung: Thích sự bất ngờ & lãng mạn, trân trọng chi tiết nhỏ, yêu thích cảm xúc và sự tinh tế.\n"
                "- Gu quà phù hợp: Son môi cao cấp, nước hoa mini set, gấu bông, vòng tay/dây chuyền, album ảnh handmade, hoa tươi kèm quà, voucher workshop trải nghiệm.\n"
                "- Danh mục gợi ý để tra cứu: 'mỹ phẩm', 'trang sức', 'handmade', 'trải nghiệm'.\n"
                "- Lưu ý: Quà cá nhân hóa (khắc tên, in ảnh) thường ghi điểm cao hơn quà đắt tiền nhưng chung chung."
            )
        elif _match(["bạn trai", "ban trai", "người yêu nam", "boyfriend", "ny nam"]):
            return (
                "Phân tích đối tượng [Bạn trai / Boyfriend]:\n"
                "- Đặc điểm chung: Thích sự tiện dụng & phong cách, trân trọng đồ có tính ứng dụng thực tế.\n"
                "- Gu quà phù hợp: Ví da, thắt lưng, tai nghe Bluetooth, đồng hồ thể thao, bàn phím cơ, sạc dự phòng, áo thun thiết kế, bộ chăm sóc da nam.\n"
                "- Danh mục gợi ý để tra cứu: 'công nghệ', 'thời trang nam', 'phụ kiện nam'.\n"
                "- Lưu ý: Quà thực tế dùng hàng ngày thường được bạn trai đánh giá cao hơn quà trang trí."
            )
        elif _match(["bạn thân", "ban than", "bạn bè", "ban be", "friend", "bestie"]):
            return (
                "Phân tích đối tượng [Bạn thân / Best Friend]:\n"
                "- Đặc điểm chung: Trân trọng kỉ niệm chung, thích sự vui vẻ & độc đáo.\n"
                "- Gu quà phù hợp: Album ảnh kỉ niệm, cốc in ảnh cá nhân hóa, khung ảnh LED, đồ handmade, vé xem phim/concert, board game.\n"
                "- Danh mục gợi ý để tra cứu: 'handmade', 'trải nghiệm', 'lưu niệm'.\n"
                "- Lưu ý: Quà gắn liền kỉ niệm chung (ảnh, nội dung inside joke) luôn ghi điểm tuyệt đối."
            )
        elif _match(["mẹ", "me", "ma", "mother", "mom"]):
            return (
                "Phân tích đối tượng [Mẹ / Mother]:\n"
                "- Đặc điểm chung: Yêu thương gia đình, quan tâm sức khỏe, thích sự thực tế & ý nghĩa tinh thần.\n"
                "- Gu quà phù hợp: Set chăm sóc sức khỏe (tinh dầu, nến thơm), bình giữ nhiệt cao cấp, khăn lụa, bộ pha trà/coffee, túi xách thời trang, voucher spa thư giãn.\n"
                "- Danh mục gợi ý để tra cứu: 'chăm sóc', 'thời trang nữ', 'sức khỏe'.\n"
                "- Lưu ý: Mẹ thường trân trọng quà mang tính chân thành hơn giá trị vật chất."
            )
        elif _match(["bố", "bo", "cha", "father", "dad"]):
            return (
                "Phân tích đối tượng [Bố / Father]:\n"
                "- Đặc điểm chung: Thích sự bền bỉ, giản dị & thiết thực, trân trọng sức khỏe và gia đình.\n"
                "- Gu quà phù hợp: Bình giữ nhiệt inox, ví da cao cấp, trà/coffee đặc biệt, máy massage cầm tay, đồng hồ, áo polo chất lượng.\n"
                "- Danh mục gợi ý để tra cứu: 'sức khỏe', 'phụ kiện nam', 'thời trang nam'.\n"
                "- Lưu ý: Bố ít khi tự mua đồ cho mình, nên quà chăm sóc cá nhân rất có ý nghĩa."
            )
        elif _match(["vợ", "vo", "wife"]):
            return (
                "Phân tích đối tượng [Vợ / Wife]:\n"
                "- Đặc điểm chung: Trân trọng sự quan tâm & thấu hiểu, thích quà mang tính chăm sóc và lãng mạn.\n"
                "- Gu quà phù hợp: Trang sức, nước hoa, set chăm sóc da cao cấp, voucher spa, khăn lụa, túi xách, hoa tươi kèm thiệp viết tay.\n"
                "- Danh mục gợi ý để tra cứu: 'mỹ phẩm', 'trang sức', 'chăm sóc', 'trải nghiệm'.\n"
                "- Lưu ý: Thiệp viết tay kèm quà luôn tăng giá trị cảm xúc lên gấp đôi."
            )
        elif _match(["chồng", "chong", "husband"]):
            return (
                "Phân tích đối tượng [Chồng / Husband]:\n"
                "- Đặc điểm chung: Thích sự tiện dụng, coi trọng chất lượng sản phẩm và trải nghiệm thực tế.\n"
                "- Gu quà phù hợp: Đồng hồ, ví da, tai nghe cao cấp, máy cạo râu, phụ kiện công nghệ, quần áo thể thao, voucher ăn tối.\n"
                "- Danh mục gợi ý để tra cứu: 'công nghệ', 'phụ kiện nam', 'trải nghiệm'.\n"
                "- Lưu ý: Một bữa tối bất ngờ + quà nhỏ thường ý nghĩa hơn một món quà đắt tiền đơn lẻ."
            )

        # ── Phân tích theo MBTI / SỞ THÍCH ──
        elif _match(["intj", "cong nghe", "lap trinh", "logic", "istj", "intp"]):
            return (
                "Phân tích tính cách [Hướng nội - Logic - Tiện ích]:\n"
                "- Đặc điểm: Tư duy phân tích, thích sự ngăn nắp, tối giản và tính ứng dụng cao.\n"
                "- Gu quà phù hợp: Thiết bị công nghệ, phụ kiện máy tính, sách chuyên ngành, tai nghe chống ồn, bàn phím cơ.\n"
                "- Danh mục gợi ý để tra cứu: 'công nghệ'."
            )
        elif _match(["enfp", "sang tao", "nghe thuat", "huong ngoai", "esfp", "enfj"]):
            return (
                "Phân tích tính cách [Hướng ngoại - Sáng tạo - Cảm xúc]:\n"
                "- Đặc điểm: Thích sự độc đáo, trải nghiệm mới mẻ, trân trọng giá trị tinh thần.\n"
                "- Gu quà phù hợp: Đồ handmade cá nhân hóa, máy chụp ảnh lấy liền, vé workshop trải nghiệm, sổ tay sáng tạo.\n"
                "- Danh mục gợi ý để tra cứu: 'handmade', 'trải nghiệm'."
            )
        elif _match(["isfj", "tinh te", "cham soc", "am ap", "infj", "infp"]):
            return (
                "Phân tích tính cách [Tinh tế - Chu đáo - Chăm sóc]:\n"
                "- Đặc điểm: Quan tâm chi tiết, yêu thích sự thư giãn và không gian ấm cúng.\n"
                "- Gu quà phù hợp: Set nến thơm tinh dầu, bộ pha trà/coffee, bình giữ nhiệt cao cấp, khăn quàng.\n"
                "- Danh mục gợi ý để tra cứu: 'chăm sóc'."
            )
        elif _match(["the thao", "gym", "estp", "istp", "outdoor", "khoe"]):
            return (
                "Phân tích tính cách [Năng động - Thể thao - Outdoor]:\n"
                "- Đặc điểm: Yêu thích vận động, coi trọng sức khỏe và sự tiện lợi khi di chuyển.\n"
                "- Gu quà phù hợp: Bình nước thể thao, dây nhảy cao cấp, đai đeo tay chạy bộ, áo thể thao, tai nghe thể thao chống nước.\n"
                "- Danh mục gợi ý để tra cứu: 'thể thao', 'sức khỏe'."
            )

        # ── Fallback tổng quát ──
        else:
            return (
                f"Phân tích tổng quan cho '{personality_trait}':\n"
                "- Đặc điểm: Phong cách linh hoạt, trân trọng sự chân thành.\n"
                "- Gu quà phù hợp: Chọn món quà có tính thực tế cao hoặc đồ cá nhân hóa.\n"
                "- Danh mục gợi ý để tra cứu: 'tổng hợp'.\n"
                "- Mẹo: Hãy thử mô tả cụ thể hơn (VD: 'mẹ', 'bạn gái thích nghệ thuật', 'bạn trai thích công nghệ') để nhận gợi ý chính xác hơn."
            )
    except Exception as e:
        return f"LỖI THỰC THI [analyze_personality]: {str(e)}"


# ==============================================================================
# 🔧 TOOL 2: search_gift_catalog
# ==============================================================================
def search_gift_catalog(category: str, max_budget: int = 1000000) -> str:
    """
    Tra cứu danh sách món quà khả dụng trong kho theo danh mục và ngân sách tối đa.

    ── Tool Contract ──
    Name:         search_gift_catalog
    Purpose:      Dùng khi đã biết danh mục quà cần tìm (từ kết quả analyze_personality hoặc yêu cầu trực tiếp).
                  KHÔNG dùng khi chưa biết người nhận thích gì (nên gọi analyze_personality trước).
    Input:        category (str)   — Danh mục: 'công nghệ', 'chăm sóc', 'mỹ phẩm', 'trang sức',
                                     'handmade', 'thời trang nam', 'thời trang nữ', 'trải nghiệm',
                                     'phụ kiện nam', 'sức khỏe', 'thể thao', 'lưu niệm'...
                  max_budget (int) — Ngân sách tối đa VNĐ, mặc định 1,000,000. Phải > 0.
    Output:       Danh sách món quà kèm giá tiền thực tế
    Error:        Trả chuỗi "LỖI THAM SỐ [...]" nếu danh mục trống hoặc ngân sách <= 0
    Side-effect:  Read-only
    Safety:       Toàn bộ logic bọc trong try-except, luôn trả về str
    """
    try:
        if category is None or not isinstance(category, str) or not category.strip():
            return (
                "LỖI THAM SỐ [search_gift_catalog]: Danh mục tìm kiếm không được để trống.\n"
                "Các danh mục hợp lệ: 'công nghệ', 'chăm sóc', 'mỹ phẩm', 'trang sức', 'handmade', "
                "'thời trang nam', 'thời trang nữ', 'trải nghiệm', 'phụ kiện nam', 'sức khỏe', 'thể thao', 'lưu niệm'."
            )

        try:
            max_budget_val = int(max_budget)
            if max_budget_val <= 0:
                return "LỖI THAM SỐ [search_gift_catalog]: Ngân sách tối đa phải lớn hơn 0 VNĐ."
        except (ValueError, TypeError):
            return f"LỖI THAM SỐ [search_gift_catalog]: Ngân sách '{max_budget}' không đúng định dạng số nguyên."

        cat_lower = category.strip().lower()
        cat_norm = _normalize(category)

        def _cat_match(keywords):
            return any(k in cat_lower or k in cat_norm for k in keywords)

        # ── Công nghệ & Phụ kiện kỹ thuật số ──
        if _cat_match(["cong nghe", "tai nghe", "ban phim", "phu kien", "tech"]):
            return (
                f"Danh sách quà [Công nghệ] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Tai nghe Bluetooth Earbuds - Giá: 750,000 VNĐ\n"
                f"2. Bàn phím cơ Bluetooth Keychron K3 - Giá: 1,800,000 VNĐ\n"
                f"3. Sạc dự phòng Anker 10000mAh - Giá: 450,000 VNĐ\n"
                f"4. Chuột không dây Logitech Pebble - Giá: 390,000 VNĐ\n"
                f"5. Đèn LED bàn học thông minh - Giá: 320,000 VNĐ"
            )

        # ── Chăm sóc / Thư giãn / Sức khỏe ──
        elif _cat_match(["cham soc", "nen thom", "tinh dau", "thu gian", "suc khoe", "spa"]):
            return (
                f"Danh sách quà [Chăm sóc / Sức khỏe] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Set Nến thơm & Tinh dầu Organic - Giá: 350,000 VNĐ\n"
                f"2. Bình giữ nhiệt Lock&Lock 500ml - Giá: 280,000 VNĐ\n"
                f"3. Máy massage cầm tay mini - Giá: 650,000 VNĐ\n"
                f"4. Voucher Spa thư giãn 90 phút - Giá: 500,000 VNĐ\n"
                f"5. Bộ pha trà hoa cao cấp - Giá: 420,000 VNĐ"
            )

        # ── Mỹ phẩm / Làm đẹp ──
        elif _cat_match(["my pham", "son", "nuoc hoa", "lam dep", "skincare", "beauty"]):
            return (
                f"Danh sách quà [Mỹ phẩm / Làm đẹp] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Set Son môi mini 3 màu cao cấp - Giá: 450,000 VNĐ\n"
                f"2. Nước hoa mini gift set (3 chai x 10ml) - Giá: 680,000 VNĐ\n"
                f"3. Mặt nạ dưỡng da Hàn Quốc (hộp 10 miếng) - Giá: 250,000 VNĐ\n"
                f"4. Set chăm sóc da cơ bản (Toner + Serum) - Giá: 550,000 VNĐ\n"
                f"5. Gương trang điểm có đèn LED - Giá: 320,000 VNĐ"
            )

        # ── Trang sức / Phụ kiện thời trang nữ ──
        elif _cat_match(["trang suc", "vong tay", "day chuyen", "nhan", "jewelry"]):
            return (
                f"Danh sách quà [Trang sức] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Vòng tay bạc khắc tên theo yêu cầu - Giá: 380,000 VNĐ\n"
                f"2. Dây chuyền mặt trái tim bạc 925 - Giá: 520,000 VNĐ\n"
                f"3. Hoa tai ngọc trai nước ngọt - Giá: 450,000 VNĐ\n"
                f"4. Nhẫn đôi couple ring bạc - Giá: 350,000 VNĐ (1 đôi)"
            )

        # ── Handmade / Cá nhân hóa ──
        elif _cat_match(["handmade", "thu cong", "ca nhan hoa", "diy", "tu lam"]):
            return (
                f"Danh sách quà [Handmade / Cá nhân hóa] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Album ảnh scrapbook handmade - Giá: 320,000 VNĐ\n"
                f"2. Vòng tay khắc tên theo yêu cầu - Giá: 250,000 VNĐ\n"
                f"3. Cốc sứ in ảnh cá nhân hóa - Giá: 180,000 VNĐ\n"
                f"4. Hộp nhạc gỗ khắc laser - Giá: 350,000 VNĐ\n"
                f"5. Gấu bông handmade kèm thiệp - Giá: 280,000 VNĐ"
            )

        # ── Thời trang nam / Phụ kiện nam ──
        elif _cat_match(["thoi trang nam", "phu kien nam", "vi da", "that lung", "dong ho nam"]):
            return (
                f"Danh sách quà [Thời trang & Phụ kiện nam] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Ví da bò thật kiểu dáng Nhật Bản - Giá: 450,000 VNĐ\n"
                f"2. Thắt lưng da cao cấp mặt kim loại - Giá: 380,000 VNĐ\n"
                f"3. Đồng hồ thể thao Casio - Giá: 950,000 VNĐ\n"
                f"4. Bộ chăm sóc da nam (Sữa rửa mặt + Kem dưỡng) - Giá: 350,000 VNĐ\n"
                f"5. Áo polo cotton cao cấp - Giá: 420,000 VNĐ"
            )

        # ── Thời trang nữ ──
        elif _cat_match(["thoi trang nu", "tui xach", "khan", "phu kien nu"]):
            return (
                f"Danh sách quà [Thời trang nữ] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Khăn lụa tơ tằm cao cấp - Giá: 480,000 VNĐ\n"
                f"2. Túi xách mini thời trang - Giá: 650,000 VNĐ\n"
                f"3. Kính mát thời trang UV400 - Giá: 350,000 VNĐ\n"
                f"4. Ví cầm tay nữ da thật - Giá: 380,000 VNĐ"
            )

        # ── Trải nghiệm / Voucher ──
        elif _cat_match(["trai nghiem", "voucher", "workshop", "ve", "concert", "an toi"]):
            return (
                f"Danh sách quà [Trải nghiệm / Voucher] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Voucher Workshop vẽ tranh sơn dầu - Giá: 450,000 VNĐ\n"
                f"2. Voucher Spa & Massage thư giãn 90 phút - Giá: 500,000 VNĐ\n"
                f"3. Vé xem phim CGV Combo 2 người - Giá: 250,000 VNĐ\n"
                f"4. Voucher ăn tối nhà hàng Hàn Quốc (2 người) - Giá: 600,000 VNĐ\n"
                f"5. Voucher chụp ảnh studio kỉ niệm - Giá: 800,000 VNĐ"
            )

        # ── Lưu niệm / Kỉ niệm ──
        elif _cat_match(["luu niem", "ki niem", "ky niem", "anh", "khung"]):
            return (
                f"Danh sách quà [Lưu niệm / Kỉ niệm] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Khung ảnh kỉ niệm kèm đèn LED - Giá: 250,000 VNĐ\n"
                f"2. Album ảnh in theo yêu cầu 20 trang - Giá: 350,000 VNĐ\n"
                f"3. Cốc đôi in ảnh couple - Giá: 200,000 VNĐ (1 đôi)\n"
                f"4. Móc khóa mica in ảnh cá nhân - Giá: 80,000 VNĐ"
            )

        # ── Thể thao / Outdoor ──
        elif _cat_match(["the thao", "gym", "chay bo", "outdoor", "fitness"]):
            return (
                f"Danh sách quà [Thể thao / Fitness] trong kho (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Bình nước thể thao Inox 750ml - Giá: 250,000 VNĐ\n"
                f"2. Dây nhảy thể lực cao cấp - Giá: 150,000 VNĐ\n"
                f"3. Đai đeo tay chạy bộ đựng điện thoại - Giá: 180,000 VNĐ\n"
                f"4. Khăn tập gym siêu thấm - Giá: 120,000 VNĐ\n"
                f"5. Tai nghe thể thao chống nước IPX5 - Giá: 650,000 VNĐ"
            )

        # ── Fallback tổng hợp ──
        else:
            return (
                f"Danh sách quà [Tổng hợp] trong kho theo '{category}' (Ngân sách <= {max_budget_val:,} VNĐ):\n"
                f"1. Sách bestseller về phát triển bản thân - Giá: 180,000 VNĐ\n"
                f"2. Khung ảnh kỉ niệm kèm đèn LED - Giá: 250,000 VNĐ\n"
                f"3. Bình giữ nhiệt Lock&Lock 500ml - Giá: 280,000 VNĐ\n"
                f"4. Cốc sứ in ảnh cá nhân hóa - Giá: 180,000 VNĐ"
            )
    except Exception as e:
        return f"LỖI THỰC THI [search_gift_catalog]: {str(e)}"


# ==============================================================================
# 🔧 TOOL 3: check_gift_stock
# ==============================================================================
def check_gift_stock(gift_name: str) -> str:
    """
    Kiểm tra tình trạng tồn kho thực tế và thời gian giao hàng của một món quà cụ thể.

    ── Tool Contract ──
    Name:         check_gift_stock
    Purpose:      Dùng khi đã chọn được món quà cụ thể và cần xác nhận còn hàng trước khi tư vấn.
                  KHÔNG dùng khi chưa biết tên món quà cụ thể.
    Input:        gift_name (str) — Tên chính xác của món quà (Ví dụ: 'Tai nghe Bluetooth Earbuds')
    Output:       Trạng thái ✅ CÒN HÀNG hoặc ❌ HẾT HÀNG kèm thời gian giao
    Error:        Trả chuỗi "LỖI THAM SỐ [...]" nếu tên quà trống
    Side-effect:  Read-only
    Safety:       Toàn bộ logic bọc trong try-except, luôn trả về str
    """
    try:
        if gift_name is None or not isinstance(gift_name, str) or not gift_name.strip():
            return "LỖI THAM SỐ [check_gift_stock]: Tên món quà cần kiểm tra không được để trống."

        name_lower = gift_name.strip().lower()

        # Danh sách các sản phẩm hiện đang hết hàng
        out_of_stock_keywords = ["bàn phím", "đồng hồ casio", "nước hoa mini"]
        if any(k in name_lower for k in out_of_stock_keywords):
            return f"Tình trạng '{gift_name}': ❌ HẾT HÀNG (Dự kiến nhập kho bổ sung sau 7 ngày)."
        else:
            return f"Tình trạng '{gift_name}': ✅ CÒN HÀNG (Sẵn sàng giao ngay trong 24h)."
    except Exception as e:
        return f"LỖI THỰC THI [check_gift_stock]: {str(e)}"


# ==============================================================================
# 📋 TOOL REGISTRY — Đăng ký danh sách tool cho Agent
# ==============================================================================
AVAILABLE_TOOLS: Dict[str, Callable[..., str]] = {
    "analyze_personality": analyze_personality,
    "search_gift_catalog": search_gift_catalog,
    "check_gift_stock": check_gift_stock,
}


# ==============================================================================
# 🛡️ SAFE EXECUTION WRAPPER — Thực thi tool an toàn cho Role 4
# ==============================================================================
def execute_tool_safely(tool_name: str, *args, **kwargs) -> str:
    """
    Thực thi tool theo tên chuỗi với bảo vệ an toàn tuyệt đối.
    Trả về chuỗi kết quả (Observation) hoặc chuỗi thông báo lỗi — không bao giờ crash.

    Args:
        tool_name (str): Tên tool cần thực thi
        *args, **kwargs: Tham số truyền vào tool

    Returns:
        str: Kết quả Observation hoặc thông báo lỗi an toàn
    """
    try:
        # Failure Mode: Unknown Tool
        if tool_name not in AVAILABLE_TOOLS:
            valid_tools = ", ".join(AVAILABLE_TOOLS.keys())
            return (
                f"LỖI HỆ THỐNG: Công cụ '{tool_name}' không tồn tại. "
                f"Các công cụ hợp lệ gồm: [{valid_tools}]"
            )

        tool_func = AVAILABLE_TOOLS[tool_name]
        return tool_func(*args, **kwargs)
    except TypeError as e:
        # Failure Mode: Malformed Args (sai số lượng hoặc kiểu tham số)
        return f"LỖI THAM SỐ [{tool_name}]: Sai cú pháp hoặc số lượng tham số - {str(e)}"
    except Exception as e:
        return f"LỖI THỰC THI AN TOÀN [{tool_name}]: {str(e)}"


# ==============================================================================
# 📄 TOOL SPECS EXTRACTOR — Trích xuất mô tả tool cho Prompt & Báo cáo
# ==============================================================================
def get_tool_specs() -> str:
    """
    Trích xuất toàn bộ Tool Specifications dạng văn bản từ docstrings.
    Hỗ trợ Role 3 & Role 4 khi cần inject mô tả tool vào prompt hoặc báo cáo.
    """
    specs = []
    for name, func in AVAILABLE_TOOLS.items():
        doc = func.__doc__.strip() if func.__doc__ else "Không có mô tả"
        first_line = doc.splitlines()[0]
        specs.append(f"- {name}: {first_line}")
    return "\n".join(specs)
