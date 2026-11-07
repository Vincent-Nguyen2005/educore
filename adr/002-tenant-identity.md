# ADR-002 — Tenant từ identity đã xác thực

**Status:** Proposed.

**Context:** S4 và S10 cần tenant routing đúng, SSO từng trường. Client có thể sửa header/body.

**Options considered:** (1) `tenant_id` từ query/header client: đơn giản nhưng có thể giả mạo. (2) Subdomain một mình: DNS/Host không chứng minh danh tính. (3) Token OIDC/SAML đã xác minh, claim tenant khớp subdomain: cần IdP mapping và kiểm chữ ký.

**Decision:** Gateway xác minh issuer, audience, signature, expiry; map IdP → tenant trong control plane; so claim và host. Core chỉ nhận context đã ký từ gateway. Role tenant được kiểm ở object access. Skeleton dùng demo API key cố định qua env để test luồng; không phải SSO production.

**Consequences:** Giảm IDOR/cross-tenant. Thêm quản lý IdP, key rotation và clock skew; nếu control plane cấu hình sai tenant/credential vẫn có risk cần kiểm chéo và audit.
