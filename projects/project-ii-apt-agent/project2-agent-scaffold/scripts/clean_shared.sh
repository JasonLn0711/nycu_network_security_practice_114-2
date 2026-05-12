#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
: "${PROJECT2_SHARED_DIR:=$PROJECT_ROOT/mock_shared}"

case "$PROJECT2_SHARED_DIR" in
  "$PROJECT_ROOT"/mock_shared|"$PROJECT_ROOT"/mock_shared/*|./mock_shared|mock_shared)
    rm -rf "$PROJECT2_SHARED_DIR"
    mkdir -p "$PROJECT2_SHARED_DIR"
    echo "cleaned mock shared directory: $PROJECT2_SHARED_DIR"
    ;;
  /shared)
    if [ "${PROJECT2_ALLOW_SHARED_DELETE:-}" = "YES" ]; then
      rm -rf /shared/*
      echo "cleaned /shared because PROJECT2_ALLOW_SHARED_DELETE=YES"
    else
      echo "refusing to clean /shared without PROJECT2_ALLOW_SHARED_DELETE=YES" >&2
      exit 1
    fi
    ;;
  *)
    echo "refusing to clean non-default shared dir: $PROJECT2_SHARED_DIR" >&2
    exit 1
    ;;
esac

