# 🧠 Zuse Coder AI v6.9.7 - Trợ Lý Lập Trình Đa Tác Vụ

> Biến Termux thành môi trường lập trình tự động. Tự viết code, tự test, tự sửa lỗi với giao diện TUI Neon cực chất. Không cần root!

![Version](https://img.shields.io/badge/Version-6.9.7-blueviolet?style=for-the-badge)
![Termux](https://img.shields.io/badge/Termux-Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

## 🚀 Tính năng "Khét Lẹt"
- **Đa tác vụ (Multi-Agent):** Tách biệt bộ não (Core), công cụ (Tools) và kỹ năng (Skills).
- **Đổi Model & Ngôn ngữ:** Tùy biến linh hoạt qua lệnh /model và /lang.
- **Tối ưu Token:** Cắt tỉa lịch sử chat tự động, giảm thiểu lỗi Rate Limit.
- **Giao diện TUI:** Màn hình Neon, bảng lệnh trực quan, tự động xóa log.

## ⚡ Hướng Dẫn Cài Đặt

**Bước 1: Cài đặt môi trường**
pkg update -y
pkg install python git curl jq -y
pip install requests rich

**Bước 2: Tải tool và chạy**
git clone https://github.com/MD03-dev/zuse-coder-ai.git
cd zuse-coder-ai
chmod +x zuse.py
export AI_API_KEY="key_groq_cua_ban"
python zuse.py
