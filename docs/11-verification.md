# Giai đoạn 4 — Kế hoạch kiểm chứng và kết quả (M4, tuần 14)

## Điều kiện đo

Mọi dòng kết quả cần ghi ngày, máy, CPU/RAM, Docker version, số replica, cỡ payload, số tenant, số request thành công/thất bại, p50/p95/p99 và bằng chứng raw. Không suy luận p95 production từ laptop.

| ASR | Thí nghiệm | Response measure | Kết quả hiện tại |
|---|---|---|---|
| S4 | `python tests/integration.py`; role A thử CONNECT vào DB B | 0 truy cập chéo; A không đọc B | PASS: API B đọc receipt/autosave A trả 404; PostgreSQL từ chối CONNECT cho role A vào DB B |
| S1 | `python src/loadtest/load.py --users 8000 --seconds 60 --output results/load-8000-60s-async.json` | p95 < 1s; error < 0,1%; 0 receipt mất | PASS trong phạm vi test: 8.000/8.000 bắt đầu trong 60s, 8.000 HTTP 202, 0 lỗi, p95 266,65ms; 8.100 receipt có UUID trong DB = 100 smoke + 8.000 final |
| S3 | `python tests/restart.py` | 0 receipt đã ack mất | PASS: API restart sau ack, receipt đọc lại được và B không thấy; chưa fault injection ngay trong giờ thi nhiều client |
| S5/S6 | `python tests/integration.py` | Không restart core; điểm đúng | PASS: A=76, B=78 với cùng điểm thành phần; QR bật cho A tại runtime, B vẫn disabled |
| S2 | Mở `/static/exam-demo.html`, Browser DevTools offline 60s, kiểm IndexedDB và retry | Mất ≤30s thao tác | PASS cho một bản nháp: offline 60s, nội dung vẫn ở IndexedDB và server nhận đúng sau reconnect; chưa đo crash/browser quota hoặc nhiều câu |

## Kết quả đo thật ngày 07/11/2026

Máy Windows: Intel Core i5-8365U 4 core/8 luồng, RAM 16,99 GB; Docker Desktop Engine 29.9.2 cấp khoảng 8,23 GB và 8 vCPU. Một container API (Gunicorn 4 workers × 8 threads), một PostgreSQL 16, một exam worker, một QR process. Test gửi payload JSON nhỏ gồm một câu trả lời tới tenant A qua HTTP localhost, không có TLS, SSO, video hoặc autosave nền đồng thời.

| Run | Generator | Bắt đầu trong 60s | Thành công/lỗi | p50 | p95 | p99 | Raw |
|---|---|---:|---:|---:|---:|---:|---|
| Baseline | Thread pool, kết nối DB/request | Không ghi | 8.000/0 | 5.409,54ms | 7.077,98ms | 51.524,27ms | [raw](../results/load-8000-60s.json) |
| Pool | Thread pool, connection pool | Không ghi | 8.000/0 | 2.140,76ms | 4.598,83ms | 53.514,12ms | [raw](../results/load-8000-60s-pooled.json) |
| Kiểm tra lịch phát | Thread pool, connection pool | **1.477/8.000** | 8.000/0 | 2.214,17ms | 5.654,90ms | 51.407,20ms | [raw](../results/load-8000-60s-window.json) |
| Final | Async aiohttp, connection pool | **8.000/8.000** (request cuối bắt đầu 59,994s) | **8.000/0** | 29,90ms | **266,65ms** | 549,30ms | [raw](../results/load-8000-60s-async.json) |

Ba run thread pool không đạt lịch phát 8K/phút; số p95 của chúng không được dùng để đánh giá S1 hay quy toàn bộ cải thiện cho connection pool. Run final có lịch phát hợp lệ và đạt p95 trên máy local. PostgreSQL trả `processed|8100` cho 100 smoke + 8.000 request UUID, chứng tỏ worker đã xử lý các receipt sau ack. Run final chưa chứng minh 0 mất bài trong mọi tình huống sự cố.

Browser test bằng Playwright trên demo: đặt offline, nhập `offline 60 seconds retained`, đợi 60 giây rồi bật online; trạng thái đổi từ “nháp vẫn ở thiết bị” sang “Nháp đã đồng bộ lên server”, GET autosave trả đúng chuỗi và sequence 2. Đây là bằng chứng về một thao tác lưu trong mất mạng 60 giây; chưa chứng minh mọi loại thao tác mất tối đa 30 giây hay khả năng sống sót khi ổ đĩa trình duyệt lỗi.

## Diễn giải phép đo

Script load xuất JSON raw với latency và thời điểm bắt đầu mỗi request, cùng aggregate p95. 8.000 request được rải trong 60 giây; có thể chạy thêm kịch bản đồng loạt 8.000 trong 5 giây để tìm bottleneck, nhưng tiêu chí đề tài là 8.000/phút. Nếu chạy trên hạ tầng khác mà p95 không đạt, kiểm CPU, IOPS, pool, log và retry; giữ nguyên số liệu.

## Giới hạn bằng chứng

Unit test công thức và route không chứng minh an toàn trước lỗi vận hành. Test cross-tenant chỉ chứng minh hai tenant và API path đã thử. Production cần penetration test, backup restore, plugin sandbox và key rotation. S1 cần kiểm trên hạ tầng target với TLS/SSO và autosave nền đồng thời. S2 cần kiểm nhiều thao tác, browser crash và quota. S7 cost cần bill cloud thực hoặc mô hình giá có giả định minh bạch.
