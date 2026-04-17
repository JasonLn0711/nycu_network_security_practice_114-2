# HW2 Report Evidence Map

Purpose: map the completed Docker mTLS lab artifacts to report sections without committing generated private keys, generated certificates, or packet captures.

## Ground Rules
- Treat `lab/config/` and `lab/logs/` as searchable, non-secret evidence that can be kept in Git.
- Treat `lab/certs/` and `lab/captures/` as generated local evidence only; they are intentionally ignored by Git.
- Do not paste private keys into the report.
- Use short command excerpts, screenshots, and concise explanations instead of dumping entire logs.
- If a screenshot is missing, do not rerun the lab first; check whether the saved log or pcap already proves the point.

## Report Skeleton
1. Assignment goal and environment
2. Topology and traffic flow
3. Certificate authority and certificate design
4. Server backend and `stunnel4` configuration
5. Valid-client success test
6. No-client-certificate failure test
7. Fake-client-certificate failure test
8. Packet capture evidence
9. Short conclusion

## Topology Explanation
Use this as the plain architecture sentence in the report:

`hw2-mtls-client` connects to `hw2-mtls-server:4433`; `stunnel4` on the server terminates mutual TLS, requires a client certificate signed by the Root CA, and then forwards accepted traffic to the plaintext Python backend on `127.0.0.1:8000`.

## Evidence Inventory
| Report slot | Local artifact | What it proves | Report action |
| --- | --- | --- | --- |
| Environment | `docker network inspect hw2-mtls-net`; `lab/logs/phase1-container-topology-2026-04-17.log` | Two Docker containers were used instead of VMs, which the assignment allows. | Add one topology screenshot or a short command/output excerpt. |
| PKI setup | `lab/logs/phase2-pki-commands-2026-04-17.log` | Root CA signs `server.crt` and `client.crt`; fake client is signed by a different fake CA. | Screenshot or excerpt the command block and verification results. |
| Server config | `lab/config/stunnel.conf` | `stunnel4` listens on `4433`, forwards to local backend `8000`, and requires client cert verification. | Paste the config snippet directly into the report. |
| Backend service | `lab/logs/phase3-backend-2026-04-17.log` | Plain backend exists behind the TLS proxy. | Mention briefly; screenshot only if the instructor expects process evidence. |
| Success test | `lab/logs/phase5-success-curl-2026-04-17.log` | Valid client cert completes mTLS and receives HTTP `200 OK`. | Screenshot the important `curl -v` lines. |
| No-cert failure | `lab/logs/phase4-failure-no-client-cert-2026-04-17.log` | Server requests a cert; client without cert fails with `certificate required`. | Screenshot the TLS alert and curl exit message. |
| Fake-cert failure | `lab/logs/phase4-failure-fake-client-cert-2026-04-17.log` | Client cert signed by the wrong CA is rejected. | Screenshot the `unknown ca` TLS alert. |
| Server-side rejection | `lab/logs/phase4-stunnel-failures-2026-04-17.log` | `stunnel4` records both rejected cases from the server perspective. | Use as supporting evidence after the two failure screenshots. |
| Packet capture | `lab/captures/success-mtls-2026-04-17.pcap` and `lab/logs/phase5-success-pcap-summary-2026-04-17.log` | Traffic was captured on port `4433` during successful mTLS. | Open the pcap in Wireshark or include readable `tcpdump` output. |
| Capture health | `lab/logs/phase5-tcpdump-capture-2026-04-17.log` | Capture completed cleanly with no kernel drops. | Include the `22 packets captured` / `0 packets dropped` lines if space allows. |

## Verified Excerpts To Use
PKI verification:

```text
server.crt: OK
client.crt: OK
error 20 at 0 depth lookup: unable to get local issuer certificate
fake-client.crt: OK
```

`stunnel.conf`:

```text
foreground = yes
debug = info
output = /hw2/logs/stunnel.log
pid = /hw2/logs/stunnel.pid

[mtls-http]
accept = 0.0.0.0:4433
connect = 127.0.0.1:8000
cert = /hw2/certs/server.crt
key = /hw2/certs/server.key
CAfile = /hw2/certs/ca.crt
verify = 2
```

Valid-client success:

```text
TLS handshake, Request CERT (13)
SSL certificate verify ok.
HTTP/1.0 200 OK
```

No-client-certificate failure:

```text
TLS handshake, Request CERT (13)
tlsv13 alert certificate required
curl: (56) OpenSSL SSL_read
```

Fake-client-certificate failure:

```text
TLS handshake, Request CERT (13)
tlsv1 alert unknown ca
curl: (56) OpenSSL SSL_read
```

Server-side rejection:

```text
peer did not return a certificate
Rejected by CERT
certificate verify failed
```

Packet capture:

```text
172.18.0.3.58836 > 172.18.0.2.4433
22 packets captured
22 packets received by filter
0 packets dropped by kernel
```

## Screenshot Checklist
- [x] Docker topology / container names or a short command excerpt selected
- [x] PKI command and verification excerpt selected
- [x] `stunnel.conf` selected
- [x] Valid-client `curl -v` success showing `Request CERT`, certificate verification, and `HTTP/1.0 200 OK` selected
- [x] No-client-cert failure showing `certificate required` selected
- [x] Fake-client-cert failure showing `unknown ca` selected
- [x] Server-side `stunnel4` rejection log selected
- [x] Packet capture view from Wireshark or readable `tcpdump` selected

## Next Bounded Block
The near-final report draft now exists at `report/near-final-report-draft.md`. Use it as the base for the final PDF.

The professional PDF source and compiled draft now exist at `report/final-report.tex` and `report/final-report.pdf`.

The official submission PDF now exists at `report/513559004_report.pdf`.

Next stop condition: no action unless the LMS or instructor reports a concrete issue. `report/513559004_report.pdf` was submitted and confirmed in LMS on `2026-04-17`; do not rerun the lab or reopen the report.
