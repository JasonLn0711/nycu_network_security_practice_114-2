# Project II Lab Bundle Manifest

Source archive: `lab.zip`

This file keeps the provided lab bundle searchable without requiring every agent or reader to unpack the archive first.

## Archive Contents

| Path in archive | Role |
| --- | --- |
| `lab/docker.sh` | Creates Docker containers for the selected project phase |
| `lab/grader.sh` | Grading runner intended to be used inside the external container |
| `lab/IC/Dockerfile` | Dockerfile for the provided internal-container image |
| `lab/IC/backdoor` | Provided internal-environment backdoor binary |
| `lab/IC/runserver.sh` | Internal-container server runner |
| `lab/IC/server_1` | Provided phase server binary |
| `lab/IC/server_2` | Provided phase server binary |
| `lab/shared/blogic` | Business-logic binary copied into the shared volume |
| `lab/shared/config.data` | Initial shared config data |
| `lab/shared/coredump/` | Runtime coredump output directory |

## Setup Notes From The Brief

Run the lab only inside the course-provided local environment.

```sh
cd lab
docker build -t ic_image ./IC
./docker.sh [1|2|3]
```

The brief says the grading measurement may change, but `/exploit` and `/triage` must be in the correct locations, and `/exploit` must modify `config.data` and produce `exploit_done`.

## Git Policy

- Keep the original `lab.zip` tracked as the official supplied lab bundle.
- Do not commit generated coredumps, container runtime output, or local scratch builds.
- If the archive is extracted for work, document the exact extraction location and whether that extracted copy is tracked or local-only before committing it.
