#!/usr/bin/env bash
set -euo pipefail

podman exec -i oracle-free bash -lc "impdp system/Senha123@//localhost:1521/FREEPDB1 DIRECTORY=dpump_dir DUMPFILE=app_owner_m2.dmp LOGFILE=imp_app_clone_m2.log REMAP_SCHEMA=APP_OWNER:APP_CLONE"

echo "Import finalizado. Arquivos em /opt/oracle/labdata"
