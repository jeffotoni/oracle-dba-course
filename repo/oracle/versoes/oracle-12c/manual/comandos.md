# Oracle 12c Enterprise - Comando Manual

Use este comando quando quiser subir o banco diretamente com `podman run`, sem script, sem compose e sem build local.

```bash
podman run -d \
  --name oracle-12c \
  -p 1529:1521 \
  -p 5508:5500 \
  -e ORACLE_PWD=Oracle123 \
  -v oracle-12c-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/enterprise:12.2.0.1
```
