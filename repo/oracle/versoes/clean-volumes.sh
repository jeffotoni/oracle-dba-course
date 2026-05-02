#!/usr/bin/env bash
set -euo pipefail

volumes=(
  oracle-free-lite-23ai-data
  oracle-free-full-23ai-data
  oracle-xe-21-slim-data
  oracle-xe-21-full-data
  oracle-free-23-slim-data
  oracle-free-23-full-data
  oracle-xe-official-data
  oracle-xe-11g-data
  oracle-12c-data
)

for volume in "${volumes[@]}"; do
  podman volume rm "${volume}" 2>/dev/null || true
done
