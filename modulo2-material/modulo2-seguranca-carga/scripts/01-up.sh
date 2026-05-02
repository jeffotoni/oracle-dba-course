#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
podman compose up -d
podman ps --filter name=oracle-free
