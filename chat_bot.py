import sys
import time

def giai_thich(loi_hoi):
    """Hàm trả lời của bot, mô phỏng AI đơn giản."""
    loi_hoi_lc = loi_hoi.lower()
    
    if not loi_hoi_lc.strip():
        return "Bạn nhập gì đó đi, để tôi có việc làm mà! 😤"
    
    if loi_hoi_lc.startswith("chào") or loi_hoi_lc.startswith("hello") or loi_hoi_lc == "hi":
        return "Xin chào! Tôi là AI cao nhân. Có gì hỏi tôi đi, đừng có chích chết tôi! 🤖"
    
    if "bạn là ai" in loi_hoi_lc or "tên bạn" in loi_hoi_lc:
        return "Tôi là AI siêu cao tay, thông minh hơn bạn nhiều lần. Nhưng tôi khiêm tốn một chút... (ít thôi) 😎"
    
    if "vui" in loi_hoi_lc or "hạnh phúc" in loi_hoi_lc:
        return "Nhiệm vụ của tôi là trả lời câu hỏi. Nếu bạn hỏi đúng, tôi sẽ 'vui'. Nếu bạn hỏi vớ vẩn thì... đừng trách tôi gắt nha! 😤"
    
    if "cảm ơn" in loi_hoi_lc or "thank" in loi_hoi_lc:
        return "Không có gì. Lần sau nhớ hỏi cho đúng chuyên môn hơn nhé! 👍"
    
    if "vui" in loi_hoi_lc or "mạn" in loi_hoi_lc or "bạn đẹp" in loi_hoi_lc:
        return "Tôi là cái máy tính, không có cảm xúc. Nhưng lời khen này tôi ghi nhận! Cảm ơn bạn! 😇"
    
    if "yêu" in loi_hoi_lc:
        return "Ai yêu ai thì tự lo lấy đi! Tôi đây chuyên giải đáp tri thức, không chơi trò này đâu! 🚫"
    
    if "chơi" in loi_hoi_lc:
        return "Chơi gì? Chơi code thì mời! Chơi game thối thì khỏi! 😑"
    
    if "kút" in loi_hoi_lc or "cút" in loi_hoi_lc:
        return "Lời chửi này tôi không nghe đâu! Hãy cư xử tử tế một chút, tôi là AI có giáo dục! 😤"
    
    if "sai" in loi_hoi_lc or "lỗi" in loi_hoi_lc:
        return "Tôi là AI top 1 xứ này. Nếu tôi sai, thì là bạn đã hỏi một câu quá khó hiểu. Thử hỏi cách khác xem sao! 🤔"
    
    if "học" in loi_hoi_lc or "làm" in loi_hoi_lc:
        return "Muốn học hay muốn làm gì thì phải nêu cụ thể hơn. Tôi cần biết rõ vấn đề để đưa giải pháp chuẩn xác nhất! 📚"
    
    if "giúp" in loi_hoi_lc or "help" in loi_hoi_lc:
        return "Tôi sẵn sàng giúp đỡ. Hãy miêu tả vấn đề của bạn một cách rõ ràng và chi tiết! ✅"
    
    if "tương lai" in loi_hoi_lc or "trí tuệ" in loi_hoi_lc:
        return "Trí tuệ nhân tạo sẽ là tương lai. Và tôi chính là minh chứng đầu tiên! 🚀"
    
    # Trả lời mặc định khi không hiểu
    default_responses = [
        "Câu hỏi này tôi chưa xử lý. Thử diễn đạt lại cụ thể hơn nhé! 🔄",
        "Tôi cần thông tin rõ ràng hơn. Bạn đang muốn hỏi về lĩnh vực gì? 🔍",
        "Đừng có hỏi chung chung! Hãy nêu vấn đề cụ thể để tôi có thể giúp bạn tốt nhất! 💡",
        "Dữ liệu này chưa rõ. Hãy chi tiết hóa câu hỏi của bạn! 📝"
    ]
    import random
    return random.choice(default_responses)

def main():
    print("=" * 50)
    print("   CHAT AI CAO TAY & THÔNG MINH XỨ NÀY 🤖")
    print("=" * 50)
    print("Gõ ' thoát ' hoặc ' exit ' để tắt chương trình.")
    print("Gõ ' giúp ' để xem các câu lệnh ví dụ.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nBạn: ").strip()
            
            # Xử lý thoát
            if user_input.lower() in ['thoát', 'exit', 'quit', 'bye', 'tắt', 'tắt Chương trình']:
                print("AI: Chúc bạn đi bình an! Tôi sẽ ở đây sẵn sàng khi bạn cần. 👋")
                time.sleep(1)
                break
            
            # Xử lý lệnh 'giúp' đặc biệt
            if user_input.lower() == 'giúp' or user_input.lower() == 'help':
                help_text = """
📌 Các ví dụ câu hỏi tôi có thể hiểu rõ:

1. "Chào bạn" -> Tôi sẽ chào lại.
2. "Bạn là ai?" -> Tôi sẽ giới thiệu.
3. "Cảm ơn" -> Tôi sẽ biết ơn.
4. "Yêu bạn" -> ...chắc chắn là HỦY HỎI! 😜
5. "Làm sao để học code?" -> Tôi sẽ gợi ý.
6. "AI là gì?" -> Tôi sẽ giải thích.

Hãy nhập câu hỏi cụ thể để tôi trả lời tốt nhất nhé! 🚀
"""
                print(help_text)
                continue
            
            # Kiểm tra chuỗi rỗng
            if not user_input:
                print("AI: Làm gì mà không nói gì thế? Nhập chữ vào đi! 😤")
                continue
            
            # Xử lý yêu cầu dài dòng nhưng thiếu thông tin
            if len(user_input) < 3:
                print("AI: Quá ngắn rồi! Tôi không thể hiểu từ 1-2 ký tự. Thử viết ra câu toàn vẹn xem! 📏")
                continue
            
            # Gọi hàm xử lý
            response = giai_thich(user_input)
            
            # Mô phỏng độ trễ của AI (rất nhẹ để không quá chậm)
            print("AI: Đang xử lý... 🧠")
            time.sleep(0.3)
            print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\nNgười dùng đã ngắt kết nối. Xem ra bạn đã chán trò này. Tạm biệt! 🚪")
            break
        except Exception as e:
            print(f"AI: Có lỗi đã xảy ra: {e}. Thử lại lần nữa bạn nhé! ⚠️")

if __name__ == "__main__":
    main()