# ADR-005 — Durable receipt trước HTTP 202

**Status:** Proposed v2.

**Context:** S1, S2, S3 yêu cầu tải cao nhưng không mất bài sau restart.

**Options considered:** Ghi thẳng DB và chấm đồng bộ làm p95 nhạy theo worker; memory queue trả ack nhanh nhưng mất khi restart; durable queue/bảng receipt rồi worker async giữ bài và giảm critical path.

**Decision:** API ghi submission/autosave idempotent vào DB tenant, commit rồi mới trả receipt 202. Worker poll pending và chấm sau. Client IndexedDB ghi trước, retry cùng key; sequence tăng để tránh autosave cũ ghi đè. Production có thể thay receipt table bằng broker durable nhưng vẫn phải ack sau broker confirm và theo dõi lag.

**Consequences:** Không mất receipt đã ack nếu DB bền; latency thêm I/O commit và cần scale DB, queue lag, cleanup/retry. Nếu DB unavailable API trả lỗi để client tiếp tục giữ local. Không được coi 202 là đã chấm xong.
