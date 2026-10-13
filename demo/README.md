# Demo PKI: Root CA → Intermediate CA → server

Lab này chỉ dùng chứng thư và khóa tự tạo ở `demo/out/`; không kết nối Internet, không cần Nginx. Nó kiểm tra **xác minh chứng thư bằng OpenSSL**, chưa mô phỏng đầy đủ hành vi trình duyệt hoặc toàn bộ phiên TLS. Theo đề cương, có thể bổ sung Nginx/curl và OCSP ở vòng sau nếu còn thời gian.

## Chạy từ đầu

Yêu cầu: Bash, OpenSSL 3.x, Python 3, `make` (tùy chọn). Tại thư mục gốc:

```bash
make demo-test
# hoặc:
bash demo/scripts/setup_lab.sh
bash demo/scripts/run_tests.sh
```

Script tạo Root CA, Intermediate CA, chứng thư `server-a.test`, `server-b.test`, chứng thư chỉ có `clientAuth`, một chứng thư tự ký không tin cậy và một chuỗi do CA khác cấp. Nó sửa một byte chữ ký cho TC05, thu hồi `server-a.test` và phát hành CRL. `results.tsv` gồm kỳ vọng, kết quả quan sát, exit code và thông báo. Script dừng lỗi nếu trạng thái hoặc nguyên nhân lỗi khác kỳ vọng.

`setup_lab.sh` giữ nguyên lab nếu đã có `demo/out/.lab_marker`. Muốn tạo bộ khóa/chứng thư mới, **kiểm tra rằng thư mục chỉ chứa output lab**, rồi xóa `demo/out/` và chạy lại. Toàn bộ khóa trong đây là khóa thử nghiệm, không được công bố.

## Mười ca kiểm thử

| ID | Thay đổi/điều kiện | Kỳ vọng | Tùy chọn quan trọng |
|---|---|---|---|
| TC01 | Chứng thư server A hợp lệ; CA tin cậy | PASS | `-CAfile`, `-untrusted`, `-purpose sslserver`, `-verify_hostname` |
| TC02 | Chứng thư server tự ký, không thuộc trust store | FAIL | `-CAfile` trỏ CA lab |
| TC03 | Xác minh tại thời điểm 40 ngày sau ngày tạo; leaf 30 ngày | FAIL | `-attime` (giả lập thời điểm tương lai) |
| TC04 | SAN không khớp hostname yêu cầu | FAIL | `-verify_hostname wrong.test` |
| TC05 | Sửa một bit của chữ ký chứng thư | FAIL | Kiểm tra chữ ký trong chain |
| TC06 | Không cấp Intermediate cho OpenSSL | FAIL | Bỏ `-untrusted` |
| TC07 | Server A đã bị thu hồi, có CRL | FAIL | `-CRLfile ... -crl_check` |
| TC08 | Chứng thư chỉ có EKU `clientAuth` | FAIL | `-purpose sslserver` |
| TC09 | Server B chưa thu hồi, CRL đã bật | PASS | `-CRLfile ... -crl_check` |
| TC10 | Server do CA khác cấp; CA đó không phải trust anchor | FAIL | `-CAfile` vẫn trỏ Root CA chính |

TC01 có thể PASS dù server A đã bị thu hồi vì lệnh đó **không bật kiểm tra CRL**; so sánh với TC07 để giải thích vai trò của chính sách xác minh. TC03 không phải chứng thư phát hành đã hết hạn tại ngày hiện tại: lab chủ động đặt thời điểm xác minh trong tương lai. TC02 và TC10 cùng kiểm tra vấn đề tin cậy nhưng TC02 là leaf tự ký, TC10 là leaf được CA khác ký đúng.

## Tùy chọn: minh họa HTTPS thật

Nếu muốn nối bước xác minh chứng thư với một phiên TLS, mở terminal thứ nhất:

```bash
openssl s_server -accept 8443 -www \
  -cert demo/out/servers/server-b.crt \
  -key demo/out/servers/server-b.key \
  -cert_chain demo/out/intermediate/ca.crt
```

Ở terminal thứ hai, dùng CA lab làm trust anchor và ánh xạ tên DNS thử nghiệm về localhost:

```bash
curl --noproxy '*' --cacert demo/out/root/root.crt \
  --resolve server-b.test:8443:127.0.0.1 \
  https://server-b.test:8443/
```

Lệnh `curl` này minh họa hostname và chain trên kết nối HTTPS. Nó không tự chứng minh trình duyệt hay `curl` đã kiểm tra CRL; phần đó được thử riêng bằng `openssl verify -crl_check`. Dừng server bằng `Ctrl+C`.

## Kịch bản trình bày 3–5 phút

1. Mở sơ đồ CA phân cấp trong slide; dùng `openssl x509 -in demo/out/servers/server-a.crt -noout -subject -issuer -dates -ext subjectAltName` để chỉ ra Subject, Issuer, SAN và thời hạn.
2. Chạy `make demo-test`; cho thấy TC01 PASS và TC04 FAIL dù cùng một chứng thư được ký đúng.
3. Cho thấy TC07 FAIL khi bật CRL, trong khi TC01 PASS vì không kiểm tra trạng thái. Giải thích chính xác điều kiện nào đã đổi.
4. Cho thấy TC10 FAIL vì trust anchor được cấu hình là Root CA khác. Kết luận: chữ ký hợp lệ là một bước, còn quyết định tin cậy phụ thuộc bối cảnh và chính sách của client.
5. Mở `demo/out/results.tsv`; ghi rõ giới hạn: private CA, OpenSSL CLI, chưa có TLS server thực/OCSP.

Khi lấy bằng chứng cho báo cáo, chụp dòng lệnh, exit code và thông báo của từng ca; chép bảng kết quả đã lọc sang `report/tables/`. Không đưa private key hoặc toàn bộ `demo/out/` vào bài nộp hay repository.
