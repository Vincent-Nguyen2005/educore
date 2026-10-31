# 01 – Business Goals

| # | Business goal | Chỉ số đo | Mốc | Nguồn con số |
|---|---|---|---|---|
| BG1 | 2 tenant trả tiền khi MVP → 5 tenant / 200K user | # tenant, # active user | 6 / 18 tháng | Nhóm tự đặt |
| BG2 | 99.9% uptime tháng thường, 99.95% trong exam window | % uptime (SLO) | Từ MVP | Nhóm tự đặt |
| BG3 | Chi phí/tenant giảm ≥ 40% so với single-tenant (tenant < 15K user) | $/user/tháng | Sau 12 tháng | Nhóm tự đặt; kiểm chứng bằng mô hình chi phí ở M2 |
| BG4 | Onboard tenant mới: Basic ≤ 1 ngày làm việc, Enterprise ≤ 1 tuần (baseline 6 tuần) | Thời gian go-live | Sau 6 tháng | "1 ngày" từ scenario (e) trong hướng dẫn; "6 tuần" là baseline giả định của nhóm |
| BG5 | 0 sự cố rò rỉ chéo tenant | # finding nghiêm trọng = 0 (audit + pen-test) | Hàng quý | Nhóm tự đặt |

> BG4 đã sửa so với bản trước (≤ 1 tuần) để khớp scenario bắt buộc "onboard tenant mới trong 1 ngày". Nhóm cần xác nhận lại việc tách Basic / Enterprise.

## Liên hệ goal → quality attribute
- BG1, BG3 → Cost-efficiency, Multi-tenancy
- BG2 → Availability, Reliability, Performance
- BG4 → Extensibility, Operability (tenant bootstrap tự động)
- BG5 → Security / Multi-tenancy isolation

## Tự kiểm tra
Hai goal nào kéo ngược nhau? **BG3 (chi phí thấp, dùng chung tài nguyên) ↔ BG5 (cô lập tuyệt đối).** Cách giải quyết nằm ở ADR multi-tenancy (M2).
