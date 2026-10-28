# Checklist trước khi nộp và trình bày

## Báo cáo

- [ ] Xác nhận format của giảng viên; kiểm tra trường/khoa nếu mẫu yêu cầu, tên và mã số ba thành viên, mã lớp, giảng viên, ngày nộp.
- [ ] Bảy chương có nội dung thật; tóm tắt và kết luận phản ánh kết quả đã đo.
- [ ] RQ1–RQ5 và H1–H2 được trả lời bằng lập luận/bằng chứng tương ứng; H3 có phép đo riêng hoặc ghi rõ chưa kiểm chứng.
- [ ] Có sơ đồ PKI, vòng đời chứng thư, luồng validation và mô hình lab; mọi hình/bảng có số, chú thích và nguồn.
- [ ] Chương 6 có bảng TC gồm **kỳ vọng và quan sát riêng**, lệnh/tùy chọn xác minh, phiên bản phần mềm và giới hạn.
- [ ] Tài liệu tham khảo dùng thống nhất một kiểu; mọi khẳng định chuẩn giao thức có nguồn chính thức.
- [ ] `make report` thành công; đọc lại PDF để phát hiện lỗi font tiếng Việt, tràn trang, link và bảng.

## Demo và repository

- [ ] `make demo-test` chạy từ trạng thái sạch; lưu số liệu đã lọc khóa bí mật.
- [ ] Trình bày được Root CA → Intermediate CA → server, một ca PASS và các ca FAIL do hostname/trust/CRL.
- [ ] Giải thích rằng chữ ký hợp lệ vẫn có thể bị từ chối bởi điều kiện khác.
- [ ] Không commit `demo/out/`, private key, khóa thật hay file chứa bí mật.
- [ ] README đủ để thành viên khác tái lập; link file không hỏng.

## Thuyết trình

- [ ] Slide 10–12 trang, nội dung theo [dàn ý](../slides/README.md).
- [ ] Chạy thử demo ngoại tuyến trước buổi trình bày; chuẩn bị ảnh/log dự phòng và PDF slide.
- [ ] Người thuyết trình trả lời được: trust anchor đến từ đâu, vì sao SAN/CRL cần kiểm tra, giới hạn của lab.
