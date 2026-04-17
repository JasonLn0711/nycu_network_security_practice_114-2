# HW2 Core Explanation Draft

Purpose: keep the report-writing work small by drafting the required explanations before PDF formatting. The final PDF still needs screenshots / excerpts inserted from the saved evidence.

## Assignment Goal And Environment
This experiment builds a mutual TLS connection for a plaintext service by using `stunnel4` as a TLS proxy. The lab uses two Docker containers on the same custom bridge network: `hw2-mtls-client` acts as the client machine, and `hw2-mtls-server` acts as the server machine. The client connects to the server through port `4433`; after a successful mTLS handshake, `stunnel4` forwards the request to a plaintext Python HTTP service running on `127.0.0.1:8000` inside the server container.

Evidence to insert: Docker container / network command excerpt or screenshot.

## Part 1: PKI Construction
The PKI contains one trusted Root CA, one server certificate, one valid client certificate, and one fake client certificate. The trusted Root CA signs both the server certificate and the valid client certificate. The fake client certificate is signed by a separate fake CA, so the server should reject it when `stunnel4` verifies client certificates against the trusted Root CA.

Commands used:

```sh
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Root CA/CN=HW2 Root CA'

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Server/CN=hw2-mtls-server'
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile lab/config/server-ext.cnf

openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Client/CN=hw2-mtls-client'
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256 -extfile lab/config/client-ext.cnf

openssl genrsa -out fake-ca.key 4096
openssl req -x509 -new -nodes -key fake-ca.key -sha256 -days 365 -out fake-ca.crt -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Fake Root CA/CN=HW2 Fake Root CA'

openssl genrsa -out fake-client.key 2048
openssl req -new -key fake-client.key -out fake-client.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Fake Client/CN=hw2-fake-client'
openssl x509 -req -in fake-client.csr -CA fake-ca.crt -CAkey fake-ca.key -CAcreateserial -out fake-client.crt -days 365 -sha256 -extfile lab/config/client-ext.cnf
```

Verification result:

```text
server.crt: OK
client.crt: OK
fake-client.crt: verification failed against ca.crt
fake-client.crt: OK against fake-ca.crt
```

This confirms that the server and valid client certificates belong to the trusted PKI, while the fake client certificate does not belong to the trusted Root CA.

Evidence to insert: `lab/logs/phase2-pki-commands-2026-04-16.log`.

## Part 2: Service Configuration
The server runs a plaintext backend using `python3 -m http.server 8000`. This backend does not provide TLS by itself. `stunnel4` provides the mTLS layer by accepting external connections on `0.0.0.0:4433`, using the server certificate, trusting only `ca.crt`, and requiring clients to provide a certificate.

Exact `stunnel.conf`:

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

The important security setting is `verify = 2`, which requires a client certificate and rejects clients that do not present a certificate trusted by `CAfile`.

Evidence to insert: `lab/config/stunnel.conf`, plus backend / stunnel startup evidence if space allows.

## Part 3: Connection Testing
### Scenario 1: Valid Client Certificate
The valid client test uses `ca.crt`, `client.crt`, and `client.key`. The `curl -v` output shows that the server requests a client certificate, the server certificate verifies successfully, and the HTTP request receives `HTTP/1.0 200 OK`. This means the client trusts the server certificate and the server accepts the client certificate.

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt --cert /hw2/certs/client.crt --key /hw2/certs/client.key https://hw2-mtls-server:4433/
```

Evidence excerpt:

```text
TLS handshake, Request CERT (13)
SSL certificate verify ok.
HTTP/1.0 200 OK
HW2 mTLS backend is reachable through stunnel.
docker/curl exit code: 0
```

Evidence to insert: `lab/logs/phase5-success-curl-2026-04-16.log`.

### Scenario 2: No Client Certificate
The no-client-certificate test uses only the Root CA to verify the server. The server still requests a client certificate, but the client does not provide one. Because `stunnel4` requires client authentication, the connection fails with a `certificate required` TLS alert.

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt https://hw2-mtls-server:4433/
```

Evidence excerpt:

```text
TLS handshake, Request CERT (13)
tlsv13 alert certificate required
curl: (56) OpenSSL SSL_read
docker/curl exit code: 56
```

Evidence to insert: `lab/logs/phase4-failure-no-client-cert-2026-04-16.log`.

### Scenario 3: Unauthorized Client Certificate
The fake-client test provides a client certificate, but that certificate was signed by the fake CA instead of the trusted Root CA. The client can still verify the server certificate, but the server rejects the fake client certificate because it is not trusted by `CAfile = /hw2/certs/ca.crt`.

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt --cert /hw2/certs/fake-client.crt --key /hw2/certs/fake-client.key https://hw2-mtls-server:4433/
```

Evidence excerpt:

```text
TLS handshake, Request CERT (13)
tlsv1 alert unknown ca
curl: (56) OpenSSL SSL_read
docker/curl exit code: 56
```

Server-side support:

```text
Rejected by CERT
certificate verify failed
```

Evidence to insert: `lab/logs/phase4-failure-fake-client-cert-2026-04-16.log` and `lab/logs/phase4-stunnel-failures-2026-04-16.log`.

## Part 4: Packet Analysis
The successful mTLS run was captured with `tcpdump` inside the server container while the valid-client `curl -v` command was executed. The packet summary shows traffic between `172.22.0.3` and `172.22.0.2` on port `4433`, which is the `stunnel4` listening port. The capture contains 21 packets and 0 kernel drops, so it captured the successful connection cleanly.

Evidence excerpt:

```text
172.22.0.3.58560 > 172.22.0.2.4433
21 packets captured
21 packets received by filter
0 packets dropped by kernel
```

Evidence to insert: `lab/captures/success-mtls-2026-04-16.pcap`, `lab/logs/phase5-success-pcap-summary-2026-04-16.log`, and `lab/logs/phase5-tcpdump-capture-2026-04-16.log`.

## Conclusion
The experiment demonstrates that `stunnel4` can wrap a plaintext HTTP backend with mutual TLS. The valid client certificate succeeds and reaches the backend, while a missing client certificate and a fake client certificate are both rejected. The packet capture confirms that the successful connection used the TLS proxy port `4433`, not direct plaintext access to the backend service.

## Next Assembly Step
This draft has been superseded by `near-final-report-draft.md`, `final-report.tex`, and the generated official PDF `513559004_report.pdf`.
