#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$BASE_DIR/out"
[[ -f "$OUT/.lab_marker" ]] || { echo 'Chạy make demo trước.' >&2; exit 1; }

ROOT="$OUT/root/root.crt"
INTERMEDIATE="$OUT/intermediate/ca.crt"
SERVERS="$OUT/servers"
RESULTS="$OUT/results.tsv"
printf 'id\texpected\tobserved\texit_code\tmessage\n' > "$RESULTS"

run_case() {
  local id="$1" expected="$2" marker="$3"
  shift 3
  local output status observed message
  set +e
  output=$("$@" 2>&1)
  status=$?
  set -e
  if [[ "$status" -eq 0 ]]; then observed=PASS; else observed=FAIL; fi
  message=$(printf '%s' "$output" | tr '\n\t' '  ' | cut -c1-300)
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$expected" "$observed" "$status" "$message" >> "$RESULTS"
  printf '%-5s expected=%-4s observed=%-4s exit=%s | %s\n' "$id" "$expected" "$observed" "$status" "$message"
  if [[ "$observed" != "$expected" ]]; then
    echo "$id: kết quả lệch kỳ vọng" >&2
    return 1
  fi
  if [[ -n "$marker" && "$output" != *"$marker"* ]]; then
    echo "$id: thất bại không đúng nguyên nhân dự kiến: $marker" >&2
    return 1
  fi
}

COMMON=(-CAfile "$ROOT" -untrusted "$INTERMEDIATE" -purpose sslserver)
run_case TC01 PASS 'OK' openssl verify "${COMMON[@]}" \
  -verify_hostname server-a.test "$SERVERS/server-a.crt"
run_case TC02 FAIL 'self-signed certificate' openssl verify \
  -CAfile "$ROOT" -purpose sslserver -verify_hostname rogue.test "$SERVERS/rogue.crt"
FUTURE_TIME=$(($(date +%s) + 40 * 86400))
run_case TC03 FAIL 'certificate has expired' openssl verify "${COMMON[@]}" \
  -attime "$FUTURE_TIME" -verify_hostname server-a.test "$SERVERS/server-a.crt"
run_case TC04 FAIL 'hostname mismatch' openssl verify "${COMMON[@]}" \
  -verify_hostname wrong.test "$SERVERS/server-a.crt"
run_case TC05 FAIL 'certificate signature failure' openssl verify "${COMMON[@]}" \
  -verify_hostname server-a.test "$SERVERS/tampered.crt"
run_case TC06 FAIL 'unable to get local issuer certificate' openssl verify \
  -CAfile "$ROOT" -purpose sslserver -verify_hostname server-a.test "$SERVERS/server-a.crt"
run_case TC07 FAIL 'certificate revoked' openssl verify "${COMMON[@]}" \
  -CRLfile "$OUT/intermediate/ca.crl" -crl_check \
  -verify_hostname server-a.test "$SERVERS/server-a.crt"
run_case TC08 FAIL 'unsuitable certificate purpose' openssl verify "${COMMON[@]}" \
  -verify_hostname client-only.test "$SERVERS/client-only.crt"
run_case TC09 PASS 'OK' openssl verify "${COMMON[@]}" \
  -CRLfile "$OUT/intermediate/ca.crl" -crl_check \
  -verify_hostname server-b.test "$SERVERS/server-b.crt"
run_case TC10 FAIL 'unable to get local issuer certificate' openssl verify \
  -CAfile "$ROOT" -purpose sslserver -verify_hostname other.test \
  "$OUT/other-ca/server.crt"

echo "Bảng kết quả: $RESULTS"
