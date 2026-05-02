#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] container"
podman ps --format '{{.Names}}\t{{.Status}}' | grep oracle-free

echo "[2/4] tools inside container"
podman exec -i oracle-free bash -lc 'which sqlplus && which sqlldr && which expdp && which impdp'

echo "[3/4] labdata mounted"
podman exec -i oracle-free bash -lc 'ls -la /opt/oracle/labdata'

echo "[4/4] sql connectivity"
podman exec -i oracle-free sqlplus -s system/Senha123@//localhost:1521/FREEPDB1 <<'SQL'
SET PAGES 100
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container FROM dual;
SELECT instance_name, status FROM v\$instance;
SELECT con_id, name, open_mode FROM v\$pdbs ORDER BY con_id;
EXIT
SQL
