# Giai đoạn 2 — Tactics và kiến trúc tổng thể (M2, tuần 8)

## Bước 7: Tactic cho 5 ASR

| ASR | Tactic ứng viên | Chọn và lý do | Tác động bất lợi |
|---|---|---|---|
| ASR-1 S1 | Tăng tài nguyên theo lịch; queue load leveling; cache đề thi | Pre-scale API/DB pool trước giờ thi; ghi receipt vào durable queue rồi worker xử lý; cache đề đọc nhiều. 8.000/60 ≈ 134 submission/s, chưa kể autosave. | Tăng chi phí trong exam window; queue tạo độ trễ hiển thị điểm; nếu ack trước khi durable sẽ mất bài. |
| ASR-2 S2 | Client local persistence; retry có backoff; replication | IndexedDB ghi mỗi thay đổi, gửi autosave ≤ 5s và retry với sequence/idempotency key. Server chỉ ack sau commit bền. | Local disk có thể đầy/không cho phép; dữ liệu trên thiết bị cần xóa sau thi. |
| ASR-3 S4 | Authenticate tenant; authorize mỗi request; DB isolation | Tenant từ token đã kiểm chữ ký, khớp host; DB role tenant riêng và RLS defense in depth. Không lấy tenant từ body/query. | Provision role/DB phức tạp; migration nhiều tenant. |
| ASR-4 S5 | Plugin interface; process isolation; circuit breaker | Extension point qua HTTP worker/plugin process và registry version theo tenant. Timeout, fail closed và không chạy code plugin trong core. | RPC và vận hành plugin tốn tài nguyên. |
| ASR-5 S6 | Config-driven behavior; versioned rules; async recompute | Công thức JSON gồm trọng số whitelist, version bất biến; tính điểm bằng pure function; job recompute ghi version. | Thay quy chế cần migration dữ liệu điểm lịch sử; JSON giới hạn biểu thức. |

Tactic tham chiếu nhóm trong *Software Architecture in Practice* (Bass et al.): manage resources, detect/recover from faults, resist attacks, defer binding và encapsulate. Đây là phân loại tham khảo, không phải kết quả đo.

## Bước 8: So sánh style theo ASR

| Tiêu chí | Modular monolith + worker tách process | Microservices toàn phần |
|---|---|---|
| S1 burst | Scale API/worker riêng, đủ cho đường nộp bài | Scale từng service, nhưng thêm network hop |
| S2 autosave | Ít hop, dễ idempotency | Nhiều điểm lỗi hơn |
| S4 isolation | Một ingress/auth và DB policy nhất quán | Mỗi service phải giữ tenant context |
| S5 plugin | Plugin process tách biệt qua contract | Tự nhiên qua service riêng, chi phí cao |
| S6 grading | Một module versioned, dễ test | Có thể tách sau khi tải tăng |
| Đội 4 người / 15 tuần | Phù hợp hơn | Gánh CI/CD, tracing, contract test lớn |

**Quyết định thiết kế đề xuất:** core modular monolith, exam worker và plugin runner tách process. Đường đọc đề qua cache/CDN, đường ghi qua receipt bền và worker. Bản v1 giả định shared schema + RLS; sau ATAM, bản v2 đổi sang database-per-tenant trên cùng cụm PostgreSQL vì yêu cầu S4 đặt cao hơn chi phí metadata/migration. Compute vẫn dùng chung, có quota để giảm noisy neighbor. Xem ADR-001 và tài liệu ATAM.

## Phạm vi prototype

Skeleton minh họa tenant DB riêng, công thức JSON, plugin QR tải động, nộp bài idempotent và test. SSO OIDC/SAML, object storage, plagiarism và analytics là integration contract/mock trong kiến trúc, chưa được triển khai như production. Không lấy kết quả prototype cục bộ để suy ra SLO production.
