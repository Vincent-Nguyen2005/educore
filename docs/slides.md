---
marp: true
theme: default
paginate: true
---

# EduCore
## Kiến trúc LMS SaaS đa trường — SE 403, đề tài 4

M1 → M5 · Architecture v2 · 07/11/2026

---

# 1. Bài toán và ASR

- Mỗi tenant 10.000–40.000 sinh viên, công thức điểm và quy chế riêng.
- 8.000 sinh viên nộp bài trong phút cuối, p95 < 1 giây.
- Không lộ dữ liệu tenant; mất mạng/restart không làm mất bài.
- Plugin và công thức thay đổi không deploy core.

Nguồn: [scenarios](05-qa-scenarios.md), [utility tree](06-utility-tree.md).

---

# 2. Tải có lịch trước

- 8.000/60 ≈ 134 submission/s.
- 8.000 autosave/5s ≈ 1.600 write/s nếu tất cả cùng gửi.
- Pre-scale theo lịch, jitter autosave, receipt bền và worker sau ack.
- Kết quả đo final local: 8.000/60s; p95 266,65ms; 0 lỗi.

Nguồn: [capacity](13-capacity-and-cost.md), [verification](11-verification.md).

---

# 3. Khác biệt tenant

| Core chung | Điểm khác biệt |
|---|---|
| Khóa học, lớp, thi, bảng điểm | Trọng số/làm tròn/điều kiện đạt |
| Hẹn giờ và nộp bài | Quy chế xem lại, xáo đề |
| Đăng nhập | IdP OIDC/SAML, claim mapping |
| Extension point | Plugin QR, widget, thông báo |

Phỏng vấn ≥2 người: **chưa có kết quả thật**, nhóm cần bổ sung.

---

# 4. Multi-tenancy

- Shared schema + RLS: rẻ, phụ thuộc policy/session đúng.
- Schema-per-tenant: tách namespace, role sai vẫn có thể đọc chéo.
- **V2: DB-per-tenant, role riêng, shared compute.**
- Tenant A role không CONNECT được DB B (đã kiểm trực tiếp).
- Giá phải trả: pool, secret, migration và backup cho nhiều DB.

Nguồn: [ADR-001](../adr/001-tenancy.md).

---

# 5. Context và trust boundary

- Browser ↔ Gateway: TLS, xác minh tenant từ identity.
- Gateway ↔ Core: trusted context, không tin body/query tenant.
- Core ↔ DB: credential tenant riêng.
- Core ↔ plugin: HTTP timeout, không chia credential DB.

Hình: [C4 L1](../diagrams/01-context.puml), [C4 L2](../diagrams/02-containers.puml).

---

# 6. Đường nộp bài

1. Client lưu IndexedDB, tạo idempotency key/sequence.
2. API commit receipt vào DB tenant rồi trả HTTP 202.
3. Worker xử lý sau; retry cùng key không tạo bài trùng.
4. Restart API sau ack vẫn truy lại được receipt.

Hình: [sequence](../diagrams/05-submit-sequence.puml); quyết định [ADR-005](../adr/005-exam-receipt.md).

---

# 7. Plugin và công thức điểm

- QR ở process riêng, enablement theo tenant tại runtime.
- Plugin lỗi chỉ làm chức năng QR trả lỗi; nộp bài độc lập.
- Formula JSON whitelist, version bất biến; tenant A 10/30/60, B 20/20/60.
- Cùng điểm thành phần, A = 76; B = 78.

Nguồn: [ADR-003](../adr/003-plugin.md), [ADR-004](../adr/004-grading.md).

---

# 8. ATAM và v2

- R1: ack trước durable → commit receipt trước 202.
- R2/R3: query/role RLS sai → DB-per-tenant và role riêng.
- R4: offline/quota → IndexedDB, retry, cảnh báo khi lưu lỗi.
- Trade-off chính: isolation và reliability tăng chi phí/latency vận hành.

Nguồn: [ATAM](09-atam.md). Peer review người thật: **chờ thực hiện**.

---

# 9. Bằng chứng prototype

- Integration: grading, cross-tenant 404, idempotency, autosave order, plugin QR.
- PostgreSQL: tenant A bị từ chối CONNECT DB B.
- Restart: receipt sau ack vẫn đọc lại.
- Browser offline 60s: nháp đồng bộ sau reconnect.
- Load hợp lệ: 8.000 bắt đầu trong 60s, p95 266,65ms, 0 lỗi.

Chỉ đo local, payload nhỏ, một tenant; xem [điều kiện đo](11-verification.md).

---

# 10. Bài học và việc cần xác nhận

- Cần load test autosave đồng thời, TLS/SSO, hạ tầng target và chi phí thật.
- Cần phỏng vấn ≥2 giảng viên/cán bộ, peer review, review code AI và luyện vấn đáp chéo.
- Nếu tải tăng 10 lần: đo DB WAL/pool/queue trước, rồi tách đường autosave hoặc tenant lớn.

Nguồn: [SAD](10-sad.md), [vấn đáp](12-presentation.md), [AI log](../ai-log.md).
