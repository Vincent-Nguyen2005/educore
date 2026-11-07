# EduCore — SE 403, đề tài 4

LMS SaaS đa trường, tổ chức theo **giai đoạn 0–5** của [hướng dẫn môn](CMUSE%20403%20%E2%80%93%20H%C6%B0%E1%BB%9Bng%20d%E1%BA%ABn%20th%E1%BB%B1c%20hi%E1%BB%87n%20Group%20Project.pdf). Repo có SAD, ADR, view, ATAM và prototype hai tenant. Kết quả đo chưa được tuyên bố khi chưa chạy test.

## Lộ trình và sản phẩm

| Giai đoạn | Tuần / mốc | Bước | Sản phẩm |
|---|---|---|---|
| 0 Khởi động | 1–2 | 1–2 | Phân vai, repo, [assumptions](docs/07-assumptions.md) |
| 1 Drivers | 4 / M1 | 3–6 | [Goals](docs/01-business-goals.md), [stakeholders](docs/02-stakeholders.md), [use cases](docs/03-use-cases.md), [constraints](docs/04-constraints.md), [scenarios](docs/05-qa-scenarios.md), [utility tree](docs/06-utility-tree.md) |
| 2 Thiết kế | 8 / M2 | 7–10 | [Tactics/style](docs/08-tactics-and-style.md), [views](diagrams/README.md), [ADR](adr/README.md) |
| 3 Đánh giá | 11 / M3 | 11–12 | [ATAM và Architecture v2](docs/09-atam.md) |
| 4 Prototype | 14 / M4 | 13–14 | [Code](src/core/app.py), [test](tests/integration.py), [load test](src/loadtest/load.py), [verification](docs/11-verification.md) |
| 5 Hoàn thiện | 15 / M5 | 15 | [SAD](docs/10-sad.md), [slides](docs/slides.md), [vấn đáp](docs/12-presentation.md), [AI log](ai-log.md) |

## Chạy prototype

Cần Docker Desktop đang chạy. Tại thư mục gốc:

```sh
docker compose up --build -d
python tests/integration.py
python tests/restart.py
python -m pip install -r src/loadtest/requirements.txt
python src/loadtest/load.py --users 8000 --seconds 60
```

Demo browser: `http://localhost:8080/static/exam-demo.html`. API key demo là `demo-key-a` và `demo-key-b`; đây chỉ là credential thử nghiệm, không phải SSO production. Lần đầu PostgreSQL init tạo hai DB, hai role độc lập. Sau khi đổi init SQL, cần tạo **volume mới có chủ đích** hoặc migration vì init script chỉ chạy khi DB chưa tồn tại. Không xóa volume nếu còn bài làm cần giữ.

Unit test không cần Docker:

```sh
python -m unittest discover -s tests -v
```

Load script ghi `load-results.json` gồm raw latency, thời điểm bắt đầu và summary. [Kết quả đo thực tế](docs/11-verification.md) có run 8.000/60s hợp lệ với p95 266,65ms trên máy local; không lấy số đo máy cá nhân để khẳng định SLA production. Dockerfile dùng `--trusted-host` cho pip vì môi trường phát triển hiện lỗi CA; production phải cấu hình CA đáng tin cậy và bỏ tùy chọn này.

## Phạm vi và việc cần người thật hoàn tất

- Phỏng vấn ít nhất hai giảng viên/cán bộ đào tạo, điền [bảng khác biệt tenant](docs/07-assumptions.md).
- Nhóm xác nhận phân vai, các ADR, tổ chức peer review và ghi nhận phản hồi thật vào [ATAM](docs/09-atam.md).
- Chạy lại integration/load/restart test trên hạ tầng mục tiêu; mở rộng browser test cho crash/quota, kiểm tra TLS/SSO và autosave nền đồng thời theo [verification](docs/11-verification.md).
- Mỗi thành viên review code AI tạo, điền người review và quyết định giữ/sửa/bỏ trong [AI log](ai-log.md), luyện vấn đáp chéo.

Prototype chỉ bao phủ exam, tenant routing, grading và plugin QR. Course/content, SSO, plagiarism và báo cáo được mô tả ở view và contract nhưng chưa là tính năng chạy được. SLO p95 và 0 mất bài chưa được xác nhận.
