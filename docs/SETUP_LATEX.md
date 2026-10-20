# Cài LaTeX và build báo cáo sau khi clone/pull

Hướng dẫn dựng báo cáo trên máy mới. Báo cáo dùng **pdfLaTeX + latexmk + BibTeX**, file nguồn UTF-8. Chạy mọi lệnh build từ **thư mục gốc**, nơi có `Makefile` và `report/`; không chạy trong `report/`. Không cần `npm install`, `pip install` hay tải riêng source LaTeX sau khi clone. Lần build đầu trên Windows có thể cần Internet để MiKTeX tải gói còn thiếu.

## 1. Ubuntu: cài một lần trên mỗi máy

Mở Terminal, copy cả khối:

```bash
sudo apt update
sudo apt install -y git make perl latexmk \
  texlive-latex-base texlive-latex-recommended texlive-latex-extra \
  texlive-lang-other texlive-fonts-recommended \
  openssl python3
pdflatex --version
latexmk -v
kpsewhich vietnam.sty
```

Ba lệnh cuối phải in ra phiên bản pdfLaTeX/latexmk và đường dẫn `vietnam.sty`. `git` dùng để lấy source; `openssl` và `python3` dùng cho demo PKI. Nếu chỉ sửa báo cáo, chưa cần chạy demo nhưng cài sẵn hai công cụ này giúp dùng chung quy trình của nhóm.

## 2. Windows: cài một lần trên mỗi máy

