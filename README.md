# Google Form Auto Filler

## Mô tả
**Google Form Auto Filler** là một công cụ tự động điền biểu mẫu Google Form dựa trên các thông tin được cung cấp sẵn. Công cụ giúp tiết kiệm thời gian và công sức khi làm việc với các biểu mẫu trực tuyến.

## Tính năng
- Tự động điền các trường trong Google Form.
- Hỗ trợ các trường văn bản, danh sách lựa chọn, checkbox, v.v.
- Tùy chỉnh linh hoạt để đáp ứng các biểu mẫu khác nhau.

## Cài đặt

### 1. Yêu cầu hệ thống
- **Python** >= 3.7
- Các thư viện Python cần thiết (được liệt kê bên dưới).

### 2. Cài đặt các thư viện cần thiết
Trước khi sử dụng, bạn cần cài đặt các thư viện cần thiết. Chạy lệnh sau trong terminal:

```bash
pip install pyqt6
pip install selenium
```

### 3. Cài đặt ChromeDriver
- Để cài đặt ChromeDriver, truy cập: https://chromedriver.chromium.org/downloads.
- Cài đặt phiên bản ChromeDriver tương thích với trình duyệt
- Chuyển tệp chromedriver.exe vào thư mục data

## Hướng dẫn sử dụng

- Để chạy chương trình:
```bash
python auto_filler.py
```

- Điền URL của mẫu, số lượng và các lựa chọn khác
- Nhấn **Bắt đầu** để khởi động và **Dừng** khi cần thiết hoặc gặp lỗi
