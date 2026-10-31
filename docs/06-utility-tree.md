# 06 – Utility Tree & ASR

## Utility Tree – (Business Importance, Technical Risk)

| Nhánh QA | Scenario | (BI, TR) | Quyết định |
|---|---|---|---|
| Performance | S1 – Exam burst 8K/min, p95 < 1s | (H, H) | **ASR-1** |
| Reliability | S2 – Mất mạng, mất ≤ 30s thao tác | (H, H) | **ASR-2** |
| Reliability | S3 – Instance restart, 0 mất autosave | (H, M) | Không phải driver – pattern chuẩn (stateless + DB bền) |
| Security/MT | S4 – 100% cô lập tenant | (H, H) | **ASR-3** |
| Extensibility | S5 – Plugin hot install / tenant | (H, H) | **ASR-4** |
| Extensibility | S6 – Công thức điểm versioned | (H, H) | **ASR-5** |
| Cost | S7 – Tenant nhỏ ≤ 5% chi phí tăng | (H, M) | Phụ thuộc ADR multi-tenancy |
| Availability | S8 – 99.95% exam window | (H, H) | Bị bao phủ bởi S1 + S3 |
| Usability | S9 – Autosave 5s | (M, L) | Không phải driver |
| Operability | S10 – Onboard tenant ≤ 1 ngày | (M, M) đề xuất | Không chọn ASR; nhóm biểu quyết lại. Là hệ quả của ASR-3 và ASR-5 |

## 5 ASR

| ASR | Nội dung | ADR dự kiến (M2) |
|---|---|---|
| ASR-1 | 8K submission/phút, p95 < 1s, error < 0.1% | Pre-scaling + queue/write-behind |
| ASR-2 | Mất mạng 60s → mất ≤ 30s thao tác, 0 mất autosave | Client buffer + idempotent autosave |
| ASR-3 | Cô lập tenant 100%, 0 leak dù misconfig | Multi-tenancy (shared schema + RLS; Enterprise = dedicated DB) |
| ASR-4 | Plugin hot-install cho 1 tenant, 0 downtime core | Microkernel + plugin sandbox |
| ASR-5 | Công thức điểm versioned, recompute 10K < 5 phút | Pluggable grading engine + versioned formula |

## Lý do chọn/bỏ
- **S1, S2, S4, S5, S6 – (H, H)**: sống còn với kinh doanh (mất bài = mất khách; leak = mất giấy phép; không extensible = mất lợi thế SaaS) và rủi ro kỹ thuật cao (không có pattern "đóng hộp").
- **S3, S7 – (H, M)**: quan trọng nhưng đã có pattern phổ biến → không cần quyết định kiến trúc đặc biệt.
- **S8**: không chọn riêng vì đã được bao phủ bởi S1 + S3.
- **S9 – (M, L)**: không phải driver.

> Xếp hạng do cả nhóm biểu quyết từng scenario và ghi biên bản (AI chỉ giải thích lý thuyết).
