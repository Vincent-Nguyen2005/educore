# Giai đoạn 5 — Slide outline và chuẩn bị vấn đáp (M5, tuần 15)

## Outline 10 slide

1. Bài toán, stakeholders, 5 ASR.
2. Định lượng burst: 8.000/60 ≈ 134/s, mục tiêu p95 <1s.
3. Tenant variation: công thức, quy chế thi, SSO, plugin; bổ sung kết quả phỏng vấn thật.
4. So sánh 3 mô hình tenancy và ADR-001.
5. Context + trust boundaries.
6. Container + component + deployment; đường nộp bài.
7. Plugin contract và grade formula versioning.
8. ATAM: R1–R4, thay đổi v1→v2.
9. Demo và kết quả test thật; ghi rõ phần chưa kiểm chứng.
10. Bài học, rủi ro còn lại và quyết định cần xác nhận.

## Phân công trình bày đề xuất, cần nhóm xác nhận

Huy: drivers; Kazan: ADR/views; Khanh: prototype; Tâm: test/ATAM. Mỗi người cần trả lời chéo ít nhất một phần không phụ trách.

## 10 câu vấn đáp để tự luyện

1. Query thiếu `tenant_id` sẽ đi tới đâu trong v2? Tài khoản DB tenant A đọc DB B được không?
2. Vì sao không chọn shared schema + RLS dù rẻ hơn?
3. Receipt 202 có nghĩa gì? Nếu API restart ngay sau đó, bài ở đâu?
4. Nếu worker chậm 10 phút, sinh viên thấy trạng thái gì?
5. Idempotency key của autosave xử lý request đảo thứ tự ra sao?
6. Plugin QR treo 30 giây có ảnh hưởng tới nộp bài không?
7. Công thức điểm thay giữa kỳ có sửa điểm cũ tự động không? Vì sao?
8. Pre-scale dựa trên lịch thi bị sai thì fallback nào?
9. Kết quả load test laptop có thể khẳng định SLA cloud không?
10. Nếu tải tăng 10 lần, bottleneck đầu tiên là gì, cần đo nào trước khi tách service?

Mỗi người trả lời bằng cách chỉ vào ADR, view, code hoặc số đo; không học thuộc câu trả lời AI. Ghi ngày và người tham gia buổi luyện thật sau khi hoàn thành.
