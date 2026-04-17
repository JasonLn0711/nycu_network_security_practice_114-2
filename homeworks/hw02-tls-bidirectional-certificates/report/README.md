# HW2 Report Assets

## Status

- Student ID: `513559004`
- Name: `Jason Chia-Sheng Lin`
- Organization: `Institute of Biophotonics, NYCU`
- Canonical source: `final-report.tex`
- Generated proof PDF: `final-report.pdf`
- Official submission filename: `513559004_report.pdf`
- Current state: PDF generated, text-checked, and submitted/confirmed in LMS on `2026-04-17`

## Build

Run from this folder:

```sh
xelatex -interaction=nonstopmode -halt-on-error final-report.tex
xelatex -interaction=nonstopmode -halt-on-error final-report.tex
cp final-report.pdf 513559004_report.pdf
```

## Verification Checklist

The compiled PDF should contain:

- `Jason Chia-Sheng Lin`
- `Student ID: 513559004`
- `Institute of Biophotonics, NYCU`
- all required `openssl` commands
- exact `stunnel.conf`
- valid-client `curl -v` success with `HTTP/1.0 200 OK`
- no-client-cert failure with `certificate required`
- fake-client-cert failure with `unknown ca`
- packet capture evidence on port `4433`
- `22 packets captured`
- `0 packets dropped by kernel`

Useful text check:

```sh
pdftotext 513559004_report.pdf - | rg 'Jason Chia-Sheng Lin|513559004|Institute of Biophotonics, NYCU|openssl|verify = 2|HTTP/1.0 200 OK|certificate required|unknown ca|22 packets captured|0 packets dropped'
```

## File Policy

- Track `final-report.tex`, `near-final-report-draft.md`, `core-explanation-draft.md`, `evidence-map.md`, and this README.
- Track the submitted `513559004_report.pdf` as the official archive artifact.
- Track non-secret text evidence logs and reproducible configs under `../lab/logs/` and `../lab/config/`.
- Ignore generated LaTeX byproducts, rebuild PDFs, private keys, generated cert/CSR/serial files, and raw packet captures.
