# HW2 Docker Lab Checklist

Use this as the bounded execution checklist for the mTLS homework.

The goal is not to build a beautiful lab system. The goal is to produce reproducible evidence for the required report.

## Decision
- Primary environment: two Docker containers on one custom bridge network
- Containers:
  - `hw2-mtls-server`
  - `hw2-mtls-client`
- Host evidence capture: `tcpdump` on the Docker bridge if practical
- Fallback: capture inside the server container if host bridge capture is too annoying

## Artifact Layout
- `lab/`: local working folder for configs, certs, logs, and packet captures
- `lab/certs/`: Root CA, server cert, valid client cert, and fake client cert materials
- `lab/config/`: `stunnel.conf` and any copied container config
- `lab/logs/`: copied `curl -v` outputs and service logs
- `lab/captures/`: `pcap` files and screenshots for the report
- `report/`: final report draft assets

Keep private keys out of Git if the lab folder is ever committed. For this homework, the commands and screenshots matter more than preserving live keys.

## Phase 1: Container Topology
Target outcome: two reachable containers on one network.

```sh
docker network create hw2-mtls-net

docker run -dit --name hw2-mtls-server --network hw2-mtls-net ubuntu:24.04 bash
docker run -dit --name hw2-mtls-client --network hw2-mtls-net ubuntu:24.04 bash

docker exec hw2-mtls-server bash -lc 'apt-get update && apt-get install -y openssl stunnel4 python3 curl tcpdump ca-certificates iproute2'
docker exec hw2-mtls-client bash -lc 'apt-get update && apt-get install -y openssl curl tcpdump ca-certificates iproute2'

docker exec hw2-mtls-client bash -lc 'getent hosts hw2-mtls-server'
```

Stop condition: client can resolve `hw2-mtls-server`.

## Phase 2: PKI Construction
Target outcome: one Root CA, one server cert, one valid client cert, and one fake client cert signed by a different CA.

Evidence required for report:
- all `openssl` commands
- generated file names
- short explanation of which CA signs which cert

Planned files:
- `ca.key`, `ca.crt`
- `server.key`, `server.csr`, `server.crt`
- `client.key`, `client.csr`, `client.crt`
- `fake-ca.key`, `fake-ca.crt`
- `fake-client.key`, `fake-client.csr`, `fake-client.crt`

Stop condition: all cert/key files exist and can be copied into the correct containers.

## Phase 3: Server Service And Stunnel
Target outcome: plaintext Python service runs on `localhost:8000`; `stunnel4` listens on `4433` and requires client certificate verification.

Required `stunnel.conf` facts:
- accepts on `0.0.0.0:4433`
- connects to `127.0.0.1:8000`
- uses the server certificate and key
- verifies client certificates against the Root CA
- requires client cert verification

Evidence required for report:
- exact `stunnel.conf`
- command that starts `python3 -m http.server 8000`
- command that starts `stunnel4`

Stop condition: server container has backend and stunnel running without config errors.

## Phase 4: Three Curl Tests
Target outcome: the three graded scenarios are captured with `curl -v`.

Success:
```sh
curl -v --cacert ca.crt --cert client.crt --key client.key https://hw2-mtls-server:4433/
```

Failure 1, no client certificate:
```sh
curl -v --cacert ca.crt https://hw2-mtls-server:4433/
```

Failure 2, unauthorized client certificate:
```sh
curl -v --cacert ca.crt --cert fake-client.crt --key fake-client.key https://hw2-mtls-server:4433/
```

Evidence required for report:
- screenshot or copied terminal output for each `curl -v`
- success must show HTTP `200 OK`
- failures must show TLS alert, certificate rejection, or handshake failure

Stop condition: all three outputs are saved in `lab/logs/`.

## Phase 5: Packet Capture
Target outcome: successful mTLS traffic is captured during Scenario 1.

Preferred host-side capture flow:
```sh
docker network inspect hw2-mtls-net
ip link
sudo tcpdump -i <docker-bridge-interface> -w lab/captures/success-mtls.pcap port 4433
```

