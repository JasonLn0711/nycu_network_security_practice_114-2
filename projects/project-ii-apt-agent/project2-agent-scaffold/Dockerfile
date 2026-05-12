FROM python:3.12-slim

WORKDIR /opt/project2-agent-scaffold
COPY . /opt/project2-agent-scaffold

RUN chmod +x exploit triage scripts/*.sh \
    && ln -sf /opt/project2-agent-scaffold/exploit /exploit \
    && ln -sf /opt/project2-agent-scaffold/triage /triage

ENV PYTHONUNBUFFERED=1

CMD ["/bin/sh", "-lc", "echo 'Project II scaffold container ready. This image does not implement a real exploit.' && sleep infinity"]

