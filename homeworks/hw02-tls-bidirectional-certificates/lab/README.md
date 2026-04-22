# HW2 Lab Evidence

This folder keeps the reproducible mutual TLS lab material for HW2.

| Path | Purpose | Git Policy |
| --- | --- | --- |
| [config/](config/) | `stunnel4` and certificate-extension config that can be reused to rebuild the lab. | tracked |
| [logs/](logs/) | Text evidence for topology, PKI commands, `curl -v`, `stunnel4`, and packet-capture summaries. | tracked |
| `certs/` | Generated certificates, CSRs, serials, and private keys from the lab run. | ignored |
| `captures/` | Raw packet captures from the lab run. | ignored |

Use [../docker-lab-checklist.md](../docker-lab-checklist.md) as the rebuild workflow and [../report/evidence-map.md](../report/evidence-map.md) as the evidence-to-report map. Do not treat generated lab keys as reusable credentials.
