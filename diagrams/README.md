# Architecture views v2

Các view dùng PlantUML thuần. Render bằng PlantUML hoặc VS Code extension. Chú giải chung: `-->` là HTTPS/JSON đồng bộ trừ khi ghi khác; `..>` là bất đồng bộ; cylinder là data store; ranh giới trust nằm ở cạnh gateway, DB và plugin. Mỗi view có chú giải riêng trong hình.

| View | Nội dung |
|---|---|
| [C4 L1](01-context.puml) | Người dùng, EduCore, IdP và plagiarism provider |
| [C4 L2](02-containers.puml) | Core, worker, plugin, DB tenant và cache |
| [C4 L3](03-components.puml) | Module quan trọng trong core API |
| [Deployment](04-deployment.puml) | Pre-scale, pool, DB và plugin isolation |
| [Submit](05-submit-sequence.puml) | Receipt bền, worker và retry |
| [Plugin](06-plugin-sequence.puml) | Bật QR runtime cho một tenant |

C4 L2 gồm object storage/video, SSO adapter, plagiarism mock và reporting theo kiến trúc mục tiêu. Skeleton chỉ hiện thực exam/grading/plugin/tenant routing, được ghi rõ trong SAD. Nếu thay đổi contract, cập nhật view tương ứng.
