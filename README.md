# End-to-End Secure Text Chat v2 (Phiên bản Web)

## FIT4012 – Nhập môn An toàn Bảo mật Thông tin

---

# Thông tin sinh viên

**Nhóm 2**

**Họ và tên sinh viên:**

- Trần Đình Khiêm
- La Văn Hải
- Lương Như Ý
- Trương Văn Ban

---

# Tổng quan dự án

End-to-End Secure Text Chat v2 là một ứng dụng trò chuyện thời gian thực trên nền tảng web được phát triển làm bài tập lớn môn **Nhập môn An toàn Bảo mật Thông tin**.

Hệ thống minh họa cách các kỹ thuật mật mã hiện đại được tích hợp vào một ứng dụng nhắn tin nhằm cung cấp:

- Tính bí mật (Confidentiality)
- Tính toàn vẹn (Integrity)
- Tính xác thực (Authentication)
- Chống tấn công phát lại (Replay Attack Protection)
- Quản lý khóa phiên an toàn (Secure Session Key Management)

Không giống như các ứng dụng trò chuyện thông thường, mọi tin nhắn được trao đổi giữa các người dùng đều được bảo vệ bằng **mã hóa có xác thực** và **chữ ký số** trước khi truyền qua mạng.

Dự án cũng bao gồm giao diện web trực quan cho phép người dùng mô phỏng các cuộc tấn công phổ biến nhằm minh họa cách các cơ chế bảo mật được triển khai để bảo vệ hệ thống.

---

# Các chức năng chính

## Xác thực người dùng

- Đăng ký tài khoản
- Đăng nhập
- Băm mật khẩu trước khi lưu trữ
- Quản lý người dùng đang trực tuyến

---

## Giao tiếp an toàn

Mỗi phiên trò chuyện bao gồm:

- Trao đổi khóa phiên bằng RSA-OAEP
- Mã hóa xác thực bằng AES-GCM
- Chữ ký số RSA
- Xác thực thông điệp
- Kiểm tra tính toàn vẹn của dữ liệu

---

## Gói tin nhắn an toàn

Mỗi tin nhắn được truyền đi bao gồm:

- Message ID
- Session ID
- Sequence Number
- Timestamp
- Nonce
- Ciphertext
- Digital Signature

Các trường dữ liệu này được sử dụng để phát hiện tấn công phát lại và xác minh tính toàn vẹn của quá trình truyền thông.

---

## Chống tấn công Replay

Hệ thống ngăn chặn tấn công phát lại bằng cách sử dụng:

- Message ID duy nhất
- Kiểm tra Sequence Number
- Replay Detector
- Đăng ký các gói tin đã xử lý

Nếu kẻ tấn công gửi lại một gói tin cũ, hệ thống sẽ phát hiện và từ chối ngay lập tức.

---

## Thay đổi khóa phiên (Session Key Rotation)

Để giảm nguy cơ lộ khóa trong thời gian dài, ứng dụng sẽ tự động thay đổi khóa phiên AES sau mỗi năm tin nhắn được gửi thành công.

### Lợi ích:

- Mô phỏng Perfect Forward Secrecy
- Giảm thiểu tác động nếu một khóa phiên bị lộ
- Minh họa vòng đời quản lý khóa phiên an toàn

---

# Minh họa các cơ chế bảo mật

Giao diện web cung cấp nhiều chế độ mô phỏng tấn công.

---

## Valid Message

Trao đổi tin nhắn mã hóa bình thường.

**Kết quả mong đợi:**

VALID

---

## Replay Attack

Gửi lại một gói tin đã được xử lý trước đó.

**Kết quả mong đợi:**

REPLAY ATTACK DETECTED


## Modify Ciphertext

Thay đổi ngẫu nhiên nội dung Ciphertext.

**Kết quả mong đợi:**

INVALID SIGNATURE

hoặc

DECRYPTION FAILED

---

## Modify Sequence Number

Thay đổi Sequence Number của gói tin.

**Kết quả mong đợi:**

INVALID SEQUENCE

---

## Wrong Session Key

Giải mã bằng khóa AES phiên không đúng.

**Kết quả mong đợi:**

DECRYPTION FAILED

---

## Fake Sender

Giả mạo danh tính người gửi.

**Kết quả mong đợi:**

INVALID SIGNATURE

---

