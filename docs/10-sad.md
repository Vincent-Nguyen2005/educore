# Software Architecture Document — EduCore v2

## 1. Giới thiệu

EduCore là LMS SaaS đa trường. Mỗi tenant có 10.000–40.000 sinh viên; giờ thi có 8.000 sinh viên nộp trong phút cuối. Tài liệu này nối driver, quyết định, view, đánh giá và prototype theo 15 bước của hướng dẫn SE 403. Đây là thiết kế và skeleton học phần, chưa phải chứng nhận SLO production.

## 2. Drivers và truy vết

M1: [business goals](01-business-goals.md), [stakeholders](02-stakeholders.md), [use cases](03-use-cases.md), [constraints](04-constraints.md), [scenarios](05-qa-scenarios.md), [utility tree](06-utility-tree.md), [assumptions](07-assumptions.md). Năm ASR ưu tiên là S1, S2, S4, S5 và S6. S3 restart, S7 cost, S8 availability và S10 onboarding được kiểm tra như hệ quả.

M2: [tactics và style](08-tactics-and-style.md), [capacity/cost](13-capacity-and-cost.md), [ADR](../adr/README.md) và [views](../diagrams/README.md). M3: [ATAM/v2](09-atam.md). M4: [verification plan và kết quả](11-verification.md). M5: tài liệu này, [slide](slides.md), [kịch bản trình bày/vấn đáp](12-presentation.md), [AI log](../ai-log.md).

## 3. Kiến trúc

- Core API là modular monolith: auth/tenant routing, course, exam, grading, plugin registry. Tenant xác định từ token đã xác thực và subdomain phải khớp. SSO thực tế đi qua OIDC/SAML adapter, chưa có trong skeleton.
- PostgreSQL cluster dùng compute chung, mỗi tenant có database và role riêng. API dùng credential DB của tenant tương ứng. Lỗi query thiếu predicate tenant vẫn không thể đọc database tenant khác. Catalog tenant/credentials cần một control plane giới hạn quyền, secret manager và rotation; prototype dùng env cho 2 tenant.
- Exam submission lưu receipt bền, trả HTTP 202 sau commit, worker chấm/aggregate sau. Idempotency key và thứ tự autosave chống ghi lùi. Client ghi IndexedDB rồi mới gửi; nếu offline sẽ retry.
- Plugin chỉ nhận event/command theo contract, process riêng với timeout và tenant-scoped enablement. Plugin QR không có quyền DB core; plugin có lỗi không làm chết core.
- Grading JSON whitelist trọng số; mỗi formula là version bất biến. Điểm lịch sử gắn version đã áp dụng.

## 4. Bảo mật và vận hành

Trust boundaries: browser ↔ gateway TLS; gateway ↔ core verified identity; core ↔ tenant DB restricted role; core ↔ plugin worker network contract. Audit access denials và thay đổi cấu hình phải append-only ngoài tenant DB trong production. Noisy neighbor được giới hạn bằng per-tenant rate limit, queue quota, pool riêng và lịch pre-scale. Backup/restore theo DB tenant; migration theo từng DB theo canary rồi batch, không chạy đồng thời không giới hạn.

## 5. Đánh giá và giới hạn

ATAM v2 xử lý R1, R2/R3, xem [ATAM](09-atam.md). Prototype minh họa cấu trúc và các test chạy được trong môi trường có Docker. Nó không bao gồm SSO thật hay cluster Kubernetes; client IndexedDB ở mức demo. Chỉ ghi SLO đã đạt khi có kết quả load/fault test thực; các thao tác cần người thật như phỏng vấn và peer review vẫn mở.

## 6. Bài học và quyết định cần xác nhận

Yêu cầu “cô lập tuyệt đối dù lỗi cấu hình” khiến DB-per-tenant đáng chọn hơn shared schema cho bản v2. Chi phí thêm chủ yếu ở connection, catalog và migration. Nếu product xác nhận shared schema chấp nhận được, ADR-001 cần xem lại; không được âm thầm hạ mức isolation. Công thức điểm JSON có chủ ý giới hạn để tránh chạy code tùy ý trong core.
