# ADR-001 — Database-per-tenant trên shared cluster

**Status:** Proposed v2 (thay thế giả định shared schema v1 ở M1; cần nhóm phê duyệt).

**Context:** S4 đòi không lộ dữ liệu dù query thiếu tenant predicate. Tenant nhỏ cần chia compute (S7); backup/restore một tenant cần khả thi.

| Option | Isolation khi thiếu WHERE | Cost | Migration | Backup/restore tenant |
|---|---|---|---|---|
| Shared schema + `tenant_id` + RLS | Phụ thuộc policy/session/role; lỗi cấu hình có thể làm lộ | Thấp | Một schema | Khó tách |
| Schema-per-tenant | Query trỏ sai schema vẫn có thể lộ nếu role được quyền nhiều schema | Trung bình | 50 schema phải orchestration | Khá thuận tiện |
| Database-per-tenant, role riêng | Role chỉ vào một DB; query thiếu WHERE không đọc DB khác | Cao hơn | 50 DB phải canary/batch | Thuận tiện |

**Decision:** Dùng một PostgreSQL cluster chia compute, DB và login role riêng mỗi tenant. Control plane map identity → credential DB, credential lưu secret manager. Pool theo tenant có trần; tenant lớn chuyển cluster riêng khi cần. Prototype dùng 2 DB trong compose.

**Consequences:** Cách ly dữ liệu trước lỗi query và restore từng tenant dễ. Đổi lại số DB, pool, secret và migration tăng. Không thể tuyên bố an toàn nếu control plane map sai credential hoặc service dùng superuser; bắt buộc test quyền và audit. Schema migration chạy canary một DB rồi batch giới hạn, theo dõi version từng DB, rollback bằng migration/backup đã kiểm.
