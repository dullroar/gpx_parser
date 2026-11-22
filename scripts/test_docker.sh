#!/usr/bin/env bash
# Run me when: I need to build the GPX Parser image and run the CLI and context checks.
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
run_dir=$(mktemp -d "${TMPDIR:-/tmp}/gpx-parser-test.XXXXXXXXXX")
run_name=${run_dir##*/}
image="gpx-parser-test:${run_name#gpx-parser-test.}"

cleanup() {
    docker image rm "$image" >/dev/null 2>&1 || true
    rmdir -- "$run_dir"
}
trap cleanup EXIT

docker build --tag "$image" "$repo_root"
docker run --rm --name "$run_name" --network none --read-only \
    --tmpfs /tmp:rw,nosuid,nodev,mode=1777 "$image"