Mở **PowerShell**. Cần có `winget` (`winget --version`). Nếu máy chưa có `winget`, cài/cập nhật **App Installer** theo [hướng dẫn Microsoft](https://learn.microsoft.com/en-us/windows/package-manager/winget/); sau đó chạy:

```powershell
winget install --id Git.Git --exact --source winget
winget install --id MiKTeX.MiKTeX --exact --source winget
winget install --id StrawberryPerl.StrawberryPerl --exact --source winget
```

Đóng PowerShell, mở cửa sổ **PowerShell mới** để nhận PATH. Cài các gói LaTeX chính của báo cáo rồi kiểm tra:

```powershell
miktex packages update-package-database
miktex packages install latexmk vntex geometry hyperref graphics amsmath amsfonts booktabs latex-tools
git --version
perl --version
pdflatex --version
latexmk -v
kpsewhich vietnam.sty
```

Nếu MiKTeX hỏi cài thêm gói khi build, chọn **Install**; có thể bật *Install missing packages: Always* trong MiKTeX Console. Nếu `pdflatex`, `latexmk` hoặc `perl` chưa được nhận diện sau khi cài, đóng/mở lại PowerShell, sau đó kiểm tra PATH và cài đặt trong MiKTeX Console. `vietnam.sty` thuộc gói `vntex`.

**Demo trên Windows:** các script trong `demo/scripts/` là Bash dành cho Ubuntu. Để chạy demo trên máy Windows, mở PowerShell với quyền Administrator, chạy `wsl --install -d Ubuntu`, khởi động lại nếu được yêu cầu, mở ứng dụng Ubuntu và làm theo mục **Ubuntu** ở trên. Có thể clone repository trực tiếp trong Ubuntu/WSL rồi chạy `make demo-test`. Việc build PDF bằng PowerShell/MiKTeX không cần WSL.

## 3. Lần đầu lấy dự án về

Repository của nhóm: `https://github.com/Tuyen230605/PKI_Security_Research.git`. Copy các dòng tương ứng với hệ điều hành.

Ubuntu hoặc Ubuntu trong WSL:

```bash
REPO_URL='https://github.com/Tuyen230605/PKI_Security_Research.git'
git clone "$REPO_URL" MM
cd MM
git status --short
make report
```

Windows PowerShell:

```powershell
$RepoUrl = 'https://github.com/Tuyen230605/PKI_Security_Research.git'
git clone $RepoUrl MM
Set-Location MM
git status --short
New-Item -ItemType Directory -Force build | Out-Null
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build report/main.tex
```

Nếu đã clone từ trước, vào thư mục dự án rồi chạy `git pull` trước khi build. Sau `git pull`, **không cần cài lại LaTeX**; chỉ chạy lại lệnh build. Mỗi máy chỉ phải cài công cụ ở mục 1 hoặc 2 một lần, trừ khi nhóm bổ sung package LaTeX mới.

## 4. Build, xem PDF và dọn file sinh ra

### Ubuntu / WSL

```bash
make report
xdg-open build/main.pdf
```

Khi cần xóa output và build lại từ đầu:

```bash
make clean
make report
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force build | Out-Null
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build report/main.tex
Invoke-Item .\build\main.pdf
```

Khi cần xóa output và build lại từ đầu:

```powershell
latexmk -C -outdir=build report/main.tex
Remove-Item -Recurse -Force build
New-Item -ItemType Directory -Force build | Out-Null
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build report/main.tex
```

PDF nằm ở `build/main.pdf`. `latexmk` tự chạy BibTeX và biên dịch lại khi cần; sau mỗi lần sửa chương hoặc nguồn tham khảo, chạy lại đúng lệnh build. Thông báo `All targets ... are up-to-date` nghĩa là không có thay đổi cần biên dịch.

Nếu build lỗi, đọc lỗi đầu tiên trong `build/main.log` hoặc ngay trên terminal. Các lỗi thường gặp: `File vietnam.sty not found` (thiếu `vntex`), `latexmk` không chạy trên Windows (thiếu Perl/PATH), `undefined citation` (sai key trong `references.bib`), thiếu file hình, hoặc ký tự `%`, `&`, `_`, `#` chưa escape trong LaTeX. Sau khi sửa, chạy lại lệnh build.

## 5. Sửa nội dung báo cáo

1. Theo [kế hoạch](HOAN_THANH_DU_AN.md), sửa file tương ứng trong `report/chapters/`. Lưu file `.tex` dưới dạng UTF-8.
2. Đặt hình nguồn trong `report/figures/`, bảng/CSV đã lọc trong `report/tables/`. Thêm chú thích và nguồn cho hình/bảng.
3. Thêm tài liệu vào `report/references.bib` rồi dùng `\cite{key}`. Hạn chế sửa `report/preamble.tex` và `report/main.tex` cùng lúc với người khác.
4. Chạy build và đọc PDF trước khi bàn giao. Kiểm tra lỗi font tiếng Việt, hình/bảng tràn lề và cảnh báo trích dẫn.
5. Kết quả trong `demo/out/results.tsv` là output cục bộ. Muốn đưa vào báo cáo, kiểm tra từng test, sao chép **bảng đã lọc** sang `report/tables/` và ghi môi trường chạy; không thêm toàn bộ `demo/out/`.

## 6. Trước khi commit/push: file nào đưa lên Git?

| Đưa lên repository | Không đưa lên repository |
|---|---|
| `report/*.tex`, `report/chapters/`, `report/references.bib`, hình/bảng nguồn đã kiểm tra | `build/`, file `.aux`, `.log`, `.bbl`, `.toc`, `.lof`, `.lot` và output LaTeX khác |
| `docs/`, `README.md`, `Makefile`, `.gitignore`, `slides/` | `demo/out/`: private key, certificate, CSR, CRL, cơ sở dữ liệu CA và kết quả thô |
| `demo/scripts/`, `demo/README.md`, hai file introduction gốc | `.vscode/`, file tạm của editor, khóa `.key`, `.pem`, `.p12`, `.pfx` nằm ngoài lab |

Các mục không đưa lên Git đã được khai báo trong [`.gitignore`](../.gitignore). **Không dùng `git add -f` để ép thêm file bị bỏ qua.** File PDF cuối cùng để nộp lấy từ `build/main.pdf` rồi nộp theo yêu cầu giảng viên; repository giữ source và lệnh tái tạo PDF. Nếu nhóm quyết định lưu PDF phát hành trên Git, thống nhất vị trí/file riêng sau khi đã duyệt bản cuối.

Trước mỗi commit, chạy từ thư mục gốc của **repository Git thật**:

```bash
git status --short
git check-ignore -v build/main.pdf demo/out/intermediate/newcerts/1000.pem
git add -A
git diff --cached --name-only
```

Chỉ commit khi danh sách ở lệnh cuối chứa file nguồn mong muốn và **không có** `build/`, `demo/out/` hoặc khóa bí mật. Nếu lỡ stage một file, chạy `git restore --staged -- DUONG_DAN_FILE`, kiểm tra lại rồi mới `git commit` và `git push`. PowerShell dùng cùng các lệnh Git này.

`.gitignore` không tự gỡ file đã được theo dõi từ commit cũ. Nếu `git ls-files build demo/out` còn in ra file, chạy `git rm -r --cached --ignore-unmatch -- build demo/out` để bỏ theo dõi mà giữ file trên máy, rồi kiểm tra `git diff --cached --name-only`. Nếu từng push **khóa thật** lên remote, cần xử lý khóa đó như đã lộ; bỏ theo dõi không xóa nó khỏi lịch sử Git.

## Nguồn lệnh cài đặt

[WinGet install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install), [manifest MiKTeX](https://github.com/microsoft/winget-pkgs/tree/master/manifests/m/MiKTeX/MiKTeX), [MiKTeX package manager](https://docs.miktex.org/manual/miktex-packages.html), [MiKTeX tự cài gói thiếu](https://docs.miktex.org/manual/autoinstall.html), [cài WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [Git check-ignore](https://git-scm.com/docs/git-check-ignore).
