#!/usr/bin/env bash
set -euo pipefail

: "${MACHINE:?MACHINE environment variable must be set}"

echo "=== build syclenv (fail if no prerequisites installed) ==="
./syclenv create "$MACHINE" .yolo || true

echo "=== build syclenv (and install prerequisites) ==="
./syclenv create "$MACHINE" .yolo \
    --noconfirm \
    --install-prerequisites

echo "=== cat activate script ==="
cat .yolo/activate.bash

echo "=== activate syclenv ==="
(
    eval "$(./syclenv activate .yolo)"
)

echo "=== create SYCL source file ==="
cat >main.cpp <<'EOF'
#include <sycl/sycl.hpp>

int main() {
    return 0;
}
EOF

echo "=== compile hello world ==="
(
    eval "$(./syclenv activate .yolo)"
    syclcc $SYCL_FLAGS main.cpp
    ./a.out
)

echo "=== verify activate/deactivate restores shell environment ==="
(
    before="$(mktemp)"
    after="$(mktemp)"

    cleanup() {
        rm -f "$before" "$after"
    }
    trap cleanup EXIT

    ./scripts/snapshot-shell-env.sh "$before"

    eval "$(./syclenv activate .yolo)"
    deactivate

    ./scripts/snapshot-shell-env.sh "$after"

    ./scripts/compare-shell-env-snapshots.sh "$before" "$after"
)

echo "=== rebuild syclenv with hello world plugin ==="

remove_hello_world_artifacts() {
    rm -f \
        helloworld__afterenv \
        helloworld__beforeenv \
        helloworld__init \
        helloworld__prereq_check
}

check_hello_world_artifacts() {
    local file

    for file in \
        helloworld__afterenv \
        helloworld__beforeenv \
        helloworld__init \
        helloworld__prereq_check; do
        [[ -f "$file" ]] || {
            echo "Missing expected file: $file" >&2
            return 1
        }
    done
}

export SYCLENV_PLUGINS=syclenv.builtins.plugins.hello_world
./syclenv create "$MACHINE" .yolo

check_hello_world_artifacts

remove_hello_world_artifacts

echo "=== success ==="
