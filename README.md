# 🧠 Zuse Coder AI v2.0 - Hệ Thống Multi-Agent Đỉnh Cao

> Không chỉ là một con AI bình thường, Zuse là một **Hệ điều hành AI thu nhỏ** dành riêng cho Termux. Với giao diện TUI chuyên nghiệp, hệ thống plugin, và khả năng tự động viết code - chạy test - sửa lỗi cực mạnh mẽ.

![Version](https://img.shields.io/badge/Version-2.0.0-blueviolet?style=for-the-badge)
![Termux](https://img.shields.io/badge/Termux-Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

## 🚀 Tính năng "Khét Lẹt"
- **Giao diện Panel (TUI):** Chia khung rõ ràng, màu sắc Neon rực rỡ.
- **Hệ thống Slash Commands:** Điều khiển AI bằng các lệnh như `/help`, `/clear`, `/exec`, `/skill`.
- **Kiến trúc Đa tác vụ:** Tách biệt Bộ não (Core), Công cụ (Tools) và Kỹ năng (Skills).
- **Auto-Fix Vòng lặp:** Tự chạy code, đọc lỗi, sửa và chạy lại đến khi thành công.
- **Hệ thống Skill:** Dạy AI các kỹ năng mới thông qua file markdown trong thư mục `skills/`.

## ⚡ Hướng Dẫn Cài Đặt

**Bước 1: Cài đặt môi trường**
pkg update -y
pkg install python git curl jq -y
pip install requests rich

**Bước 2: Tải tool**
git clone https://github.com/MD03-dev/zuse-coder-ai.git
cd zuse-coder-ai
chmod +x zuse.py

**Bước 3: Lấy API Key và chạy**
export AI_API_KEY="key_cua_ban"
python zuse.py
