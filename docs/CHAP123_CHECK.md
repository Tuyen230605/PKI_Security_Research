# Kết Quả Đối Chiếu Nguồn và Nhận Xét Kiểm Tra Chương 1, 2, 3

---

## A. Kết quả đối chiếu nguồn

### 1. Baseline Requirements (BR) của CA/Browser Forum
- **Phiên bản & Thời gian**: Phiên bản mới nhất là 2.3.1 (ngày 04/10/2026), nên mục [4] trong tài liệu tham khảo đang ghi "2023" cần sửa lại cho đúng phiên bản sử dụng.  
  *Nguồn tham khảo*: [CA/Browser Forum Baseline Requirements](https://cabforum.org/working-groups/server/baseline-requirements/requirements/)
- **Yêu cầu FIPS (Mục 3.3.2 - đang sai)**:
  - Theo trích đoạn mục 6.2.7 của BR, khóa CA phải được lưu trữ và bảo vệ trong thiết bị đạt tối thiểu **FIPS 140-2 Level 3** hoặc **FIPS 140-3 Level 3**, hoặc **Common Criteria EAL 4+**.
  - Câu *"thông thường từ Level 2 hoặc Level 3"* nên đổi thành **Level 3**. Level 2 thực tế chỉ là mức yêu cầu cho khóa của thuê bao (subscriber) ký mã nguồn (code signing). Cần đọc lại trực tiếp Mục 6.2.7 trong BR để đối chiếu chi tiết.
- **Quy định về CP/CPS (Mục 3.3.1 - Mục 2.2 BR)**:
  - Mục 2.2 BR **không quy định việc bắt buộc gộp CP/CPS**. Mục này chỉ yêu cầu CP và/hoặc CPS phải tuân thủ cấu trúc của RFC 3647 và chứa đầy đủ nội dung theo yêu cầu.
  - "Gộp" (combined CP/CPS) chỉ là thực tế triển khai phổ biến của các CA thương mại (BR có nhắc đến thuật ngữ này ở mục khác). Cần viết lại câu ở 3.3.1 theo đúng tinh thần này.
- **Phạm vi áp dụng BR (Mục 3.3.5 và 6.4)**:
  - BR nêu rõ: BR **không điều chỉnh hệ thống PKI nội bộ doanh nghiệp** mà Root CA không được các nhà phát triển phần mềm/hệ điều hành (root store) tin cậy và phân phối mặc định.
  - Các yêu cầu của BR chỉ mang tính ràng buộc bắt buộc khi được các nhà cung cấp phần mềm tin cậy (Root Store Programs: Mozilla, Microsoft, Apple, Google) chấp nhận và thực thi. Cần dùng luận điểm này để giải thích vì sao lab mô phỏng nằm ngoài phạm vi điều chỉnh bắt buộc của BR.
- **Kiểm toán hằng năm (Mục 8 BR và Bảng 3.3)**:
  - Cần tự tra cứu và đọc kỹ Mục 8 BR cùng chính sách Root Store trước khi khẳng định câu *"kiểm toán hằng năm"*, bao gồm cả nội dung trong Bảng 3.3.

---

### 2. Báo cáo Fox-IT về sự cố DigiNotar

| Câu trong bản nháp | Kết quả đối chiếu & Đánh giá | Chi tiết chỉnh sửa |
| :--- | :--- | :--- |
| *“không áp dụng HSM chặt chẽ”* | **Sai** | DigiNotar thực tế có trang bị HSM (nCipher netHSM), khóa chỉ được kích hoạt bằng thẻ thông minh (smartcard) kèm mã PIN. Tuy nhiên, toàn bộ 8 máy chủ quản lý CA đều bị chiếm quyền điều khiển. Kẻ tấn công đã thực hiện ký chứng thư giả mạo ngay trong lúc khóa đang ở trạng thái kích hoạt (activated). |
| *“mật khẩu quản trị yếu”* | **Đúng theo bản tạm (Mục 4.4)** | Mật khẩu yếu dễ bị tấn công vét cạn (brute-force); tất cả các máy chủ CA cùng gia nhập một miền Windows (single domain); hệ thống thiếu phần mềm diệt virus (antivirus) và không có hệ thống ghi nhật ký tập trung an toàn. |
| *“không phân tách mạng đúng chuẩn”* | **Đúng một phần** | Mạng có chia 24 phân đoạn và có phân vùng `Secure-net` tách riêng; tuy nhiên ranh giới các vùng không được định nghĩa rõ ràng và không thực thi nghiêm ngặt, tường lửa (firewall) cấu hình nhiều luật ngoại lệ lỏng lẻo. |
| *“xóa nhật ký mà không bị phát hiện”* | **Cần sửa** | Nhật ký được lưu trữ trực tiếp trên chính các máy chủ bị chiếm quyền và đã có bằng chứng về việc bị can thiệp/chỉnh sửa. Do đó, sự vắng mặt của các bản ghi đáng ngờ không đồng nghĩa với việc không có hành vi cấp phát trái phép. |
| *“đã vượt qua các kỳ kiểm toán”* | **Chưa tìm thấy căn cứ** | Phần báo cáo chưa tìm thấy thông tin này (bản tạm chỉ nhắc đến một báo cáo của công ty pentest/audit vào ngày 27/07). Cần chỉ rõ trang tham chiếu cụ thể hoặc lược bỏ khẳng định này. |
| *Chương 1: “không hề làm phát sinh cảnh báo”* | **Sai** | Sự cố thực tế bị phát hiện khi trình duyệt Google Chrome chủ động chặn chứng thư giả mạo của Google nhờ cơ chế **Certificate Pinning** (vào ngày 28/08/2011). |

- **Số liệu chính xác cần đưa vào**:
  - Tối thiểu **531 chứng thư giả mạo** được phát hiện (danh sách chưa đầy đủ).
  - Khoảng **298.140 địa chỉ IP** bị ảnh hưởng, trong đó xấp xỉ **95% tại Iran** (lưu ý: số lượng IP chỉ là ước tính thô cho số người dùng thực tế).  
  *Nguồn*: [Báo cáo Fox-IT (Chính phủ Hà Lan công bố)](https://zoek.officielebekendmakingen.nl/blg-191225.pdf)
- **Thông tin trích dẫn tài liệu [1] (Fox-IT)**:
  - Bản tạm ghi tác giả: *"J.R. Prins (CEO Fox-IT)"*.
  - Bản chính thức (Final Report, 101 trang nộp Bộ Nội vụ Hà Lan): nhóm điều tra Fox-IT do **Hans Hoogstraaten** dẫn đầu, cùng **Ronald Prins** (CEO), không có tên "Jelle Schipper".
  - **Khuyến nghị**: Trích dẫn nguồn với tác giả tổ chức là **Fox-IT**. Nên trích dẫn bản báo cáo cuối cùng (101 trang) vì chứa đầy đủ thông tin kỹ thuật về HSM, log và cấu trúc mạng, có thể kèm theo bản tạm thời (Interim Report).  
  *Nguồn tham khảo*: [SEC Filing - Fox-IT Report](https://www.sec.gov/Archives/edgar/data/1044777/000119312511241796/dex992.htm)
- **Đề xuất viết lại đoạn DigiNotar ở Mục 3.3.4**:
  > *"Báo cáo của Fox-IT [1] cho thấy DigiNotar có trang bị HSM và khóa riêng chỉ được kích hoạt bằng thẻ thông minh, nhưng toàn bộ tám máy chủ quản lý CA đều bị chiếm quyền điều khiển, dẫn đến việc kẻ tấn công ký được chứng thư giả mạo khi khóa đang ở trạng thái kích hoạt. Các máy chủ CA dùng chung một miền Windows với chính sách mật khẩu yếu, nhật ký sự kiện lưu cục bộ trên chính máy bị xâm nhập và đã bị can thiệp. Bài học từ DigiNotar chứng minh rằng HSM, chính sách trên giấy và kiểm toán chỉ là điều kiện cần chứ chưa đủ để đảm bảo an toàn nếu khâu vận hành và kiến trúc bảo mật bị buông lỏng."*

---

## B. Chương 1

### 1. Điểm tiến bộ đã ghi nhận
- Quy ước ký hiệu rõ ràng: $PU/PR$ (Public/Private Key) và $PK/SK$ (Public/Secret Key).
- Bổ sung bảng ánh xạ từ các câu hỏi nghiên cứu (RQ) sang cấu trúc các chương.
- Mục 1.3 đã được bổ sung nội dung.

### 2. Các điểm cần khắc phục và chỉnh sửa
- **Danh sách 4 bước kiểm tra của Alice (Mục 1.1.4)**:
  - Chưa đồng bộ với nội dung Chương 3 và thực nghiệm: Mục 3.2 (bước 6) đã đề cập đến việc xây dựng chuỗi chứng thư lên Trust Anchor, kiểm tra `pathLenConstraint` và `Extended Key Usage (EKU)`.
  - Các ca kiểm thử `TC02`, `TC06`, `TC08`, `TC10` đều kiểm tra các điều kiện này. Do đó, danh sách 4 bước kiểm tra cơ bản ở Chương 1 cần được cập nhật/bổ sung để khớp với logic kỹ thuật phía sau.
- **Đoạn phân tích sự cố DigiNotar (Mục 1.1.4)**:
  - Sửa lại các chi tiết lịch sử: cơ chế cảnh báo của Google Chrome (Certificate Pinning), cập nhật số liệu chuẩn (531 certs, ~300k IP).
  - Diễn đạt: Cụm từ *"khó phát hiện"* nên đổi thành *"kiểm tra chữ ký thông thường không phát hiện được"* (bởi vì chứng thư giả mạo vẫn mang chữ ký số hoàn toàn hợp lệ từ Root CA bị xâm nhập).
- **Phạm vi nghiên cứu (Mục 1.3) bị lệch so với Lab**:
  - Mục 1.3 nêu *"hai cơ chế CRL và OCSP"*, nhưng kịch bản thực nghiệm `TC07` chỉ kiểm tra CRL. Cần ghi rõ: **OCSP chỉ được phân tích trên khía cạnh lý thuyết**.
  - Cụm từ *"Hạ tầng PKI hoàn chỉnh"* gây mâu thuẫn trực tiếp với Mục 3.3.5. Cần chỉnh thành **"Hạ tầng PKI mô phỏng"**.
  - Cụm từ *"Đo lường"* dễ tạo kỳ vọng về việc thực hiện benchmark định lượng/hiệu năng (Giả thuyết $H_3$). Nếu nhóm không thực hiện benchmark, cần điều chỉnh từ ngữ.
  - Cần bổ sung rõ ràng các giới hạn và những phần **nằm ngoài phạm vi nghiên cứu** (Out of Scope).
- **Giả thuyết nghiên cứu ($H_1$ – $H_3$)**:
  - Hiện tại chỉ xuất hiện đột ngột ở Mục 6.1. Cần giới thiệu tóm tắt ngay tại Mục 1.2 và liên kết chặt chẽ với các câu hỏi nghiên cứu ($RQ$).
  - Cụm từ *"kiểm chứng trực quan"* ở $RQ_2, RQ_3$ cần chỉ rõ được kiểm chứng thông qua các thực nghiệm/kịch bản cụ thể nào.
- **Trích dẫn khoa học**:
  - Mục 1.1.1 chưa có trích dẫn nguồn lịch sử (Diffie–Hellman 1976, RSA 1978).
  - Mục 1.3 nhắc đến RFC 5280, RFC 6960, RFC 8446, RFC 3647 nhưng chưa gắn lệnh `\cite`.
- **Các góp ý nhỏ về mặt kỹ thuật/thuật ngữ**:
  - Tiêu đề Mục 1.1.2 ghi *"trao đổi khóa"* nhưng nội dung thực tế lại mô tả bài toán *mã hóa thông điệp*.
  - Thuật ngữ *"nghịch lý toán học"*: bản chất đây là bài toán một chiều (one-way trapdoor function), không phải "nghịch lý".
  - Công thức (1.3) đang lặp lại nội dung của công thức (1.1) và (1.2).
  - Cần bổ sung nhận định: mô hình ở mục này là mô hình lý thuyết đơn giản hóa; thực tế các giao thức hiện đại đều áp dụng mô hình lai (Hybrid Cryptography - chi tiết ở Mục 2.3).

---

## C. Chương 2

- **Mục 2.1.1**:
  - Khẳng định *"loại bỏ triệt để nguy cơ"* là nói quá (bằng chứng là vụ DigiNotar dù có CA nhưng vẫn bị xâm nhập). Cần đổi thành **"giảm thiểu nguy cơ"**.
- **Mục 2.1.2**:
  - Câu *"Máy chủ quan trọng phải lưu khóa trong HSM"* là quá mức mở rộng; theo BR chỉ áp dụng bắt buộc đối với **khóa của Root CA và Intermediate CA**.
  - Thống nhất thuật ngữ: Mục 2.1.2 viết *"k-out-of-n"*, trong khi Mục 3.3 lại viết *"m-trên-n"*. Cần đồng nhất một kiểu ký hiệu xuyên suốt tài liệu.
  - Khái niệm **"Cryptoperiod"** hiện đang bị gán với thuộc tính `notBefore` / `notAfter`. Đây thực chất là *thời hạn hiệu lực của chứng thư* (Certificate Validity Period), không phải *thời hạn sử dụng an toàn của cặp khóa* (Key Cryptoperiod). Cần tách bạch đúng như Mục 3.2 đã phân tích.
- **Mục 2.2**:
  - Cần làm rõ: chuẩn mã hóa PKCS#1 v1.5 sử dụng cơ chế đệm tất định (deterministic padding), chỉ có RSA-PSS mới là lược đồ đệm xác suất (probabilistic signature).
  - Đối với công thức tổng quát: $\sigma = \text{Sign}(SK, H(m))$, cần ghi chú thêm rằng thuật toán chữ ký **Ed25519 (EdDSA)** thực hiện ký trực tiếp trên thông điệp (pure mode băm bên trong thuật toán) chứ không qua một bước băm $H(m)$ độc lập bên ngoài như RSA/ECDSA truyền thống.
- **Mục 2.3 (Đối chiếu RFC 8446 - TLS 1.3)**:
  - Giao thức TLS 1.3 vẫn hỗ trợ chế độ xác thực chỉ sử dụng Pre-Shared Key (PSK-only handshake), do đó khẳng định *"bắt buộc ECDHE/DHE"* chỉ chính xác đối với **handshake xác thực dựa trên chứng thư số (Certificate-based Handshake)**.
  - Câu *"loại bỏ hoàn toàn nguy cơ giả mạo"* cần được chỉnh sửa chính xác về mặt mật mã học: Bản tin `CertificateVerify` chỉ chứng minh bên gửi sở hữu khóa riêng tương ứng với khóa công khai trong chứng thư (Proof-of-Possession), chứ **không chứng minh** được chứng thư đó có bị cấp phát trái phép hoặc bị thỏa hiệp từ CA hay không.

---

## D. Chương 3

### 1. Mục 3.1: Kiến trúc phân cấp PKI
- **Kế thừa niềm tin**: Khẳng định *"Tự động được thừa hưởng độ tin cậy"* còn mang tính vô điều kiện. Cần sửa thành: *"được tin cậy nếu toàn bộ đường dẫn chứng thư thỏa mãn các điều kiện kiểm tra xác thực ở Mục 4.2"*.
- **Thuật ngữ khóa Root CA**: Cụm từ *"Cặp khóa mã hóa tối cao"* chưa chuẩn xác về chức năng; bản chất khóa của Root CA là **cặp khóa ký (signing key pair)**.
- **Trạng thái Root CA**: Thay vì nói *"Luôn offline tuyệt đối"*, nên diễn đạt là **"thường được duy trì ở trạng thái ngoại tuyến (offline)"** (trong thực tế có thể bật online khi thực hiện lễ ký định kỳ).
- **Extension `basicConstraints` của End-entity**: Cần đối chiếu lại chuẩn RFC 5280: đối với chứng thư thực thể cuối (End-entity), chuẩn cho phép extension này có thể **vắng mặt** hoặc có giá trị `cA:FALSE`.
- **Phân định khái niệm Subject**: Mục *"Subject / End-entity"* hiện đang gộp lẫn hai khái niệm. Subject là một trường thuộc tính định danh trong chứng thư X.509, còn End-entity là vai trò của đối tượng trong cấu trúc PKI.
- **Phân tách trách nhiệm (Segregation of Duties)**: Thuật ngữ này đang bị dùng sai ngữ cảnh kỹ thuật. *Segregation of Duties* là nguyên tắc phân tách quyền hạn giữa các cá nhân/nhân sự vận hành; còn ý đồ trong bài đang nói về **phân nhánh CA theo mục đích sử dụng (purpose-based CA segmentation)** (ví dụ: CA chuyên ký web server, CA chuyên ký email, CA ký mã nguồn).
- **Nội dung còn thiếu**:
  - Bảng/sơ đồ ánh xạ rõ thành phần nào trong mô hình lý thuyết được triển khai trong lab thực nghiệm.
  - Câu dẫn trỏ sang Mục 5.2 khi thảo luận về các mô hình PKI khác (Cross-certification, Bridge CA, Web of Trust).
  - Bổ sung trích dẫn cho RFC 5280 và RFC 3647.

---

### 2. Mục 3.2: Vòng đời chứng thư số (Lifecycle)
- **Quy trình Certificate Transparency (CT)**:
  - Hiện tại sơ đồ Hình 3.2 và Bước 4 đang mô tả *"sau khi ký chứng thư thì gửi vào CT Log"*. Điều này chưa đúng với thực tế: CA phải tạo **chứng thư tiền phát hành (Precertificate)**, gửi lên CT Log để nhận lại bằng chứng ghi nhận thời gian **SCT (Signed Certificate Timestamp)**, sau đó nhúng SCT này vào chính chứng thư cuối cùng trước khi phát hành.
  - Lưu ý thêm: Việc gửi CT Log là **chính sách bắt buộc của các trình duyệt (Chrome, Safari...)**, không phải là yêu cầu bắt buộc trong chuẩn gốc của RFC 5280.
- **Chứng thư xác thực mở rộng (EV - Extended Validation)**:
  - Quy chuẩn cấp phát EV được quy định trong tài liệu riêng **EV Guidelines**, không nằm trong bộ tiêu chuẩn BR cơ bản. Cần tách riêng trích dẫn ở Bước 3.
- **Quy định rút ngắn thời hạn chứng thư (Bước 7)**:
  - Thay vì câu chung chung *"liên tục rút ngắn"*, nên bổ sung số liệu lộ trình cụ thể từ bản **CA/B Forum BR 2.3.1**:
    - Tối đa **200 ngày**: áp dụng từ ngày 15/03/2026.
    - Tối đa **100 ngày**: áp dụng từ ngày 15/03/2027.
    - Tối đa **47 ngày**: áp dụng từ ngày 15/03/2029.
- **Lưu ý cấu hình `copy_extensions`**:
  - Việc gắn `copy_extensions = copy` với `TC04` / `TC08` dễ gây hiểu nhầm đây là một kịch bản kiểm thử bảo mật. Cần giải thích rõ đây là **bẫy cấu hình (pitfall) khi dựng CA bằng OpenSSL**; nếu cấu hình sai CA sẽ bỏ qua trường `Subject Alternative Name (SAN)`, khiến trình duyệt từ chối chứng thư. Đồng thời cần đảm bảo kịch bản chuẩn `TC01` phải có cấu hình SAN đầy đủ.
- **Khắc phục cam kết nội dung**:
  - Phần mở đầu Mục 3.2 có nhắc rằng vòng đời của chính CA (CA key lifecycle) sẽ được trình bày ở Mục 3.3, nhưng Mục 3.3 hiện chưa có. Cần bổ sung 2–3 câu tóm tắt về quy trình thay thế khóa CA (CA Key Rollover/Rekey) và ngừng hoạt động CA (CA Termination) theo mục 5.6 và 5.8 của cấu trúc RFC 3647, hoặc điều chỉnh lại câu giới thiệu.
- **Đề xuất bổ sung**:
  - Bổ sung bảng tổng hợp ánh xạ: **[Giai đoạn vòng đời] $\rightarrow$ [Lệnh OpenSSL tương ứng] $\rightarrow$ [Kịch bản Test Case kiểm thử]**.

---

### 3. Mục 3.3: Chính sách, Vận hành và So sánh
- Sửa các nội dung về FIPS, BR 2.2 và bài học DigiNotar theo các điểm đã nêu ở Phần A.
- **Chỉnh sửa Bảng 3.3**:
  - Cột giữa hiện dùng từ ngữ quá khẳng định, mâu thuẫn với nội dung 3.3.3: *"tối thiểu 4 vai trò"*, *"không cho phép kiêm nhiệm"*, *"kiểm toán hằng năm"*. Đổi tiêu đề cột thành **"CPS của CA công cộng thường đặc tả"** và sử dụng từ ngữ có tính chất phản ánh thực tế ("thường quy định").
  - Cột Lab: Vì nhóm nghiên cứu gồm 3 thành viên, cách diễn đạt *"một cá nhân duy nhất"* nên đổi thành **"một máy trạm, một tài khoản quản trị, không phân tách vai trò"**.
  - Kiểm tra và đối chiếu các chi tiết về đường dẫn file khóa riêng (`.key`) và mật khẩu bảo vệ với tài liệu hướng dẫn trong `demo/README.md`.
- **Câu kết Mục 3.3.5**:
  - Cụm từ *"chứng minh tính đúng đắn"* mang tính tuyệt đối hóa; nên đổi thành: **"quan sát phản ứng của quy trình xác minh chuỗi chứng thư đối với từng điều kiện vi phạm kỹ thuật cụ thể"**.

---

### 4. Bổ sung tài liệu tham khảo (References)
Cần bổ sung các nguồn chuẩn sau vào danh mục tài liệu trích dẫn (`.bib`):
1. **CA/B Forum Baseline Requirements** (ghi rõ phiên bản sử dụng, ví dụ v2.3.1).
2. **CA/B Forum EV Guidelines**.
3. **Network and Certificate System Security Requirements (NCSSR)**.
4. **WebTrust Principles and Criteria for Certification Authorities**.
5. **ETSI EN 319 411** (Tiêu chuẩn kỹ thuật chữ ký số và PKI của Châu Âu).
6. **NIST FIPS 140-3** (Chuẩn bảo mật mô-đun mật mã).
7. Các tài liệu nền tảng:
   - Shamir, A. (1979). *"How to share a secret"*.
   - Diffie, W., & Hellman, M. (1976). *"New directions in cryptography"*.
   - Rivest, R. L., Shamir, A., & Adleman, L. (1978). *"A method for obtaining digital signatures and public-key cryptosystems"*.
- **Lưu ý định dạng BibTeX**: Phải đặt dấu ngoặc nhọn `{...}` quanh các từ viết tắt kỹ thuật để giữ đúng chữ in hoa trong tiêu đề tài liệu xuất bản: ví dụ `{X.509}`, `{TLS}`, `{CRL}`, `{OCSP}`, `{RSA}`.

---

## E. Thứ tự ưu tiên thực hiện chỉnh sửa

1. **Ưu tiên 1 (Lỗi sai sự kiện & chuẩn mực)**:
   - Đính chính yêu cầu FIPS 140 Level 3 tại 3.3.2.
   - Sửa toàn bộ đoạn phân tích sự cố DigiNotar (HSM, log, miền Windows, phát hiện nhờ Pinning, số liệu chứng thư/IP).
   - Đính chính trích dẫn Mục 2.2 của BR (về CP/CPS).
   - Chuẩn hóa lại thông tin tài liệu trích dẫn `[1]` (Fox-IT) và `[4]` (phiên bản BR).
2. **Ưu tiên 2 (Khớp nối logic giữa lý thuyết và thực nghiệm)**:
   - Bổ sung 2 bước kiểm tra chuỗi/chính sách vào danh sách 4 bước kiểm tra của Alice ở Mục 1.1.4.
   - Rà soát lại phạm vi Mục 1.3: làm rõ OCSP chỉ phân tích lý thuyết, thay đổi thuật ngữ "hạ tầng hoàn chỉnh" thành "mô phỏng", giải thích rõ phạm vi ngoài nghiên cứu (out-of-scope).
   - Tóm tắt các giả thuyết $H_1, H_2, H_3$ ở Mục 1.2 và liên kết với các RQ.
3. **Ưu tiên 3 (Cấu trúc bảng biểu & quy trình kỹ thuật)**:
   - Hiệu chỉnh tiêu đề và nội dung các cột trong Bảng 3.3.
   - Chỉnh lại đúng thứ tự phát hành có nhúng SCT từ Certificate Transparency (Precertificate $\rightarrow$ CT Log $\rightarrow$ SCT $\rightarrow$ End-entity cert) ở Mục 3.2 và Hình 3.2.
4. **Ưu tiên 4 (Hoàn thiện học thuật & tinh chỉnh văn phong)**:
   - Thêm đầy đủ các trích dẫn thiếu (Diffie-Hellman, RSA, các RFCs, FIPS 140-3, WebTrust, ETSI).
   - Thống nhất toàn bộ ký hiệu ($k$-out-of-$n$, $PU/PR$, $PK/SK$).
   - Tinh chỉnh các câu chữ nói quá ("loại bỏ triệt để", "nghịch lý", "tự động thừa hưởng").
