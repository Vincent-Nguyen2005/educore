# ADR-006 — Modular monolith + isolated workers

**Status:** Proposed.

**Context:** Đội 4 người, thời gian học phần ngắn; S1/S5 cần scale và fault isolation có chọn lọc.

**Options considered:** Full microservices scale độc lập nhưng tăng tracing, CI/CD, auth propagation, distributed consistency. Monolith một process triển khai nhanh nhưng plugin/worker có thể kéo sập core. Modular monolith với exam worker và plugin process tách đáp ứng cả hai.

**Decision:** Chọn modular monolith core, exam worker và plugin process. Contract giữa module nội bộ rõ; chỉ tách service khi phép đo cho thấy bottleneck.

**Consequences:** Code và giao dịch đơn giản hơn, ít hạ tầng. Core vẫn có blast radius nội bộ; phải giữ boundary module và test. Worker/DB cần scale riêng khi 8K/min đo không đạt.
