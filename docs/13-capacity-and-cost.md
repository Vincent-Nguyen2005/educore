# Ước lượng tải và chi phí — giả định cần xác nhận

## Tải giờ thi

- 8.000 nộp bài / 60 giây = khoảng **134 submission/s** trung bình. Nếu dồn vào 5 giây, mức cần khảo sát là 1.600/s; đây là stress scenario nội bộ, không phải con số đề bài.
- 8.000 sinh viên autosave mỗi 5 giây = **1.600 autosave/s** trước debounce/jitter. Đây có thể là tải ghi lớn hơn nộp bài. Client nên jitter lịch gửi, chỉ gửi phần thay đổi và dùng sequence để giữ bản mới nhất.
- Payload giả định 2 KB/receipt: 8.000 lượt tương đương 16 MB dữ liệu thô trong 1 phút, chưa kể WAL, index, replica và metadata. Cần đo payload thật theo số câu và media; video đi object storage/CDN, không qua DB receipt.
- Pre-scale API, pool và DB IOPS theo lịch thi trước ít nhất 30 phút; dùng per-tenant quota và cảnh báo queue lag/p95. Nếu lịch đổi đột ngột, autoscale dựa CPU, pool wait và backlog; client tiếp tục giữ IndexedDB khi API trả lỗi.

## Mô hình chi phí để kiểm BG3/S7

Ký hiệu `C = C_shared_compute + Σ(C_db_tenant + C_storage_tenant + C_egress_tenant) + C_ops`. Với shared cluster, tenant nhỏ tránh một cụm DB và một deployment riêng, nhưng mỗi DB thêm connection, backup, migration và storage tối thiểu. Để chứng minh S7 (thêm tenant nhỏ tăng ≤5%), cần bảng giá cloud thực, mức dùng baseline, cấu hình HA và bill sau onboarding. Hiện chưa có dữ liệu đó, nên S7 và BG3 **chưa được xác nhận**. DB-per-tenant có thể khiến S7 không đạt nếu mỗi tenant tạo pool/backup riêng quá lớn; giới hạn pool, connection proxy và tiering là biện pháp cần đo.

## Ngưỡng thay đổi kiến trúc

Nếu 1.600 autosave/s làm DB WAL hoặc pool nghẽn, ưu tiên batch/coalesce và tách autosave store/partition trước khi chia toàn core thành microservices. Nếu 50 DB vượt giới hạn vận hành của một cụm, phân nhóm tenant sang nhiều cluster và migration canary. Nếu tenant lớn gây noisy neighbor, chuyển tenant đó sang cluster riêng, giữ API contract.