# Công nghệ bảo mật sử dụng

| Thành phần | Thuật toán |
|------------|------------|
| Mã hóa đối xứng | AES-GCM |
| Trao đổi khóa phiên | RSA-OAEP |
| Chữ ký số | RSA |
| Hàm băm | SHA-256 |
| Chống Replay | Message ID + Sequence Number |
| Quản lý phiên | Automatic Key Rotation |

---

# Kiến trúc dự án

Browser A
    │
    │
 Socket.IO
    │
    ▼
Flask Web Server
    │
    │
Socket Handler
    │
 ├───────────────┐
 │               │
 ▼               ▼
Session Manager  Replay Detector
 │               │
 ▼               ▼
Chat Engine   Packet Validation
 │
 ▼
AES-GCM Encryption
 │
 ▼
RSA Signature
 │
 ▼
Browser B

---

# Cấu trúc dự án

FIT4012-Secure-Chat
│
├── client/
├── crypto/
│   ├── aes_gcm.py
│   ├── rsa_encrypt.py
│   ├── rsa_signature.py
│   ├── rsa_key.py
│   └── key_exchange.py
│
├── protocol/
│   ├── packet.py
│   ├── session.py
│   └── message_processor.py
│
├── replay/
│   └── replay_detector.py
│
├── server/
│   └── session_manager.py
│
├── web/
│   ├── app.py
│   ├── websocket/
│   ├── security/
│   ├── auth/
│   ├── templates/
│   └── static/
│
├── tests/
├── docs/
├── diagram/
├── benchmark/
├── logs/
├── demo/
└── README.md

---

# Cài đặt

Clone repository:

bash
git clone
cd FIT4012-Secure-Chat


Cài đặt thư viện:

bash
pip install -r requirements.txt

---

# Chạy chương trình

Khởi động Flask Server:
bash
python web/app.py

hoặc
bash
flask run

Mở trình duyệt:
http://127.0.0.1:5000


---

# Hướng dẫn sử dụng

- Đăng ký hai tài khoản.
- Đăng nhập.
- Mở cửa sổ trò chuyện.
- Chọn một người dùng đang trực tuyến.
- Gửi tin nhắn đã được mã hóa.
- Quan sát bảng **Security Information**.
- Bật các chế độ mô phỏng tấn công để kiểm tra các cơ chế bảo vệ.

---

# Bảng Security Information

Đối với mỗi tin nhắn, hệ thống hiển thị:

- Plaintext
- AES Ciphertext
- Nonce
- RSA Signature
- Session ID
- Sequence Number
- Message ID
- Timestamp
- Security Status

Điều này cho phép người dùng quan sát cách từng cơ chế bảo mật hoạt động theo thời gian thực.

---

# Kiểm thử

Dự án bao gồm các bài kiểm thử bảo mật cho:

- Valid Message
- Replay Attack
- Modify Ciphertext
- Modify Sequence Number
- Wrong Session Key
- Fake Sender
- Session Key Rotation

Ảnh chụp màn hình và kết quả được lưu tại:

test_report/

---

# Tài liệu

Dự án bao gồm các tài liệu:

- Protocol Design
- Threat Model
- Test Report
- Benchmark Report
- Sequence Diagrams

Được lưu tại:

docs/
diagram/
benchmark/
test_report/

---

# Mục đích giáo dục

Dự án được phát triển hoàn toàn cho mục đích học tập trong khuôn khổ môn học **FIT4012 – Nhập môn An toàn Bảo mật Thông tin**.

Các chế độ mô phỏng tấn công được xây dựng nhằm minh họa cách các giao thức truyền thông an toàn chống lại các hình thức tấn công phổ biến và không được sử dụng cho bất kỳ mục đích xấu nào.

---

# Hướng phát triển

Các hướng phát triển trong tương lai bao gồm:

- Perfect Forward Secrecy sử dụng ECDH (X25519)
- Trò chuyện nhóm nhiều người
- Quản lý khóa trên nền tảng đám mây
- Băm mật khẩu bằng Argon2 hoặc bcrypt
- Quản lý người dùng bằng cơ sở dữ liệu
- Triển khai TLS
- Hỗ trợ ứng dụng di động

---

# Tác giả

**Trần Khiêm**

FIT4012 – Nhập môn An toàn Bảo mật Thông tin

**End-to-End Secure Text Chat v2**