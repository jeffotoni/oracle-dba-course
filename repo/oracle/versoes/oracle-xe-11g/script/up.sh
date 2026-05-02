#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-xe-11g}"
IMAGE="${IMAGE:-wnameless/oracle-xe-11g-r2}"
HOST_PORT="${HOST_PORT:-1528}"
podman run -d \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:1521" \
  "${IMAGE}"

echo "Container: ${CONTAINER_NAME}"
echo "Image: ${IMAGE}"
echo "Port: ${HOST_PORT}->1521"
echo "Password: oracle"
echo "Database: XE"
echo "Service/PDB: XE"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
