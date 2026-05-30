#!/usr/bin/env bash
set -euo pipefail

student_id="${1:-513559004}"
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_root="$repo_dir/submission/dry-run/HW6_${student_id}"
zip_path="$repo_dir/submission/dry-run/HW6_${student_id}.zip"
report_pdf="$package_root/${student_id}_report.pdf"

rm -rf "$package_root" "$zip_path"
mkdir -p "$package_root/Extension"

cp "$repo_dir/solution/Extension/manifest.json" "$package_root/Extension/manifest.json"
cp "$repo_dir/solution/Extension/background.js" "$package_root/Extension/background.js"

STUDENT_ID="$student_id" REPORT_PDF="$report_pdf" python3 - <<'PY'
from __future__ import annotations

import os
from pathlib import Path

student_id = os.environ["STUDENT_ID"]
output = Path(os.environ["REPORT_PDF"])
text = (
    f"HW4 Web Traffic Sniffer dry-run report for {student_id}. "
    "This placeholder proves package structure and PDF readability only; "
    "replace it with the final evidence-backed report before LMS upload."
)

objects: list[bytes] = []
objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("ascii")
objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")

pdf = bytearray(b"%PDF-1.4\n")
offsets = [0]
for index, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{index} 0 obj\n".encode("ascii"))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref_offset = len(pdf)
pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
pdf.extend(b"0000000000 65535 f \n")
for offset in offsets[1:]:
    pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
pdf.extend(
    f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
)

output.write_bytes(pdf)
PY

(
  cd "$repo_dir/submission/dry-run"
  zip -qr "HW6_${student_id}.zip" "HW6_${student_id}"
)

python3 "$repo_dir/scripts/validate_submission.py" \
  --student-id "$student_id" \
  --package-dir "$package_root" \
  --zip "$zip_path"

echo "Dry-run package built and validated:"
echo "$zip_path"
