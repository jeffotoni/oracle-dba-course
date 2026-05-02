#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-xe-official}"
IMAGE="${IMAGE:-container-registry.oracle.com/database/express:21.3.0-xe}"
ORACLE_PWD="${ORACLE_PWD:-OraclePwd123}"
HOST_PORT="${HOST_PORT:-1527}"
VOLUME_NAME="${VOLUME_NAME:-oracle-xe-official-data}"
podman run -d \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:1521" \
  -e "ORACLE_PWD=${ORACLE_PWD}" \
  -v "${VOLUME_NAME}:/opt/oracle/oradata:Z" \
  "${IMAGE}"

echo "Container: ${CONTAINER_NAME}"
echo "Image: ${IMAGE}"
echo "Port: ${HOST_PORT}->1521"
echo "Password: ${ORACLE_PWD}"
echo "Database: XE"
echo "Service/PDB: XEPDB1"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
