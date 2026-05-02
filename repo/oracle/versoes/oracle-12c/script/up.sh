#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-oracle-12c}"
IMAGE="${IMAGE:-container-registry.oracle.com/database/enterprise:12.2.0.1}"
ORACLE_PWD="${ORACLE_PWD:-Oracle123}"
HOST_PORT="${HOST_PORT:-1529}"
HOST_PORT_WEB="${HOST_PORT_WEB:-5508}"
VOLUME_NAME="${VOLUME_NAME:-oracle-12c-data}"

podman run -d \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:1521" \
  -p "${HOST_PORT_WEB}:5500" \
  -e "ORACLE_PWD=${ORACLE_PWD}" \
  -v "${VOLUME_NAME}:/opt/oracle/oradata:Z" \
  "${IMAGE}"

echo "Container: ${CONTAINER_NAME}"
echo "Image: ${IMAGE}"
echo "Port SQL: ${HOST_PORT}->1521"
echo "Port Web: ${HOST_PORT_WEB}->5500"
echo "Password: ${ORACLE_PWD}"
echo "Check health: podman ps --filter name=${CONTAINER_NAME}"
echo "Logs: podman logs -f ${CONTAINER_NAME}"
