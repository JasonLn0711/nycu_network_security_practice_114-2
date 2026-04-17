# HW2: TLS Connection with Bidirectional Certificates

- Name: Jason Chia-Sheng Lin
- Student ID: 513559004
- Organization: Institute of Biophotonics, NYCU
- Course: Network Security Practices - Attack and Defense
- Date: 2026-04-17
- Output target: `513559004_report.pdf`

## Assignment Goal

This experiment builds a mutual TLS connection for a plaintext HTTP service. The plaintext backend runs on the server container at `127.0.0.1:8000`. `stunnel4` listens on port `4433`, terminates mutual TLS, requires a trusted client certificate, and forwards accepted traffic to the backend.

## Environment And Topology

The experiment uses two Docker containers on one custom bridge network, which satisfies the assignment requirement to use two separate VMs or containers.

```text
Docker network: hw2-mtls-net
Server container: hw2-mtls-server 172.18.0.2
Client container: hw2-mtls-client 172.18.0.3
Traffic path: client -> server:4433 -> stunnel4 -> 127.0.0.1:8000 Python backend
```

Topology check:

```text
172.18.0.2      hw2-mtls-server
```

Evidence source: `lab/logs/phase1-container-topology-2026-04-17.log`

## Part 1: PKI Construction

The PKI contains one trusted Root CA, one server certificate, one valid client certificate, and one unauthorized client certificate. The trusted Root CA signs the server and valid client certificates. A separate fake CA signs the unauthorized client certificate, so the server rejects it when validating against the trusted Root CA.

Commands used:

```sh
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Root CA/CN=HW2 Root CA'

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Server/CN=hw2-mtls-server'
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile ../config/server-ext.cnf

openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Client/CN=hw2-mtls-client'
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256 -extfile ../config/client-ext.cnf

openssl genrsa -out fake-ca.key 4096
openssl req -x509 -new -nodes -key fake-ca.key -sha256 -days 365 -out fake-ca.crt -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Fake Root CA/CN=HW2 Fake Root CA'

openssl genrsa -out fake-client.key 2048
openssl req -new -key fake-client.key -out fake-client.csr -subj '/C=TW/ST=Taiwan/L=Hsinchu/O=NYCU Network Security HW2/OU=Fake Client/CN=hw2-fake-client'
openssl x509 -req -in fake-client.csr -CA fake-ca.crt -CAkey fake-ca.key -CAcreateserial -out fake-client.crt -days 365 -sha256 -extfile ../config/client-ext.cnf
```

Certificate extension files:

```text
# server-ext.cnf
subjectAltName = DNS:hw2-mtls-server
extendedKeyUsage = serverAuth
keyUsage = digitalSignature,keyEncipherment

# client-ext.cnf
extendedKeyUsage = clientAuth
keyUsage = digitalSignature,keyEncipherment
```

Verification excerpt:

```text
server.crt: OK
client.crt: OK
error fake-client.crt: verification failed
fake-client.crt: OK
```

This confirms that `server.crt` and `client.crt` verify against the trusted Root CA, while `fake-client.crt` fails against the trusted Root CA and only verifies against `fake-ca.crt`.

Evidence source: `lab/logs/phase2-pki-commands-2026-04-17.log`

## Part 2: Service Configuration

The server runs a plaintext backend:

```sh
python3 -m http.server 8000
```

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

The important setting is `verify = 2`, which requires the client to present a certificate trusted by `CAfile = /hw2/certs/ca.crt`.

Evidence sources:
- `lab/config/stunnel.conf`
- `lab/logs/phase3-backend-2026-04-17.log`
- `lab/logs/phase3-stunnel-2026-04-17.log`

## Part 3: Connection Testing

### Scenario 1: Success With Valid Client Certificate

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt --cert /hw2/certs/client.crt --key /hw2/certs/client.key https://hw2-mtls-server:4433/
```

Selected output:

```text
TLSv1.3 (IN), TLS handshake, Request CERT (13)
subjectAltName: host "hw2-mtls-server" matched cert's "hw2-mtls-server"
SSL certificate verify ok.
HTTP/1.0 200 OK
HW2 mTLS backend is reachable through stunnel.
docker/curl exit code: 0
```

Interpretation: the server requested a client certificate, the client verified the server certificate, the server accepted the valid client certificate, and the request reached the backend.

Evidence source: `lab/logs/phase5-success-curl-2026-04-17.log`

### Scenario 2: Failure Without Client Certificate

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt https://hw2-mtls-server:4433/
```

