# Kịch bản slide 12 trang: từ nền tảng đến bằng chứng

Slide là bản trình bày ngắn của báo cáo, không chép nguyên chương 1–4. Cần có câu hỏi, một sơ đồ luồng và các kết quả thật lấy từ lần chạy demo cuối. Thông tin bìa: môn Mật mã và An toàn thông tin; lớp 2627I_INT3230_2; giảng viên Lê Thị Hợi; Đoàn Văn Tuyền (23020151), Vũ Minh Quân (23020142), Nguyễn Chi Tú (23020148). Không ghi phân công theo thành viên.

| Trang | Tiêu đề/câu hỏi | Nội dung nên hiện | Nguồn/bằng chứng |
|---|---|---|---|
| 1 | Chữ ký đúng đã đủ tin chưa? | Tên đề tài, thành viên, câu hỏi trung tâm. | Chương 1. |
| 2 | Vì sao cần PKI? | Alice nhận public key của server, kẻ đứng giữa có thể thay khóa; cần liên kết tên và khóa. | Chương 1; sơ đồ tự vẽ. |
| 3 | Mật mã làm các việc khác nhau | CA ký chứng thư; server ký transcript TLS; ECDHE/khóa phiên và mã hóa đối xứng bảo vệ dữ liệu. | Chương 2; RFC 8446. |
| 4 | Ai vận hành niềm tin? | Sơ đồ Root → Intermediate → leaf; client cấu hình Root làm trust anchor; RA và dịch vụ trạng thái ở bên cạnh. | Chương 3; phân biệt thành phần trong lab. |
| 5 | Chứng thư nói gì? | Một đoạn xuất thông tin thật: Issuer, Subject, Validity, SAN, Basic Constraints, KU/EKU. | Lệnh openssl x509 -text của server A; chương 4. |
| 6 | Client chấp nhận thế nào? | Luồng dựng chuỗi → kiểm tra chữ ký/thời gian/ràng buộc → hostname → trạng thái theo chính sách → PASS/FAIL. | Chương 4; RFC 5280, RFC 9525. |
| 7 | Lab được dựng ra sao? | Root và Intermediate ký các leaf; server A bị thu hồi, server B không; các thành phần chưa có: RA, HSM, OCSP. | demo/scripts/setup_lab.sh. |
| 8 | Thử những điều kiện nào? | Bảng rút gọn mười ca nhóm theo trust/chain, thời gian, tên, chữ ký, EKU, CRL. | run_tests.sh và chương 6. |
| 9 | Demo trực tiếp | Chạy make demo-test; mở TC01, TC04, TC07, TC10 với tùy chọn và thông báo chính. | Kết quả lần chạy cuối, có exit code. |
| 10 | Dữ liệu cho biết gì? | TC01 và TC07 khác nhau do CRL được bật; TC04 FAIL do hostname; TC10 FAIL do trust anchor. | results.tsv đã đối chiếu. |
| 11 | Giới hạn và rủi ro | Lab private CA/OpenSSL CLI; không kiểm chứng chính sách trình duyệt, OCSP, RA hoặc độ an toàn vận hành khóa. | Chương 3–6. |
| 12 | Kết luận | Chữ ký đúng là một phép kiểm; quyết định chấp nhận còn cần đường dẫn tin cậy, tên, thời gian, mục đích và trạng thái theo chính sách. | RQ1–RQ4, H1–H2; không tuyên bố H3 đã được đo. |

Thời lượng gợi ý: 1 phút cho trang 1–3, 2 phút cho trang 4–6, 2–3 phút cho trang 7–10, 1 phút cho trang 11–12. Nếu không chạy demo trực tiếp được, dùng ảnh/log dự phòng có ngày chạy, phiên bản OpenSSL và tùy chọn xác minh rõ ràng. Không đưa private key lên slide.

Trước khi làm file PPTX/PDF cuối, đọc lại [lộ trình nền tảng](../docs/NEN_TANG_PKI_DEMO_SLIDE.md) và xác nhận bảng kết quả thực nghiệm trong chương 6 đã được cập nhật từ lần chạy cuối.