Fallback container-side capture flow:
```sh
docker exec hw2-mtls-server bash -lc 'tcpdump -i any -w /tmp/success-mtls.pcap port 4433'
docker cp hw2-mtls-server:/tmp/success-mtls.pcap lab/captures/success-mtls.pcap
```

Evidence required for report:
- packet-capture screenshot from Wireshark or readable `tcpdump` output
- show the successful mTLS connection, not just the backend HTTP service

Stop condition: `success-mtls.pcap` exists and can be opened or summarized.

## Report Evidence Inventory
- `openssl` command list for CA, server cert, valid client cert, fake CA, and fake client cert
- exact `stunnel.conf`
- screenshot/log for valid client certificate success
- screenshot/log for no client certificate failure
- screenshot/log for fake client certificate failure
- packet-capture screenshot for successful handshake
- short architecture note: client container -> server container `stunnel4:4433` -> server plaintext `localhost:8000`

## Next Bounded Block
No bounded HW2 block remains. `report/513559004_report.pdf` was submitted and confirmed in LMS on `2026-04-17`.

Phase 1 is already complete as of 2026-04-16: the Docker network and two containers exist, the required tools are installed, and the client resolves the server.

Phase 2 is also complete as of 2026-04-16: the Root CA, server cert, valid client cert, fake CA, and fake client cert exist; the `openssl` command/output log is saved in `lab/logs/phase2-pki-commands-2026-04-16.log`; and the required cert/key materials have been copied into the server and client containers.

Phase 3 is also complete as of 2026-04-16: the plaintext backend and `stunnel4` are running, the exact `stunnel.conf` is saved in `lab/config/stunnel.conf`, and the successful valid-client `curl -v` log is saved in `lab/logs/phase3-success-curl-2026-04-16.log`.

Phase 4 is also complete as of 2026-04-16: the no-client-cert failure is saved in `lab/logs/phase4-failure-no-client-cert-2026-04-16.log`, the fake-client-cert failure is saved in `lab/logs/phase4-failure-fake-client-cert-2026-04-16.log`, and the server-side rejection evidence is saved in `lab/logs/phase4-stunnel-failures-2026-04-16.log`.

Phase 5 is also complete as of 2026-04-16: the successful packet capture is saved in `lab/captures/success-mtls-2026-04-16.pcap`, the paired success `curl -v` log is saved in `lab/logs/phase5-success-curl-2026-04-16.log`, and the readable packet summary is saved in `lab/logs/phase5-success-pcap-summary-2026-04-16.log`.

2026-04-17 regeneration note: the ignored 2026-04-16 local lab artifacts were not present in this workspace, so the two-container lab evidence was regenerated. The active local evidence set now uses `2026-04-17` filenames, including `lab/logs/phase2-pki-commands-2026-04-17.log`, `lab/logs/phase5-success-curl-2026-04-17.log`, `lab/captures/success-mtls-2026-04-17.pcap`, and `lab/logs/phase5-success-pcap-summary-2026-04-17.log`.

The report evidence map is also complete as of 2026-04-16: `report/evidence-map.md` links the required report sections to the saved command/config/log/pcap evidence while keeping generated certs, keys, logs, and packet captures out of Git.

The core explanation draft is also complete as of 2026-04-16: `report/core-explanation-draft.md` contains the report-ready topology, PKI, success/failure, and packet-capture explanations.

The near-final report draft is complete as of 2026-04-17: `report/near-final-report-draft.md` contains the selected evidence excerpts and final PDF checklist.

The professional PDF draft is complete as of 2026-04-17: `report/final-report.tex` contains the cybersecurity-style report narrative, and `report/final-report.pdf` was compiled and text-checked for the required rubric signals.

The official submission PDF is complete as of 2026-04-17: `report/513559004_report.pdf` includes `Jason Chia-Sheng Lin`, student ID `513559004`, and `Institute of Biophotonics, NYCU`, and has been text-checked for the required rubric signals.

Next stop condition: no action unless the LMS or instructor reports a concrete issue. Do not rerun the lab or reopen the report.
