# Hạ tầng khóa công khai (PKI): kiến trúc, cơ chế xác thực chứng thư X.509 và ứng dụng

Dự án tiểu luận môn **Mật mã và An toàn thông tin**, mã lớp **2627I_INT3230_2**, giảng viên **Lê Thị Hợi**. Thành viên: **Đoàn Văn Tuyền (23020151), Vũ Minh Quân (23020142), Nguyễn Chi Tú (23020148)**. Câu hỏi xuyên suốt: **chữ ký mật mã hợp lệ của một chứng thư có đủ để client tin cậy và chấp nhận chứng thư đó không?** Báo cáo trình bày PKI ở hai tầng: tổng quan (cơ sở mật mã, kiến trúc và mô hình tổ chức, vòng đời chứng thư, phân tích bảo mật và sự cố thực tế, so sánh mô hình tin cậy và cơ chế thu hồi, ứng dụng và xu hướng như chữ ký số tại Việt Nam, Certificate Transparency, ACME, hậu lượng tử); và đi sâu vào trường hợp xác thực máy chủ TLS bằng chứng thư X.509, kiểm chứng bằng CA phân cấp trong môi trường lab nội bộ.

Hai tài liệu gốc ở thư mục này là [Introduction.docx](Introduction.docx) (đề cương nghiên cứu) và [introduction2.docx](introduction2.docx) (bộ sản phẩm nên nộp). Đây là đề xuất ban đầu; yêu cầu chính thức của giảng viên, thời hạn, độ dài và mẫu trình bày cần được nhóm xác nhận trước khi chốt báo cáo.

## Bắt đầu trong 5 phút

1. Đọc [kế hoạch thực hiện](docs/HOAN_THANH_DU_AN.md) và [lộ trình học, demo, slide](docs/NEN_TANG_PKI_DEMO_SLIDE.md).
2. Cài LaTeX theo [hướng dẫn workspace](docs/SETUP_LATEX.md); chạy `make report`. PDF nằm tại `build/main.pdf`.
3. Chạy `make demo-test` để tạo CA thử nghiệm và ghi kết quả ở `demo/out/results.tsv`. Đọc [hướng dẫn demo](demo/README.md) trước khi dùng kết quả trong báo cáo.
4. Đọc chương 1–4 trong nguồn LaTeX để nắm nền tảng; đối chiếu câu lệnh demo với chương 4 và nguồn tham khảo.
5. Theo [checklist nộp bài](docs/CHECKLIST_NOP_BAI.md) để hoàn thiện PDF, slide và bằng chứng thực nghiệm.

## Cấu trúc

```text
.
├── Introduction.docx, introduction2.docx  # Tài liệu đề bài gốc
├── README.md, Makefile, .gitignore
├── docs/
│   ├── SETUP_LATEX.md          # Cài LaTeX và dựng báo cáo
│   ├── HOAN_THANH_DU_AN.md     # Tiến độ và tiêu chí hoàn thành
│   ├── CHECKLIST_NOP_BAI.md    # Kiểm tra trước khi nộp
│   └── NEN_TANG_PKI_DEMO_SLIDE.md # Lộ trình học và trình bày
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
| Báo cáo PDF | Chương 1–5 và 7 đã viết; chương 6 chưa đưa kết quả quan sát; kết luận và tóm tắt còn là khung | Hoàn thiện phần phân tích, kết quả thật, kết luận và trích dẫn |
| Demo PKI | Lab OpenSSL và test tự động | Quay/chụp bằng chứng, giải thích từng trường hợp |
| Slide | Kịch bản 12 trang | File trình chiếu có sơ đồ và kết quả |
| Repository | Cấu trúc và hướng dẫn chạy | Người khác tái lập được trên máy sạch |
| Biểu đồ/benchmark, dashboard | Chưa triển khai | Tùy thời gian, chỉ thêm sau phần cốt lõi |

**Lưu ý:** `demo/out/` chứa khóa bí mật thử nghiệm. Chỉ dùng cho lab; không dùng các khóa/chứng thư này trong hệ thống thật và không commit thư mục đó.
