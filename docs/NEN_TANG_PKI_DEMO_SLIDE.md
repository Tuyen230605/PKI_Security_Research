# Lộ trình hiểu PKI, chuẩn bị demo và slide

Tài liệu này là bản dẫn đường cho chương 1–4 của báo cáo. Đọc chương 1 để nắm câu hỏi nghiên cứu, chương 2 để phân biệt vai trò mật mã, chương 3 để hiểu ai phát hành và vận hành chứng thư, chương 4 để biết client chấp nhận chứng thư trong điều kiện nào. Phần demo ở chương 6 chỉ có ý nghĩa khi giải thích được các điều kiện ấy.

## Sáu điều phải tự giải thích được

1. **Vì sao public key cần chứng thực?** Kẻ đứng giữa có thể thay khóa công khai; một chữ ký hợp lệ trên dữ liệu về sau không giúp gì nếu ta gắn nhầm khóa với danh tính. Xem chương 1.
2. **Ba khóa/chữ ký khác nhau là gì?** Khóa CA ký chứng thư; khóa bí mật của server ký CertificateVerify trong phiên TLS; khóa phiên đối xứng bảo vệ dữ liệu ứng dụng. Xem chương 2. Lệnh xác minh chứng thư hiện tại chưa chạy toàn bộ bắt tay TLS.
3. **Niềm tin bắt đầu từ đâu?** Trust anchor do client cấu hình; Root tự ký không tự được tin. Intermediate được cung cấp để dựng đường dẫn và phải được xác minh. Xem chương 3–4.
4. **Chứng thư chứa gì?** Đọc Issuer, Subject, Validity, SAN, Basic Constraints, KU và EKU. Tên DNS để so khớp nằm ở SAN; CN trong Subject không phải căn cứ theo quy tắc nhận dạng dịch vụ của RFC 9525.
5. **PASS cần các điều kiện nào?** Có đường dẫn tới Root được tin, chữ ký và thời hạn hợp lệ, CA/leaf được dùng đúng mục đích, SAN khớp tên yêu cầu, trạng thái thu hồi đạt theo chính sách đã bật. Phải nêu rõ tùy chọn kiểm tra.
6. **Điểm yếu ngoài thuật toán là gì?** CA có thể xác minh tên sai, khóa có thể lộ, client có thể bỏ kiểm tra hostname hoặc CRL, nguồn trạng thái có thể không sẵn có. Lab không có RA, HSM hay OCSP nên không kết luận các cơ chế này đã được kiểm chứng.

## Những gì demo đã triển khai

| Thành phần/bước | File hoặc lệnh | Cần giải thích |
|---|---|---|
| Root CA | demo/scripts/setup_lab.sh; root/root.crt | Chứng thư tự ký; chỉ là trust anchor khi client cấp rõ bằng -CAfile. |
| Intermediate CA | intermediate/ca.crt, ca.key, openssl.cnf | Root ký Intermediate; Intermediate được phép ký leaf, không được cấp thêm CA con theo pathlen:0. |
| Ba leaf | server-a, server-b, client-only | SAN và EKU do cấu hình CA cấp; client-only dùng để thử sai mục đích TLS server. |
| Thu hồi | intermediate/ca.crl | Server A bị thu hồi; server B không bị thu hồi; client phải bật -crl_check. |
| Bộ kiểm thử | demo/scripts/run_tests.sh; results.tsv | Mười ca gồm PASS/FAIL, exit code và thông báo; script xác nhận cả nguyên nhân lỗi dự kiến. |
| TLS tùy chọn | openssl s_server và curl trong demo/README.md | Minh họa kết nối HTTPS riêng, không tự chứng minh kiểm tra CRL/OCSP. |

Chạy từ thư mục gốc:

    make demo-test
    openssl version
    openssl x509 -in demo/out/servers/server-a.crt -noout -subject -issuer -dates -ext subjectAltName
    cat demo/out/results.tsv

Không đưa khóa bí mật hoặc cả thư mục demo/out vào slide/repository. Nếu muốn chụp bằng chứng, chụp chứng thư công khai, câu lệnh xác minh, exit code và dòng lỗi chính.

## Chọn ca để trình bày trực tiếp

| Ca | Cặp so sánh nên nói | Kết luận vừa đủ |
|---|---|---|
| TC01 và TC04 | Cùng leaf server A, đổi hostname sang wrong.test. | Chữ ký/chuỗi vẫn như cũ nhưng sai danh tính dịch vụ thì bị từ chối. |
| TC01 và TC07 | Cùng leaf server A, chỉ TC07 bật CRL. | Kết quả trạng thái phụ thuộc việc client có kiểm tra CRL theo chính sách. |
| TC07 và TC09 | Cùng Root, Intermediate và CRL, đổi leaf A sang B. | Thu hồi áp dụng cho một serial cụ thể; B vẫn PASS. |
| TC06 và TC10 | Một ca thiếu Intermediate, một ca do Root khác cấp. | Phải phân biệt không dựng được chuỗi với chuỗi không dẫn đến Root được tin. |
| TC03 | Dùng -attime sau notAfter. | Đây là mô phỏng thời điểm tương lai, không phải chờ chứng thư hết hạn thật. |

TC05 cho thấy sửa chữ ký làm FAIL; TC08 cho thấy clientAuth không dùng như serverAuth. Nếu chỉ có vài phút, ưu tiên TC01, TC04, TC07, TC10 và mở bảng kết quả mười ca. Luôn đọc tùy chọn của lệnh trước khi tuyên bố OpenSSL đã kiểm tra gì.

## Ranh giới giữa kiến thức, demo và slide

- **Cần biết nhưng chưa hiện thực:** RA/xác minh quyền sở hữu DNS, CP/CPS thực tế, HSM, OCSP responder, tự động cấp lại, policy trình duyệt/Web PKI công cộng. Trình bày ngắn ở slide giới hạn hoặc hướng phát triển; không diễn giải chúng như kết quả lab.
- **Có trong báo cáo và demo:** Root, Intermediate, leaf, CSR, extension, trust anchor cấu hình, dựng chuỗi, hostname, purpose, thời gian và CRL.
- **Cần bổ sung trước khi chốt chương 6:** chạy lại lab trên môi trường cuối, ghi ngày và phiên bản OpenSSL, kiểm tra toàn bộ kết quả, đưa bảng đã lọc bí mật vào báo cáo. Các chương 5–8 hiện còn là khung nội dung nên không dùng làm kết luận hoàn thành đề tài.

## Dàn ý slide và quy tắc trình bày

Xem bảng từng trang trong [slides/README.md](../slides/README.md). Mỗi slide chỉ trả lời một câu hỏi: vấn đề, cơ chế, điều kiện, bằng chứng hoặc giới hạn. Dùng một sơ đồ CA, một sơ đồ luồng xác minh, một bảng ca thử rút gọn; không dán nguyên bảng trường X.509 hoặc màn hình lệnh quá dài. Trên slide kết quả, hiện cả lệnh/tùy chọn chính và thông báo cho ít nhất một PASS và một FAIL. Kết luận cuối phải có điều kiện: chữ ký đúng chưa đủ; client phải xác minh đúng đường dẫn, danh tính, mục đích, thời điểm và trạng thái theo chính sách.
