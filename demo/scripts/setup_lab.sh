#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$BASE_DIR/out"

for command_name in openssl python3; do
  command -v "$command_name" >/dev/null || { echo "Thiếu $command_name" >&2; exit 1; }
done

if [[ -f "$OUT/.lab_marker" ]]; then
  echo "Lab đã tồn tại tại $OUT. Xem demo/README.md để tạo lại từ đầu."
  exit 0
fi
if [[ -e "$OUT" ]]; then
  echo "Thư mục $OUT đã tồn tại nhưng không phải lab do script tạo; hãy kiểm tra thủ công." >&2
  exit 1
fi

mkdir -p "$OUT/root" "$OUT/intermediate/newcerts" "$OUT/servers" "$OUT/other-ca"
printf '1000\n' > "$OUT/intermediate/serial"
printf '1000\n' > "$OUT/intermediate/crlnumber"
: > "$OUT/intermediate/index.txt"

# Root is trusted only when passed explicitly with -CAfile.
openssl req -new -x509 -newkey rsa:2048 -nodes -sha256 -days 3650 \
  -subj '/CN=Lab Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE,pathlen:1' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign' \
  -keyout "$OUT/root/root.key" -out "$OUT/root/root.crt" >/dev/null 2>&1

openssl req -new -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=Lab Intermediate CA' \
  -keyout "$OUT/intermediate/ca.key" \
  -out "$OUT/intermediate/ca.csr" >/dev/null 2>&1

cat > "$OUT/intermediate/ca.ext" <<'EOF'
basicConstraints=critical,CA:TRUE,pathlen:0
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
EOF

openssl x509 -req -in "$OUT/intermediate/ca.csr" \
  -CA "$OUT/root/root.crt" -CAkey "$OUT/root/root.key" -CAcreateserial \
  -days 365 -sha256 -extfile "$OUT/intermediate/ca.ext" \
  -out "$OUT/intermediate/ca.crt" >/dev/null 2>&1

cat > "$OUT/intermediate/openssl.cnf" <<EOF
[ ca ]
default_ca = lab_ca
[ lab_ca ]
dir = $OUT/intermediate
certificate = \$dir/ca.crt
private_key = \$dir/ca.key
database = \$dir/index.txt
new_certs_dir = \$dir/newcerts
serial = \$dir/serial
crlnumber = \$dir/crlnumber
default_md = sha256
default_days = 30
default_crl_days = 30
policy = policy_any
unique_subject = no
copy_extensions = none
[ policy_any ]
commonName = supplied
[ server_a ]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:server-a.test
[ server_b ]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:server-b.test
[ client_only ]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = clientAuth
subjectAltName = DNS:client-only.test
EOF

issue_server() {
  local name="$1" section="$2" cn="$3"
  openssl req -new -newkey rsa:2048 -nodes -sha256 \
    -subj "/CN=$cn" -keyout "$OUT/servers/$name.key" \
    -out "$OUT/servers/$name.csr" >/dev/null 2>&1
  openssl ca -batch -config "$OUT/intermediate/openssl.cnf" \
    -extensions "$section" -in "$OUT/servers/$name.csr" \
    -out "$OUT/servers/$name.crt" -notext >/dev/null 2>&1
}

issue_server server-a server_a server-a.test
issue_server server-b server_b server-b.test
issue_server client-only client_only client-only.test

# A self-signed leaf for TC02: no trusted CA chain.
openssl req -new -x509 -newkey rsa:2048 -nodes -sha256 -days 30 \
  -subj '/CN=rogue.test' -addext 'basicConstraints=critical,CA:FALSE' \
  -addext 'keyUsage=critical,digitalSignature,keyEncipherment' \
  -addext 'extendedKeyUsage=serverAuth' -addext 'subjectAltName=DNS:rogue.test' \
  -keyout "$OUT/servers/rogue.key" -out "$OUT/servers/rogue.crt" >/dev/null 2>&1

# TC10: a correctly signed leaf from a DIFFERENT root, which the client does not trust.
openssl req -new -x509 -newkey rsa:2048 -nodes -sha256 -days 365 \
  -subj '/CN=Other Lab Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE,pathlen:0' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign' \
  -keyout "$OUT/other-ca/root.key" -out "$OUT/other-ca/root.crt" >/dev/null 2>&1
openssl req -new -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=other.test' -keyout "$OUT/other-ca/server.key" \
  -out "$OUT/other-ca/server.csr" >/dev/null 2>&1
cat > "$OUT/other-ca/server.ext" <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:other.test
EOF
openssl x509 -req -in "$OUT/other-ca/server.csr" \
  -CA "$OUT/other-ca/root.crt" -CAkey "$OUT/other-ca/root.key" \
  -CAcreateserial -days 30 -sha256 -extfile "$OUT/other-ca/server.ext" \
  -out "$OUT/other-ca/server.crt" >/dev/null 2>&1

# TC05: change one bit in the DER signature while retaining parseable ASN.1.
openssl x509 -in "$OUT/servers/server-a.crt" -outform DER \
  -out "$OUT/servers/server-a.der"
python3 - "$OUT/servers/server-a.der" "$OUT/servers/tampered.der" <<'PY'
from pathlib import Path
import sys
data = bytearray(Path(sys.argv[1]).read_bytes())
data[-1] ^= 1
Path(sys.argv[2]).write_bytes(data)
PY
openssl x509 -inform DER -in "$OUT/servers/tampered.der" \
  -out "$OUT/servers/tampered.crt"

# Revoke only server-a; server-b remains a positive CRL case.
openssl ca -batch -config "$OUT/intermediate/openssl.cnf" \
  -revoke "$OUT/servers/server-a.crt" >/dev/null 2>&1
openssl ca -gencrl -config "$OUT/intermediate/openssl.cnf" \
  -out "$OUT/intermediate/ca.crl" >/dev/null 2>&1

printf 'Generated by demo/scripts/setup_lab.sh\n' > "$OUT/.lab_marker"
echo "Đã tạo lab tại $OUT"
echo "Chạy: bash demo/scripts/run_tests.sh"