Selected output:

```text
TLSv1.3 (IN), TLS handshake, Request CERT (13)
TLS alert, unknown (628)
tlsv13 alert certificate required
curl: (56) OpenSSL SSL_read
docker/curl exit code: 56
```

Server-side support:

```text
Peer certificate required
peer did not return a certificate
```

Interpretation: the server required client authentication, but the client did not provide a certificate, so the TLS connection failed.

Evidence sources:
- `lab/logs/phase4-failure-no-client-cert-2026-04-17.log`
- `lab/logs/phase4-stunnel-failures-2026-04-17.log`

### Scenario 3: Failure With Unauthorized Client Certificate

Command:

```sh
curl -v --cacert /hw2/certs/ca.crt --cert /hw2/certs/fake-client.crt --key /hw2/certs/fake-client.key https://hw2-mtls-server:4433/
```

Selected output:

```text
TLSv1.3 (IN), TLS handshake, Request CERT (13)
TLS alert, unknown CA (560)
tlsv1 alert unknown ca
curl: (56) OpenSSL SSL_read
docker/curl exit code: 56
```

Server-side support:

```text
CERT: Pre-verification error: unable to get local issuer certificate
Rejected by CERT at depth=0: C=TW, ST=Taiwan, L=Hsinchu, O=NYCU Network Security HW2, OU=Fake Client, CN=hw2-fake-client
certificate verify failed
```

Interpretation: the client presented a certificate, but it was signed by the fake CA instead of the trusted Root CA. `stunnel4` rejected it during client certificate verification.

Evidence sources:
- `lab/logs/phase4-failure-fake-client-cert-2026-04-17.log`
- `lab/logs/phase4-stunnel-failures-2026-04-17.log`

## Part 4: Packet Analysis

Packet capture was run inside the server container during a successful valid-client connection.

Readable `tcpdump` excerpt:

```text
172.18.0.3.58836 > 172.18.0.2.4433: Flags [S]
172.18.0.2.4433 > 172.18.0.3.58836: Flags [S.]
172.18.0.3.58836 > 172.18.0.2.4433: Flags [P.], length 517
172.18.0.2.4433 > 172.18.0.3.58836: Flags [P.], length 3561
172.18.0.3.58836 > 172.18.0.2.4433: Flags [P.], length 3172
```

Capture health:

```text
22 packets captured
22 packets received by filter
0 packets dropped by kernel
```

Interpretation: the packet capture shows traffic between the client container `172.18.0.3` and server container `172.18.0.2` on port `4433`, which is the `stunnel4` TLS proxy port. The packet count and zero-drop summary show that the successful mTLS connection was captured cleanly.

Evidence sources:
- `lab/captures/success-mtls-2026-04-17.pcap`
- `lab/logs/phase5-success-pcap-summary-2026-04-17.log`
- `lab/logs/phase5-tcpdump-capture-2026-04-17.log`

## Conclusion

The experiment successfully wrapped a plaintext Python HTTP backend with mutual TLS using `stunnel4`. The valid client certificate completed the handshake and received `HTTP/1.0 200 OK`. A client with no certificate failed with `certificate required`, and a client using a certificate signed by an untrusted fake CA failed with `unknown ca`. The packet capture confirms the successful mTLS traffic flowed through server port `4433`.

## Final PDF Assembly Checklist

- [x] Fill in the student ID.
- [ ] Insert or screenshot the PKI command/verification excerpt.
- [ ] Insert or screenshot the exact `stunnel.conf`.
- [ ] Insert or screenshot valid-client `curl -v` output showing `Request CERT`, `SSL certificate verify ok.`, and `HTTP/1.0 200 OK`.
- [ ] Insert or screenshot no-client-cert `curl -v` output showing `certificate required`.
- [ ] Insert or screenshot fake-client-cert `curl -v` output showing `unknown ca`.
- [ ] Insert or screenshot server-side rejection lines from `stunnel.log`.
- [ ] Insert a Wireshark view of `lab/captures/success-mtls-2026-04-17.pcap` or a readable `tcpdump` screenshot from `phase5-success-pcap-summary-2026-04-17.log`.
- [x] Export as `513559004_report.pdf`.
