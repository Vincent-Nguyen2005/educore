# ADR-003 — Microkernel với plugin process

**Status:** Proposed.

**Context:** S5 cần bật QR cho tenant A khi core đang chạy; plugin lỗi không được chặn bài thi.

**Options considered:** Import code plugin in-process dễ triển khai nhưng crash/CPU/blocking ảnh hưởng core; webhook/plugin process qua JSON contract tăng RPC nhưng có timeout; WASM sandbox cô lập mạnh hơn song runtime phức tạp cho MVP.

**Decision:** Core sở hữu extension registry theo tenant và contract version. Extension points: `attendance.record`, `submission.accepted` và `dashboard.widget`; grading dùng JSON config riêng. Plugin QR chạy process riêng qua HTTP, có timeout 500ms và chỉ nhận tenant-scoped payload không chứa credential DB. SaaS owner duyệt gói/signature, tenant admin chỉ bật gói đã duyệt. Enable/disable là thay đổi registry runtime.

**Consequences:** Core không load plugin code; plugin chết chỉ mất tính năng QR. Cần rate limit, retries cho sự kiện async, schema version và vận hành process. Prototype chỉ hiện thực QR synchronous; sandbox hệ điều hành và ký gói là việc production.
