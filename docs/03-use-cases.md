# 03 – Use Cases

| # | Use case | Actor chính | Ghi chú kiến trúc |
|---|---|---|---|
| UC1 | Đăng ký tenant, cấu hình công thức điểm | Tenant admin | Tenant bootstrap |
| UC2 | SSO vào trường qua IdP | SV / GV | SAML/OIDC per tenant |
| UC3 | Tạo khóa học, upload tài liệu & video | Giảng viên | Object storage |
| UC4 | Nộp bài tập + async plagiarism check | Sinh viên | External call async |
| UC5 | Tạo bài thi trắc nghiệm hẹn giờ | Giảng viên | Exam scheduling |
| UC6 | Làm bài + autosave định kỳ | Sinh viên | Reliability path |
| UC7 | Nộp bài 1 phút cuối | Sinh viên | Burst path – ASR-1 |
| UC8 | Tự động chấm trắc nghiệm | Hệ thống | Async batch |
| UC9 | Xem bảng điểm theo công thức tenant | GV / Phòng ĐT | Extensibility |
| UC10 | Cài plugin mới (QR attendance) cho 1 tenant | Tenant admin | Hot install 0 downtime |
| UC11 | Cảnh báo SV nguy cơ rớt môn | Phòng ĐT | Reporting/batch |
| UC12 | Báo cáo cross-tenant ẩn danh | SaaS owner | Aggregate, no PII |

## Use case bổ sung sau rà soát

| # | Use case | Quyết định |
|---|---|---|
| UC13 | Data export / offboarding khi tenant rời đi | **Giữ** – liên quan isolation/security |
| UC14 | Audit truy cập dữ liệu SV | **Giữ** – ràng buộc pháp lý |
| UC15 | Thu hồi / khoá tenant | **Backlog** – ngoài phạm vi M1–M3 |

## Ánh xạ use case → ASR
- UC7 → ASR-1 · UC6 → ASR-2 · UC2, UC13, UC14 → ASR-3
- UC10 → ASR-4 · UC1, UC9 → ASR-5
