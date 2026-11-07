# Giai đoạn 3 — ATAM rút gọn và Architecture v2 (M3, tuần 11)

## Bước 11: 3 ASR ưu tiên

| ASR | Phân tích response | Sensitivity point | Trade-off point | Risk / non-risk |
|---|---|---|---|---|
| S1: 8K/min, p95 <1s | Receipt chỉ trả sau ghi bền; worker chấm sau. Tải trung bình 134/s, phải test burst sát cuối phút và autosave nền. | Số API replica, pool DB, độ dài payload, số IOPS durable store. | Batch/queue giảm p95 nhưng tăng độ trễ thấy điểm và chi phí. | R1: ack trước commit làm mất bài. Non-risk: chấm điểm async không nằm trên critical path. |
| S4: query thiếu tenant | V1 shared schema + RLS phụ thuộc policy, session context và role chính xác. | DB role có BYPASSRLS hay không, `FORCE ROW LEVEL SECURITY`, connection pool reset. | DB riêng tăng isolation nhưng tăng số migration/connection. | R2: session tenant context rò giữa request; R3: cấu hình RLS thiếu trên một bảng. |
| S2: mất mạng/restart | IndexedDB lưu local trước khi POST, sequence và retry; API stateless. | Tần suất local save, retention, độ bền local và idempotency. | Save thường xuyên tăng tải/chi phí; save thưa tăng mất dữ liệu. | R4: trình duyệt cấm/quota IndexedDB. Non-risk: restart API sau ack không xóa DB commit. |

Các câu hỏi đánh giá cần chạy: Khi queue đầy có trả 503 và giữ local receipt không? Khi token tenant A gửi ID tenant B, DB role nào thực thi? Khi browser offline 60s, local edits được gửi theo thứ tự nào? Khi một plugin treo, timeout có chặn submission không?

## Bước 12: Thay đổi v1 → v2

| Risk | V1 | V2 | Cách xác minh |
|---|---|---|---|
| R1 ack trước durable | Queue có thể là memory | Receipt transaction commit trên DB tenant trước HTTP 202; worker tiêu thụ sau | Restart API rồi GET receipt; test fault injection |
| R2/R3 lỗi RLS/session | Shared schema + RLS | DB-per-tenant; app role chỉ có quyền vào DB của tenant đó, không thể mở DB khác; token/host match | Test token A gọi object B; kiểm tra privilege/connection config |
| R4 offline/quota | Autosave định kỳ | IndexedDB trước khi báo “đã lưu”, cảnh báo khi storage failed; retry idempotent | Browser offline test thủ công cần thực hiện |

**Điểm còn mở:** Không có biên bản peer review thực tế. Cần trình bày v2 cho một nhóm khác và ghi người tham gia, ngày, phản hồi, thay đổi vào bảng dưới. Không được điền thay bằng phản hồi AI.

| Ngày | Nhóm phản biện | Nhận xét nguyên văn/tóm tắt có xác nhận | Quyết định xử lý |
|---|---|---|---|
| Chờ thực hiện | Chờ thực hiện | Chờ thực hiện | Chờ thực hiện |
