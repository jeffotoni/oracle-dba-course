#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-xe-11g}"

podman rm -f "${CONTAINER_NAME}"
