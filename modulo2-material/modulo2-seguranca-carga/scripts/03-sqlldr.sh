#!/usr/bin/env bash
set -euo pipefail

podman exec -i oracle-free bash -lc "sqlldr app_owner/AppOwner123@//localhost:1521/FREEPDB1 control=/opt/oracle/labdata/produtos.ctl log=/opt/oracle/labdata/produtos_sqlldr.log"

echo "SQL*Loader finalizado. Log: /opt/oracle/labdata/produtos_sqlldr.log"
