# Nghiên cứu PKI và xác thực chứng thư X.509

Dự án tiểu luận môn **Mật mã và An toàn thông tin**. Câu hỏi xuyên suốt: **chữ ký mật mã hợp lệ của một chứng thư có đủ để client tin cậy và chấp nhận chứng thư đó không?** Nhóm nghiên cứu kiến trúc PKI, chứng thư X.509, chuỗi tin cậy và thu hồi; sau đó kiểm chứng bằng CA phân cấp trong môi trường lab nội bộ.

Hai tài liệu gốc ở thư mục này là [Introduction.docx](Introduction.docx) (đề cương nghiên cứu) và [introduction2.docx](introduction2.docx) (bộ sản phẩm nên nộp). Đây là đề xuất ban đầu; yêu cầu chính thức của giảng viên, thời hạn, độ dài và mẫu trình bày cần được nhóm xác nhận trước khi chốt báo cáo.

## Bắt đầu trong 5 phút

1. Đọc [kế hoạch thực hiện](docs/HOAN_THANH_DU_AN.md) và chia việc cho ba thành viên.
2. Cài LaTeX theo [hướng dẫn workspace](docs/SETUP_LATEX.md); chạy `make report`. PDF nằm tại `build/main.pdf`.
3. Chạy `make demo-test` để tạo CA thử nghiệm và ghi kết quả ở `demo/out/results.tsv`. Đọc [hướng dẫn demo](demo/README.md) trước khi dùng kết quả trong báo cáo.
4. Thay thông tin nhóm ở `report/main.tex`; viết từng chương trong `report/chapters/`; thêm nguồn vào `report/references.bib`.
5. Theo [checklist nộp bài](docs/CHECKLIST_NOP_BAI.md) để hoàn thiện PDF, slide và bằng chứng thực nghiệm.

## Cấu trúc

```text
.
├── Introduction.docx, introduction2.docx  # Tài liệu đề bài gốc
├── README.md, Makefile, .gitignore
├── docs/
│   ├── SETUP_LATEX.md          # Cài đặt chung cho hai thành viên còn lại
│   ├── HOAN_THANH_DU_AN.md     # Tiến độ, chia việc, tiêu chí hoàn thành
│   └── CHECKLIST_NOP_BAI.md    # Kiểm tra trước khi nộp
├── report/
│   ├── main.tex, preamble.tex, references.bib
│   ├── chapters/              # Bảy chương và kết luận
│   ├── figures/               # Hình gốc do nhóm tạo
│   └── tables/                # Bảng kết quả đã đối chiếu
├── demo/
│   ├── README.md              # Kịch bản trình bày và cách đọc test
│   └── scripts/               # Tạo CA, cấp chứng thư, kiểm thử
├── slides/README.md           # Cấu trúc 10–12 slide
└── build/, demo/out/           # Sinh tự động, không đưa lên repository
```

## Phạm vi sản phẩm

| Sản phẩm | Trạng thái ban đầu | Đích hoàn thành |
|---|---|---|
| Báo cáo PDF | Bộ khung LaTeX biên dịch được | Nội dung 7 chương, kết quả thật, trích dẫn đầy đủ |
| Demo PKI | Lab OpenSSL và test tự động | Quay/chụp bằng chứng, giải thích từng trường hợp |
| Slide | Dàn ý | 10–12 slide có sơ đồ và kết quả |
| Repository | Cấu trúc và hướng dẫn chạy | Người khác tái lập được trên máy sạch |
| Biểu đồ/benchmark, dashboard | Chưa triển khai | Tùy thời gian, chỉ thêm sau phần cốt lõi |

**Lưu ý:** `demo/out/` chứa khóa bí mật thử nghiệm. Chỉ dùng cho lab; không dùng các khóa/chứng thư này trong hệ thống thật và không commit thư mục đó.
