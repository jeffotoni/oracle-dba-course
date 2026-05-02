#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-free-23-slim}"
IMAGE="${IMAGE:-gvenzl/oracle-free:23-slim}"
ORACLE_PASSWORD="${ORACLE_PASSWORD:-OraclePwd123}"
HOST_PORT="${HOST_PORT:-1525}"
VOLUME_NAME="${VOLUME_NAME:-oracle-free-23-slim-data}"
podman run -d \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:1521" \
  -e "ORACLE_PASSWORD=${ORACLE_PASSWORD}" \
  -v "${VOLUME_NAME}:/opt/oracle/oradata:Z" \
  "${IMAGE}"

echo "Container: ${CONTAINER_NAME}"
echo "Image: ${IMAGE}"
echo "Port: ${HOST_PORT}->1521"
echo "Password: ${ORACLE_PASSWORD}"
echo "Database: FREE"
echo "Service/PDB: FREEPDB1"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
