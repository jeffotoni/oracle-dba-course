#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-free-lite-23ai}"
VOLUME_NAME="${VOLUME_NAME:-oracle-free-lite-23ai-data}"
REMOVE_VOLUME="${REMOVE_VOLUME:-false}"

podman rm -f "${CONTAINER_NAME}"

if [[ "${REMOVE_VOLUME}" == "true" ]]; then
  podman volume rm "${VOLUME_NAME}"
fi
