# 02 – Stakeholders

## Stakeholder – Mối quan tâm – QA ưu tiên

| Stakeholder | Mối quan tâm chính | QA ưu tiên |
|---|---|---|
| Sinh viên | Không mất bài, làm bài mượt, kết quả công bằng | Reliability, Performance |
| Giảng viên | Tạo đề nhanh, chấm đúng, chống gian lận | Correctness, Security |
| Phòng đào tạo | Công thức điểm đúng quy chế, báo cáo đầy đủ | Extensibility, Data integrity |
| Quản trị tenant | Cấu hình độc lập, không lẫn dữ liệu trường khác | Multi-tenancy & Security |
| Công ty SaaS (owner) | Chi phí thấp, scale được, uptime toàn cục | Cost-efficiency, Reliability |
| Đội bán hàng | Demo plugin & công thức nhanh để chốt deal | Extensibility, Time-to-onboard |
| Đội vận hành | Quan sát được, deploy 0 downtime, xử lý sự cố | Operability, Availability |

## Cặp stakeholder xung đột

1. **Quản trị tenant ↔ Công ty SaaS**
   Tenant muốn DB riêng (isolation tuyệt đối); SaaS muốn shared schema (cost thấp).
   → Cần ADR multi-tenancy phân tier: Basic = shared schema + RLS, Enterprise = dedicated schema/DB.

2. **Sinh viên ↔ Đội vận hành / SaaS owner**
   Autosave thường xuyên làm tăng write load và chi phí.
   → Cần write-behind + debounce phía client/server.
