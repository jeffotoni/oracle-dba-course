#!/usr/bin/env bash
set -euo pipefail

podman pull gvenzl/oracle-xe:21-slim

podman run -d \
  --name oracle-xe \
  -p 1521:1521 \
  -p 5500:5500 \
  -e ORACLE_PASSWORD=Oracle123 \
  gvenzl/oracle-xe:21-slim
