# Standards Alignment

## Purpose

This note records how Sentinel was checked against internationally recognized
security references. It is a refinement guide, not a claim that the course
scanner is production antivirus software.

## Source Baseline

| Source | Why it matters for this project | Sentinel refinement |
| --- | --- | --- |
| [EICAR Anti-Malware Testfile](https://www.eicar.org/download-anti-malware-testfile/) | EICAR/CARO provide the widely used safe anti-malware test file. The official page defines the 68-byte test string and states that it is not a real virus. | `signatures/malware-signatures.json` stores the EICAR MD5, SHA-256, and hex-pattern matchers. The Rust `prepare-eicar-demo` command generates the 68-byte file in the demo tree at runtime so the live demo detects EICAR without committing the file. |
| [NIST SP 800-83 Rev. 1](https://csrc.nist.gov/pubs/sp/800/83/r1/final) | NIST frames malware as a common host threat and emphasizes prevention plus response readiness. | Sentinel stays read-only, records evidence, avoids live malware, and separates confirmed signature detections from weaker heuristic findings. |
| [NIST Cybersecurity Framework 2.0 overview](https://csrc.nist.gov/pubs/sp/1299/final) | CSF 2.0 is a current NIST reference for organizing cybersecurity work and links to the CSF 2.0 specification/resources. | The project is positioned mainly under `Detect` evidence, with `Govern`/`Identify` decisions captured in traceability and submission-package notes. |
| [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | OWASP recommends defense in depth for untrusted files, including anti-malware/sandbox checks, file size limits, safe storage, and not trusting metadata alone. | Sentinel documents that it is one static scan control, not a complete upload-security system. It keeps explicit-target scans, bounded heuristic sampling, and no execute/delete/quarantine behavior. |
| [MITRE ATT&CK T1055.002 Portable Executable Injection](https://attack.mitre.org/techniques/T1055/002/) | MITRE documents process-injection API sequences such as `VirtualAllocEx`, `WriteProcessMemory`, and `CreateRemoteThread`. | Sentinel's heuristic fixture uses these API-name indicators only as `suspicious`, never as confirmed malware without an exact signature match. |

## Accepted Refinements

- Use the official EICAR safe anti-malware test file for the final demo because
  the instructor wording asks for EICAR.
- Generate the EICAR demo fixture at runtime with Rust.
- Do not commit or export the generated literal EICAR file.
- Preserve a read-only scanner posture: no execution, no deletion, no quarantine,
  no upload, and no network action.
- Keep symbolic links skipped by default so scans remain inside the explicit
  target tree.
- Explain that heuristic indicators are low-confidence signals and should not be
  reported as confirmed malware.

## Evidence Links

- EICAR demo signature: `signatures/malware-signatures.json`
- EICAR reference-hash profile: `signatures/eicar-reference-signature.json`
- Core safety checks: `scripts/check_release.py`
- Requirements traceability: `docs/requirements-traceability.md`
- Demo evidence manifest: `reports/demo-evidence-manifest.json`
