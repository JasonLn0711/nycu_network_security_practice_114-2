# Network Security HW2 - mTLS With Bidirectional Certificates

## Agent Search Summary

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Assignment: `HW2. TLS Connection with Bidirectional Certificates`
- Name: `Jason Chia-Sheng Lin`
- Student ID: `513559004`
- Organization: `Institute of Biophotonics, NYCU`
- Due: `2026-04-25 23:59`
- Status: submitted and confirmed in LMS on `2026-04-17`; no W17 action remains unless the LMS or instructor reports a concrete issue
- Submission file: `report/513559004_report.pdf`
- Planning/project locator from the course repo root: `../planning-everything-track/data/projects/2026-04-network-security-hw2-tls-bidirectional-certificates.md`
- Durable concept note from the course repo root: `../planning-everything-track/data/knowledge/cybersecurity/network-security/concept-notes/mutual-tls-stunnel-client-authentication.md`

## What This Project Proves

This homework builds a two-container mutual TLS lab where `stunnel4` protects a plaintext Python HTTP backend. The server requires a client certificate signed by the trusted Root CA before forwarding traffic to `127.0.0.1:8000`.

Verified results:

- Valid client certificate succeeds with `HTTP/1.0 200 OK`.
- No client certificate fails with `tlsv13 alert certificate required`.
- Fake client certificate signed by an untrusted CA fails with `tlsv1 alert unknown ca`.
- Packet capture on port `4433` recorded 22 packets with 0 kernel drops.

## Folder Map

| Path | Purpose | Git policy |
| --- | --- | --- |
| `hw2-spec.pdf` | Assignment PDF copied into the project | tracked source asset |
| `docker-lab-checklist.md` | Reproducible lab workflow and current state | tracked |
| `lab/config/` | Reproducible `stunnel4` and certificate extension config | tracked |
| `lab/logs/` | Text evidence logs for topology, PKI, `curl -v`, `stunnel4`, and packet-capture summaries | tracked |
| `lab/certs/` | Generated certs, CSRs, serials, and private keys | ignored |
| `lab/captures/` | Raw packet captures | ignored |
| `report/core-explanation-draft.md` | Early report explanation draft | tracked |
| `report/near-final-report-draft.md` | Markdown draft with selected excerpts | tracked |
| `report/final-report.tex` | Canonical report source | tracked |
| `report/final-report.pdf` | Generated PDF from LaTeX | ignored |
| `report/513559004_report.pdf` | Official submitted PDF artifact | tracked |
| `report/evidence-map.md` | Map from rubric requirements to evidence files | tracked |
| `report/README.md` | Report build and submission instructions | tracked |

## Canonical Build Command

Run from `report/`:

```sh
xelatex -interaction=nonstopmode -halt-on-error final-report.tex
xelatex -interaction=nonstopmode -halt-on-error final-report.tex
cp final-report.pdf 513559004_report.pdf
```

## Safety Rules

- Do not commit private keys, generated certs, CSRs, serial files, or `.pcap` captures from `lab/`.
- Keep text logs and configs because they make the homework auditable without rerunning the lab.
- Do not rerun the lab unless the final PDF proofread reveals a concrete evidence gap.
- Keep canonical homework archive material here in `homeworks/`; keep reusable mTLS concepts in the planning repo knowledge system.
- If the TA requires literal screenshots, use the existing logs/pcap to generate screenshots instead of changing the experiment.

## Next Action

Submission was recorded from the `2026-04-17` daily note: LMS status `Submitted for grading`, file `513559004_report.pdf`, last modified `Friday, 17 April 2026, 10:43 AM`.
