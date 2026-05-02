#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-xe-21-full}"
IMAGE="${IMAGE:-gvenzl/oracle-xe:21-full}"
ORACLE_PASSWORD="${ORACLE_PASSWORD:-OraclePwd123}"
HOST_PORT="${HOST_PORT:-1524}"
VOLUME_NAME="${VOLUME_NAME:-oracle-xe-21-full-data}"
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
echo "Database: XE"
echo "Service/PDB: XEPDB1"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
