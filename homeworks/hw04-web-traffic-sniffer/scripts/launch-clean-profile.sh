#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
profile_dir="$repo_dir/evidence/raw-local/edge-profile"
start_url="${1:-https://dictionary.cambridge.org/}"
remote_debugging_port="${HW4_REMOTE_DEBUGGING_PORT:-9222}"

mkdir -p "$profile_dir"

browser=""
needs_no_sandbox=0
for candidate in microsoft-edge microsoft-edge-stable chromium chromium-browser google-chrome google-chrome-stable; do
  if command -v "$candidate" >/dev/null 2>&1; then
    browser="$candidate"
    break
  fi
done

if [ -z "$browser" ]; then
  playwright_chrome="$(find "$HOME/.cache/ms-playwright" -path '*/chrome-linux64/chrome' -type f 2>/dev/null | sort | tail -n 1 || true)"
  if [ -n "$playwright_chrome" ]; then
    browser="$playwright_chrome"
    needs_no_sandbox=1
  fi
fi

if [ -z "$browser" ]; then
  echo "No Edge/Chromium/Chrome executable found on PATH or in ~/.cache/ms-playwright." >&2
  echo "Install or launch Microsoft Edge manually with a clean profile at:" >&2
  echo "$profile_dir" >&2
  exit 1
fi

echo "Launching $browser with clean HW4 profile:"
echo "$profile_dir"

extra_args=()
if [ "$needs_no_sandbox" -eq 1 ]; then
  extra_args+=(--no-sandbox)
fi

"$browser" \
  --user-data-dir="$profile_dir" \
  --no-first-run \
  --disable-sync \
  --load-extension="$repo_dir/solution/Extension" \
  --remote-debugging-port="$remote_debugging_port" \
  "${extra_args[@]}" \
  "$start_url" >/tmp/hw4-clean-profile-browser.log 2>&1 &

echo "Browser started. Load the extension from:"
echo "$repo_dir/solution/Extension"
echo "Remote debugging URL:"
echo "http://127.0.0.1:$remote_debugging_port/json/version"
