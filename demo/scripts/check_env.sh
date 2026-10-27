#!/usr/bin/env bash
# ==============================================================================
# Script: check_env.sh
# Mục đích: Tự động trích xuất thông số môi trường thực nghiệm cho Chương 6
# ==============================================================================

echo "=== HE DIEU HANH VA NHAN KERNEL ==="
uname -s -r -m
if [ -f /etc/os-release ]; then
    grep PRETTY_NAME /etc/os-release | cut -d'=' -f2 | tr -d '"'
fi

echo "=== THIET BI PHAN CUNG ==="
lscpu | grep "Model name" | sed 's/Model name:[ \t]*/CPU: /'
free -h | awk '/Mem:/ {printf "RAM WSL2: %s (Kha dung: %s)\n", $2, $7}'

echo "=== PHIEN BAN OPENSSL ==="
openssl version
openssl version -d

echo "=== THOI DIEM CHAY THUC NGHIEM ==="
date +"%A, %d/%m/%Y %H:%M:%S %Z"
