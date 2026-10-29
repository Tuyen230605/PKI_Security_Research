"""
Script tao bieu do so sanh kich thuoc Public Key va Chu ky so
giua Mat ma Co dien va Mat ma Hau luong tu (NIST PQC Standards FIPS 204, FIPS 205, FIPS 206).
Xuat file: report/figures/pqc-size-comparison.pdf va report/figures/pqc-size-comparison.png
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Thiet lap phong chu va phong cach do hoa chuan hoc thuat
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# Du lieu so sanh: Ten thuat toan, Public Key (bytes), Signature (bytes), Nhom
algorithms = [
    # Co dien
    {"name": "ECDSA P-256", "pk": 65, "sig": 64, "group": "Classical"},
    {"name": "Ed25519", "pk": 32, "sig": 64, "group": "Classical"},
    {"name": "RSA-2048", "pk": 270, "sig": 256, "group": "Classical"},
    {"name": "RSA-4096", "pk": 526, "sig": 512, "group": "Classical"},
    # Hau luong tu NIST
    {"name": "FN-DSA-512\n(Falcon)", "pk": 897, "sig": 666, "group": "PQC Lattice"},
    {"name": "ML-DSA-44\n(FIPS 204)", "pk": 1312, "sig": 2420, "group": "PQC Lattice"},
    {"name": "ML-DSA-65\n(FIPS 204)", "pk": 1952, "sig": 3309, "group": "PQC Lattice"},
    {"name": "ML-DSA-87\n(FIPS 204)", "pk": 2592, "sig": 4627, "group": "PQC Lattice"},
    {"name": "SLH-DSA-128s\n(FIPS 205)", "pk": 32, "sig": 7856, "group": "PQC Stateless Hash"},
    {"name": "SLH-DSA-128f\n(FIPS 205)", "pk": 32, "sig": 17088, "group": "PQC Stateless Hash"},
]

names = [item["name"] for item in algorithms]
pk_sizes = [item["pk"] for item in algorithms]
sig_sizes = [item["sig"] for item in algorithms]

x = np.arange(len(names))
width = 0.38

fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)

# Ve 2 cot: Public Key va Signature
bars_pk = ax.bar(x - width/2, pk_sizes, width, label='Khóa công khai (Public Key)', color='#2b5c8f', edgecolor='black', linewidth=0.6)
bars_sig = ax.bar(x + width/2, sig_sizes, width, label='Chữ ký số (Digital Signature)', color='#d95f02', edgecolor='black', linewidth=0.6)

# Ve duong nguong TCP MSS / MTU chuan tren Internet de minh hoa phan manh goi tin
ax.axhline(y=1460, color='#c00000', linestyle='--', linewidth=1.2, label='TCP MSS chuẩn (1.460 bytes)')
ax.text(len(names) - 0.55, 1550, 'Ngưỡng TCP MSS (1.460 B)', color='#c00000', fontsize=8.5, fontweight='bold', ha='right')

# Trục tung logarit de the hien su phan hoa tu hang chuc byte toi hang chuc kilobyte
ax.set_yscale('log')
ax.set_ylabel('Dung lượng (Bytes, thang đo logarit)', fontsize=10.5, fontweight='bold')
ax.set_title('So sánh kích thước khóa công khai và chữ ký số: Mật mã cổ điển vs Hậu lượng tử (NIST)', fontsize=11.5, fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=8.5, rotation=0)

# Hien thi so lieu tren dau cot
for bar in bars_pk:
    height = bar.get_height()
    ax.annotate(f'{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 2),  # 2 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom', fontsize=7.2, rotation=90)

for bar in bars_sig:
    height = bar.get_height()
    ax.annotate(f'{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 2),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=7.2, rotation=90)

# Vung phan tach giua Co dien va Hau luong tu
ax.axvline(x=3.5, color='gray', linestyle=':', linewidth=1.2)
ax.text(1.5, 30000, 'MẬT MÃ CỔ ĐIỂN', fontsize=9.5, fontweight='bold', color='#444444', ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="#f0f0f0", ec="#cccccc"))
ax.text(6.5, 30000, 'CHUẨN HẬU LƯỢNG TỬ NIST (FIPS 204/205/206)', fontsize=9.5, fontweight='bold', color='#444444', ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="#f0f0f0", ec="#cccccc"))

ax.set_ylim(10, 60000)
ax.grid(axis='y', which='both', linestyle=':', alpha=0.5)
ax.legend(loc='upper left', framealpha=0.95, fontsize=9)

plt.tight_layout()

# Luu file
output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'report', 'figures')
os.makedirs(output_dir, exist_ok=True)

pdf_path = os.path.join(output_dir, 'pqc-size-comparison.pdf')
png_path = os.path.join(output_dir, 'pqc-size-comparison.png')

plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f"Da xuat thanh cong:\n  {pdf_path}\n  {png_path}")

