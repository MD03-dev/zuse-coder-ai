# 🧠 Zuse Coder AI v4.0 - Hệ Thống Multi-Agent Đỉnh Cao

> Trợ lý lập trình AI tự trị trên Termux. Hỗ trợ chuyển đổi linh hoạt giữa các model của Groq (Llama 3, Qwen, GPT-OSS...) ngay trên Terminal.

![Version](https://img.shields.io/badge/Version-4.0.0-blueviolet?style=for-the-badge)
![Termux](https://img.shields.io/badge/Termux-Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

## 🚀 Tính năng mới (v4.0)
- **Chuyển đổi Model linh hoạt:** Gõ lệnh `/model` để xem danh sách và đổi sang các model mạnh hơn (như `llama-3.3-70b-versatile` hay `openai/gpt-oss-120b`) khi cần.
- **Xóa log thông minh:** Màn hình tự động clear mỗi khi mở tool hoặc gõ `/help`.
- **Giao diện TUI Chuyên Nghiệp:** Khung Panel Neon rực rỡ.
- **Hệ thống Slash Commands:** Hơn 15 lệnh điều khiển hệ thống.

## ⚡ Hướng Dẫn Cài Đặt

**Bước 1: Cài đặt môi trường**
pkg update -y
pkg install python git curl jq -y
pip install requests rich

**Bước 2: Tải tool**
git clone https://github.com/MD03-dev/zuse-coder-ai.git
cd zuse-coder-ai
chmod +x zuse.py

**Bước 3: Lấy API Key miễn phí**
Truy cập https://console.groq.com, đăng nhập và tạo API Key.

**Bước 4: Cấu hình và sử dụng**
export AI_API_KEY="key_cua_ban"
python zuse.py

## 💡 Danh sách Model hỗ trợ (Gõ /model để đổi)
- `llama-3.1-8b-instant`: Siêu nhanh, ít tốn token.
- `llama-3.3-70b-versatile`: Thông minh nhất, viết code cực đỉnh.
- `qwen/qwen3.8-27b`: Cân bằng, tốt cho tiếng Việt.
- `openai/gpt-oss-120b`: Model suy luận mạnh mẽ.

## 🤝 Đóng góp
Đừng quên thả 1 Star ⭐ nếu bạn thấy tool hữu ích!
