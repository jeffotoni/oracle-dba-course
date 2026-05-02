#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-xe-official}"
VOLUME_NAME="${VOLUME_NAME:-oracle-xe-official-data}"
REMOVE_VOLUME="${REMOVE_VOLUME:-false}"

podman rm -f "${CONTAINER_NAME}"

if [[ "${REMOVE_VOLUME}" == "true" ]]; then
  podman volume rm "${VOLUME_NAME}"
fi
