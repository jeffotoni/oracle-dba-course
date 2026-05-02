#!/usr/bin/env bash
set -euo pipefail

podman exec -i oracle-free bash -lc "expdp system/Senha123@//localhost:1521/FREEPDB1 DIRECTORY=dpump_dir DUMPFILE=app_owner_m2.dmp LOGFILE=exp_app_owner_m2.log SCHEMAS=APP_OWNER"

echo "Export finalizado. Arquivos em /opt/oracle/labdata"
