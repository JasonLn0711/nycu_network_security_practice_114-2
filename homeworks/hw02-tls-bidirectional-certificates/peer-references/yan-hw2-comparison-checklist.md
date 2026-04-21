# Yan HW2 Comparison Checklist

Purpose: use Yan's HW2 report as a private peer-learning reference for improving understanding of mutual TLS evidence, not as source material for copying.

Related files:

- Peer report: `yan-hw2-mtls-report-2026-04-19.pdf`
- Your submitted report: `../report/513559004_report.pdf`
- Your evidence map: `../report/evidence-map.md`
- Durable concept note: `../../../../planning-everything-track/data/knowledge/cybersecurity/network-security/concept-notes/mutual-tls-stunnel-client-authentication.md`

## Integrity Boundary

- [ ] Read for rubric coverage and security reasoning only.
- [ ] Do not copy sentences, screenshots, table layout, or command formatting.
- [ ] Validate any useful idea against your own logs, config, report, or packet capture before promoting it.

## Rubric Comparison

| Area | What to compare | Yan's useful signal | Your current strength | Next learning action |
| --- | --- | --- | --- | --- |
| PKI construction | Root CA, server cert, client cert, fake CA, fake client cert, SAN/EKU files, and verification commands | Clear command sequence for CA, server, client, and fake-client material; includes server/client extension files | Your archive keeps exact commands, certificate verification results, and fake-client trust-chain evidence | Be able to explain why SAN and EKU matter separately from the certificate being signed |
| `stunnel.conf` | Exact listener, backend, server cert/key, trusted CA, and client-verification setting | Useful explanation of `verify=1` vs `verify=2`, with `verify=2` framed as the strict mTLS setting | Your report has a concise exact config and directly ties `verify = 2` plus `CAfile` to client authentication | Write a 3-sentence explanation of why encryption alone is not enough without client-certificate verification |
| Success test | Valid client certificate reaches the protected backend and returns HTTP success | Shows the intended successful `curl -v` path | Your report records `HTTP/1.0 200 OK`, hostname verification, backend reachability, and command context | Compare hostname/SAN handling when using `server`, `localhost`, `--resolve`, or a Docker service name |
| No-certificate failure | Client trusts server but does not present a client cert | Shows the required no-client-certificate negative scenario | Your report records both client-side TLS alert and server-side rejection evidence | Practice recognizing `certificate required` as an authorization failure, not a server-authentication failure |
| Fake-certificate failure | Client presents a cert signed by an untrusted CA | Shows the required unauthorized-client negative scenario | Your report separates fake CA verification from trusted Root CA verification and records `unknown ca` | Explain why "has a certificate" is not equivalent to "is authorized" |
| Packet analysis | Evidence from successful mTLS traffic | Wireshark-focused packet review highlights TLS filtering, Certificate Request, Distinguished Names, and the client certificate packet | Your report has reproducible `tcpdump` capture evidence with packet counts and the correct TLS proxy port | Open your own capture in Wireshark and locate the Certificate Request if you want stronger packet-level confidence |
| Security explanation | mTLS vs one-way TLS, transport-layer access control, and secret handling | Helpful high-level explanation of why mTLS is stronger than one-way TLS; includes a practical note about container secret persistence | Your report is stronger on reproducibility, exact failure evidence, and concise security interpretation per scenario | Promote only durable lessons, such as how to prove mTLS client authentication from packets, into the concept note |

## What To Do Next

- [ ] Spend one focused block comparing the two reports against the rubric, not against style preferences.
- [ ] Re-open your own packet capture in Wireshark and find the Certificate Request / accepted CA clue if time allows.
- [ ] Add one small update to the durable mTLS concept note only if the packet-analysis comparison changes how you would explain the mechanism later.
- [ ] Keep the peer report as a reference artifact; do not turn it into a template.
