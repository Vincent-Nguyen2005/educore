# ADR-004 — Formula JSON có version

**Status:** Proposed.

**Context:** S6 đòi tenant đổi trọng số không redeploy, điểm cũ truy vết được.

**Options considered:** Python/JS expression linh hoạt nhưng chạy code nguy hiểm; rule engine tổng quát mạnh nhưng phức tạp; JSON whitelist trọng số đủ cho MVP và dễ validate.

**Decision:** Formula là JSON bất biến theo version, khóa `attendance`, `midterm`, `final` (0–100), trọng số không âm tổng 100, rounding được định nghĩa. Grade record giữ formula version. Recompute là job riêng, không chặn đọc/nộp bài.

**Consequences:** Dễ audit và tính tay, không cần deploy. Không biểu diễn được mọi quy chế phức tạp; khi phỏng vấn phát hiện điều kiện đạt môn đặc biệt, mở DSL có grammar/kiểm thử chứ không eval tùy ý.
