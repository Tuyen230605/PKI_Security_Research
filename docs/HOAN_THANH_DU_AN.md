# Lộ trình hoàn thành dự án

## Đầu ra và tiêu chí hoàn thành

Bộ nộp tối thiểu: (1) PDF báo cáo, (2) slide 10–12 trang, (3) demo PKI hoạt động và log/bảng kết quả, (4) repository tái lập được. Dự kiến báo cáo 28–36 trang nội dung theo đề cương gốc, điều chỉnh theo yêu cầu giảng viên.

| Giai đoạn | Việc làm | Kết quả có thể kiểm tra |
|---|---|---|
| 0. Chốt yêu cầu | Xác nhận mẫu báo cáo, số trang, hạn nộp, quy cách trích dẫn | Kiểm tra bìa và format cuối |
| 1. Nền tảng | Đọc RFC 5280; đối chiếu RQ1–RQ4, giả thuyết H1–H3; phác sơ đồ Root → Intermediate → Server | Chương 1–4 và nguồn được đối chiếu với demo |
| 2. Cơ chế | Viết chương 2–4: mật mã, kiến trúc, X.509, path validation, CRL/OCSP, TLS | Bản nháp kỹ thuật có trích dẫn và sơ đồ |
| 3. Lab | Chạy `make demo-test`; đối chiếu từng TC với lệnh OpenSSL, lưu phiên bản công cụ và output | Bảng test thật, log, hình minh họa |
| 4. Phân tích | Viết chương 5–6 từ kết quả, nêu điều kiện kiểm tra, giới hạn OpenSSL/private PKI | Kết luận cho từng giả thuyết, không suy diễn quá dữ liệu |
| 5. Hoàn thiện | Viết chương 1, 7, tóm tắt và kết luận sau khi có kết quả; làm slide | Báo cáo thống nhất, slide tập trung vào câu hỏi và bằng chứng |
| 6. Review | Build PDF trên ít nhất một máy khác; chạy demo từ thư mục sạch; tập thuyết trình | Hoàn tất [checklist](CHECKLIST_NOP_BAI.md) |

## Quy trình hoàn thiện

Thực hiện tuần tự theo các giai đoạn ở trên; không phân chia chương hoặc demo theo thành viên. Trước khi viết chương 5–7, đối chiếu từng nhận định thực nghiệm với lệnh và kết quả trong chương 6. [Lộ trình học, demo và slide](NEN_TANG_PKI_DEMO_SLIDE.md) nêu rõ kiến thức cần nắm và bằng chứng cần chuẩn bị.

## Nội dung từng chương

1. **Vấn đề nghiên cứu:** bài toán thay khóa công khai, câu hỏi RQ1–RQ4, phạm vi CA phân cấp/TLS.
2. **Cơ sở mật mã:** khóa công khai, chữ ký, hash; phân biệt ký chứng thư, bắt tay TLS và mã hóa dữ liệu.
3. **Kiến trúc:** CA/RA/repository/relying party, vòng đời chứng thư, chính sách CP/CPS.
4. **X.509:** trường/extension, trust anchor, path validation, hostname, CRL/OCSP, giới hạn xác minh.
5. **Bảo mật:** CA bị chiếm, cấp sai, lộ khóa, lỗi kiểm tra; so sánh mô hình tin cậy và thu hồi.
6. **Thực nghiệm:** môi trường, lệnh, test cases, kết quả thật, giải thích, giới hạn.
7. **Ứng dụng/hướng phát triển:** CT, ACME, hậu lượng tử ở mức liên quan trực tiếp; kiểm tra lại các mốc/quy định trước khi viết bản cuối.

## Cách ghi nhận thực nghiệm

- Lưu `openssl version`, hệ điều hành, ngày chạy, lệnh và `results.tsv` cùng ảnh/log cần thiết. `demo/out/` bị bỏ qua bởi Git vì có private key; chỉ đưa **bảng đã lọc bí mật** và trích đoạn log cần thiết vào `report/tables/` hoặc phụ lục.
- Với mỗi TC, ghi: điều kiện, câu lệnh, exit code, thông báo chính, kỳ vọng, quan sát, giải thích. TC03 trong lab dùng thời điểm kiểm tra tương lai để chứng minh điều kiện hết hạn; đừng mô tả là đã chờ chứng thư hết hạn thật.
- OpenSSL `verify` không áp dụng mọi chính sách trình duyệt. Nêu chính xác tùy chọn như `-verify_hostname`, `-purpose sslserver`, `-crl_check_all`, `-attime` thay vì nói “client tự kiểm tra hết”.
- Lab cốt lõi kiểm chứng H1 và các điều kiện của H2. H3 về chi phí/giới hạn giữa nhiều cơ chế cần phép đo hoặc phân tích so sánh riêng; nếu không thực hiện, ghi rõ H3 chưa được kiểm chứng thực nghiệm và chỉ thảo luận bằng tài liệu.
- Benchmark RSA/ECDSA, dashboard và mô phỏng CA cấp sai là phần mở rộng. Chỉ làm khi báo cáo và 7 test chính đã đạt; ghi phương pháp đo riêng.
