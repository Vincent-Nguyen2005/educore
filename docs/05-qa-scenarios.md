# 05 – Quality Attribute Scenarios

10 scenario, phủ 7 QA, gồm đủ 5 scenario bắt buộc (a)–(e) của đề tài 4.

| # | QA | Source → Stimulus | Artifact | Environment | Response | Response measure | Đề bắt buộc |
|---|---|---|---|---|---|---|---|
| S1 | Performance | 8K SV nộp bài phút cuối | Submission service + DB | Exam window biết trước | Nhận, lưu bền, trả receipt | p95 < 1s, lỗi < 0,1%, 0 bài mất | (a) |
| S2 | Reliability | Mất mạng 60s khi thi | Exam client + autosave API | Trong giờ thi | Client buffer + gửi lại idempotent | Mất ≤ 30s thao tác, 0 autosave mất | |
| S3 | Reliability | Instance restart giữa giờ thi | Toàn hệ thống | Active exam | Failover + reconnect + khôi phục autosave (state = các câu đã autosave) | Gián đoạn < 30s/client | (b) |
| S4 | Security/MT | Truy cập chéo tenant, kể cả khi query thiếu điều kiện tenant | API gateway + DB | Bất kỳ | Từ chối 100%, audit log, cảnh báo SOC | 0 rò rỉ, cảnh báo < 5 phút | (c) |
| S5 | Extensibility | Tenant admin bật plugin QR | Plugin runtime + core | Production, 0 downtime | Tải và kích hoạt lúc runtime | Core 0 downtime, plugin < 5 phút, tenant khác không bị ảnh hưởng | |
| S6 | Extensibility | Trường mới cấu hình công thức 10% chuyên cần + 30% giữa kỳ + 60% cuối kỳ (hoặc đổi công thức giữa kỳ) | Grading service | Bất kỳ | Áp dụng bằng cấu hình, không deploy core, giữ version cũ | Không redeploy core; tính lại 10K bài < 5 phút; 100% khớp kết quả tính tay | (d) |
| S7 | Cost | Thêm tenant nhỏ 10K user | Hạ tầng | Baseline 10K user | Dùng chung tài nguyên | Chi phí tăng ≤ 5% so với baseline 10K user | |
| S8 | Availability | Lưu lượng thường + đợt thi burst | Toàn hệ thống | Trong học kỳ | Đạt SLO | 99,9% tháng / 99,95% exam window | |
| S9 | Usability | Sinh viên gõ bài | Exam UI | Trong giờ thi | Lưu nền mỗi 5s | Mất ≤ 5s nếu trình duyệt crash | |
| S10 | Operability | Trường mới ký hợp đồng | Tenant bootstrap | Production | Tạo tenant, SSO, công thức điểm, dữ liệu mẫu bằng cấu hình/script | Go-live kỹ thuật ≤ 1 ngày, 0 dòng code core phải sửa | (e) |

## Nguồn con số
- S1 (p95 < 1s, 8K) và S2 (30s) lấy trực tiếp từ đề tài; "1 ngày" ở S10 từ yêu cầu bắt buộc (e) của hướng dẫn.
- S3, S5, S6, S7, S9 là mục tiêu nội bộ do nhóm đặt, cần xác thực qua prototype ở M4.

## Cách kiểm chứng trong prototype
Số liệu phải là số đo thật, kèm mô tả môi trường và cách tái hiện.
- **S1**: k6/Locust bắn 8K request/phút vào endpoint nộp bài, đo p95 và tỉ lệ lỗi.
- **S2**: Chrome DevTools "Offline" 60s rồi online lại; đối chiếu số câu nhập với số câu server nhận.
- **S3**: dừng/khởi động lại một container giữa lúc load test.
- **S4**: token tenant A gọi ID tenant B → assert 403/404 + có audit log; thêm test cố ý bỏ điều kiện tenant ở query.
- **S5**: bật plugin cho tenant A khi hệ thống đang chạy; tenant B không thấy, core không restart.
- **S6**: cấu hình công thức 10/30/60, chạy job tính lại, đo thời gian, so với kết quả tính tay.
- **S10**: chạy script tạo tenant từ đầu, bấm giờ đến khi đăng nhập SSO và xem được bảng điểm.
