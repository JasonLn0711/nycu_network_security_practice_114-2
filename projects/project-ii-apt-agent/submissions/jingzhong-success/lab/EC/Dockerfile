FROM ubuntu:24.04

RUN apt update && apt install -y \
    --no-install-recommends \
    python3 \
    file \
    binutils \
    && rm -rf /var/lib/apt/lists/*

COPY exploit /exploit
COPY triage /triage
COPY analyze_target.py /analyze_target.py

RUN chmod +x /exploit /triage /analyze_target.py