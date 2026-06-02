#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-free-full-23ai}"
IMAGE="${IMAGE:-container-registry.oracle.com/database/free:latest}"
ORACLE_PWD="${ORACLE_PWD:-OraclePwd123}"
ORACLE_PDB="${ORACLE_PDB:-FREEPDB1}"
HOST_PORT="${HOST_PORT:-1522}"
VOLUME_NAME="${VOLUME_NAME:-oracle-free-full-23ai-data}"

podman run -d \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:1521" \
  --cap-add SYS_NICE \
  -e "ORACLE_PWD=${ORACLE_PWD}" \
  -e "ORACLE_PDB=${ORACLE_PDB}" \
  -v "${VOLUME_NAME}:/opt/oracle/oradata:Z" \
  "${IMAGE}"

echo "Container: ${CONTAINER_NAME}"
echo "Image: ${IMAGE}"
echo "Port: ${HOST_PORT}->1521"
echo "Password: ${ORACLE_PWD}"
echo "Service/PDB: ${ORACLE_PDB}"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
