# EduCore – LMS & Thi trực tuyến đa trường (SaaS)

SE 403 – Group Project · Đề tài 4 · Giai đoạn 0 (Khởi động) và Giai đoạn 1 (Architectural Drivers, mốc M1).

## Bài toán
EduCore là nền tảng LMS SaaS dùng chung cho nhiều trường đại học/cao đẳng. Mỗi trường là một **tenant** (10.000–40.000 SV) với quy trình đào tạo và công thức tính điểm riêng. Đợt thi cuối kỳ có thể có **8.000 SV nộp bài trong 1 phút cuối**.

Ba thách thức kiến trúc cốt lõi:
1. **Multi-tenancy & Security** – cô lập dữ liệu tuyệt đối giữa các tenant, kể cả khi lỗi cấu hình.
2. **Performance dưới tải đột biến dự báo được** – 8.000 nộp bài/phút, p95 < 1 giây.
3. **Extensibility** – công thức điểm cấu hình được + plugin hot-install (VD điểm danh QR) không redeploy core.

Ngoài ra: không mất bài khi mất mạng/server restart (mất tối đa 30 giây thao tác); chi phí hạ tầng tỷ lệ với số tenant.

## Nhóm (3 thành viên)

Mỗi người giữ một hoặc hai vai chịu trách nhiệm chính nhưng vẫn tham gia mọi phần.

| Thành viên | Vai trò | Sản phẩm phụ trách chính | Mốc |
|---|---|---|---|
| Châu Y Kazan | Lead Architect | ADR, C4, quyết định multi-tenancy | M1, M2 |
| Châu Y Kazan | Documentation Owner | docs/, ai-log.md, biên bản họp, báo cáo | Mọi mốc |
| Nguyễn Văn Huy | Requirements Owner | Business goals, use case, QA scenario, Utility Tree | M1 |
| Nguyễn Văn Huy | QA/Test Lead | Test cách ly dữ liệu, load test, test plan | M3 |
| Phan Hùng Khanh | Prototype Lead | 2 tenant + 1 plugin động + load test | M2, M3 |

> Cách chia vai trên là đề xuất ban đầu (5 vai / 3 người). Nhóm họp thống nhất lại và sửa bảng này nếu cần.

## Cấu trúc repo
```
educore/
├── docs/
│   ├── 01-business-goals.md      02-stakeholders.md
│   ├── 03-use-cases.md           04-constraints.md
│   ├── 05-qa-scenarios.md        06-utility-tree.md
│   └── 07-assumptions.md
├── adr/
├── diagrams/
├── src/   (tenant-a, tenant-b, plugin-qr, core, loadtest)
├── ai-log.md
└── README.md
```

## Prototype tối thiểu (M2–M4)
- 2 tenant với công thức tính điểm khác nhau
- 1 plugin cài đặt động (điểm danh QR)
- Load test kịch bản nộp bài thi đồng thời
- Test chứng minh cách ly dữ liệu giữa tenant
- Chạy được bằng một lệnh `docker compose up`

## Nguyên tắc
AI là trợ lý, không phải tác giả – mọi thành viên phải giải thích được nội dung khi vấn đáp. Mọi lần dùng AI ghi vào `ai-log.md`.
