# AI Log

> Nguyên tắc: AI là trợ lý, không phải tác giả. Mọi thành viên phải giải thích được nội dung khi vấn đáp.
> Cột **Ngày** do nhóm điền theo thực tế. Cột cuối là quan trọng nhất.

Thành viên: Châu Y Kazan (Kazan) · Nguyễn Văn Huy (Huy, nhóm trưởng) · Phan Hùng Khanh (Khanh) · Trương Nguyễn Bảo Tâm (Tâm)

| Ngày | Thành viên | Công cụ | Mục đích / prompt tóm tắt | AI đề xuất gì | Nhóm đã giữ / sửa / bỏ gì và vì sao |
|---|---|---|---|---|---|
| _(điền)_ | Kazan | ChatGPT | Gợi ý cấu trúc repo cho dự án có ADR + C4 dạng code | Cây thư mục | Giữ – khớp hướng dẫn môn; thêm `loadtest/` vì có load test |
| _(điền)_ | Huy | Claude | "Đặt 10 câu hỏi làm rõ yêu cầu cho LMS SaaS đa tenant + thi 8K" | 12 câu, 3 câu trùng | Giữ 10, gộp 2 cặp trùng; bỏ 2 câu UX ngoài phạm vi kiến trúc |
| _(điền)_ | Huy | ChatGPT | "Stakeholder Quản trị tenant lo gì?" | 8 mối lo | Giữ 4, gộp 2, bỏ 2 (UI theme không phải QA kiến trúc) |
| _(điền)_ | Huy | ChatGPT | "3–5 business goal đo được" | 6 goal, có goal mơ hồ | Giữ 5; sửa "nâng cao trải nghiệm" thành chỉ số cụ thể; mốc do nhóm đặt |
| _(điền)_ | Huy | ChatGPT | "12 use case này thiếu luồng ngoại lệ nào?" | 6 gợi ý | Giữ offboarding + audit; bỏ 4 vì ngoài phạm vi M1–M3 |
| _(điền)_ | Kazan | Claude | "Phân biệt constraint và requirement" | Giải thích + ví dụ | Giữ; tự viết lại theo ví dụ của đề tài |
| _(điền)_ | Huy | ChatGPT | "Scenario này đo lường/kiểm thử được không? Chỉ phần mơ hồ" | S7 cần baseline; S3 cần định nghĩa "khôi phục" | Sửa S7 và S3 |
| _(điền)_ | Huy | ChatGPT | "Giải thích cách xếp hạng (BI, TR)" | Lý thuyết | Giữ lý thuyết; không để AI xếp hạng, nhóm tự biểu quyết, ghi biên bản |
| _(điền)_ | Khanh | Claude | "Cách đo p95 cho 8K nộp bài/phút bằng k6" | Script mẫu | Giữ ý tưởng; tự viết script ở M4, không nộp code chưa đọc |
| _(điền)_ | _(điền)_ | Claude | Soạn bản Word + repo này từ nội dung nhóm cung cấp và hướng dẫn SE 403 | Văn bản; thêm S10 (onboard 1 ngày), bảng khác biệt tenant, bảng "3 câu hỏi" | _(nhóm điền: đã đọc, sửa gì, giữ gì và vì sao)_ |

## Lần hỗ trợ AI hiện tại (07/11/2026)

| Ngày | Thành viên | Công cụ | Mục đích / prompt tóm tắt | AI đề xuất gì | Nhóm đã giữ / sửa / bỏ gì và vì sao |
|---|---|---|---|---|---|
| 07/11/2026 | Người yêu cầu (chờ nhóm xác nhận tên) | Codex | Thực hiện tuần tự giai đoạn 0–5 EduCore theo PDF | ADR, views PlantUML, ATAM v2, SAD, skeleton Docker/Python, test và slide outline | **Chưa được nhóm review/chấp nhận**. Cần đọc từng ADR, chạy test và ghi sửa đổi cùng lý do trước khi nộp. Không dùng số đo giả; phỏng vấn/peer review để trống. Reviewer cho từng file code: chờ phân công. |

## Checklist nộp M1

**Giai đoạn 0**
- [x] Phân vai + repo Git với docs/, adr/, diagrams/, src/, ai-log.md
- [x] Tóm tắt bài toán hợp nhất + 10 câu hỏi làm rõ + 7 giả định
- [ ] Bảng khác biệt giữa các tenant có kết quả phỏng vấn ≥ 2 giảng viên/cán bộ đào tạo (docs/07)

**Giai đoạn 1**
- [x] 5 business goals đo được
- [x] Bảng stakeholder + QA ưu tiên + cặp xung đột
- [x] Use case + constraint (kỹ thuật/kinh doanh/pháp lý)
- [x] 10 QA scenario đủ 6 phần, có đủ 5 scenario bắt buộc (a)–(e)
- [x] Utility Tree + 5 ASR (H,H) + lý do chọn/bỏ
- [ ] AI log điền đủ ngày; cột "giữ/sửa/bỏ và vì sao" không để trống
- [ ] Mỗi thành viên xác nhận hiểu từng mục, đã luyện vấn đáp ít nhất một lần
