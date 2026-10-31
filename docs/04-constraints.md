# 04 – Constraints

| Loại | Ràng buộc | Vì sao không thương lượng |
|---|---|---|
| Kỹ thuật | Cloud + Kubernetes, container hóa | Cam kết hạ tầng SaaS |
| Kỹ thuật | SSO SAML 2.0 / OIDC | IdP do trường sở hữu |
| Kỹ thuật | p95 < 1s cho 8K submission/phút cuối giờ | Đã cam kết với khách hàng |
| Kinh doanh | MVP 6 tháng, đội 3 người | Ngân sách & hợp đồng |
| Kinh doanh | Ngân sách cloud giai đoạn 1 ≤ $X/tháng | Ràng buộc chi phí (X: chờ chốt) |
| Pháp lý | Audit log truy cập dữ liệu SV; tuân thủ quy chế thi | Bắt buộc theo quy định |

## Constraint vs Requirement
- **Constraint**: ràng buộc không thương lượng, giới hạn không gian giải pháp. VD: "phải dùng SSO SAML/OIDC của trường".
- **Requirement**: tính năng/hành vi hệ thống phải có, có thể ưu tiên/thương lượng. VD: "có bảng điểm".
