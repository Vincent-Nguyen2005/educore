# 07 – Assumptions

## Mười câu hỏi làm rõ (kiến trúc sư → khách hàng)
1. Mức cô lập tối thiểu: logical (shared schema), schema-per-tenant hay bắt buộc database-per-tenant? Có tenant nào cần vật lý riêng?
2. Yêu cầu data residency theo quốc gia/vùng?
3. Cửa sổ thi có biết trước lịch không → pre-scale hay autoscale mù?
4. Autosave granularity bao nhiêu giây? Client có buffer local (offline-first) không?
5. SSO mỗi tenant dùng SAML 2.0, OIDC hay cả hai? IdP do trường sở hữu?
6. Plugin có cần sandbox cách ly không, hay tin tưởng chạy trong process core?
7. Công thức điểm có cần versioning và recompute lịch sử không?
8. Plagiarism check là blocking hay async?
9. SaaS owner có cần cross-tenant analytics ẩn danh không?
10. Mức tuân thủ pháp lý (audit log, quy chế thi, lưu bao lâu)?

## Assumptions

| # | Giả định | Ảnh hưởng kiến trúc |
|---|---|---|
| A1 | Giả định M1 ban đầu là shared schema + RLS; Architecture v2 đề xuất DB-per-tenant trên shared cluster để giảm risk S4. Cần nhóm xác nhận ADR-001. | ADR multi-tenancy, cost |
| A2 | Lịch thi biết trước ≥ 1 tuần → pre-scale + warm pool | Chiến lược burst |
| A3 | Plagiarism check là async (có SLA riêng) | Tách submission path khỏi external call |
| A4 | Client web có IndexedDB/LocalStorage để buffer autosave | Reliability khi mất mạng |
| A5 | Core chạy trên Kubernetes, autoscale được | Prototype load test |
| A6 | Không yêu cầu offline exam hoàn toàn (chỉ buffer khi mạng chập chờn) | Giảm phức tạp sync đa chiều |
| A7 | SSO chuẩn SAML 2.0 / OIDC, IdP do trường | Chốt tech stack auth |

## Khác biệt giữa các tenant (cơ sở xác định variation point)

Hướng dẫn yêu cầu phỏng vấn ≥ 2 giảng viên/cán bộ đào tạo. Cột "Giả thuyết" là của nhóm; cột "Kết quả phỏng vấn" phải điền bằng dữ liệu thật.

| Nội dung | Giống nhau (core) | Khác nhau (variation point) | Kết quả phỏng vấn |
|---|---|---|---|
| Công thức điểm | Có điểm thành phần, điểm tổng kết | Trọng số, số cột điểm, làm tròn, điều kiện đạt | _(điền)_ |
| Quy chế thi | Thi hẹn giờ, có nộp bài | Thời lượng, xem lại câu, xáo trộn đề | _(điền)_ |
| Đăng nhập | Có SSO | Giao thức, IdP, ánh xạ thuộc tính | _(điền)_ |
| Tiện ích | Quản lý khóa học, tài liệu | Plugin bật/tắt theo tenant | _(điền)_ |
