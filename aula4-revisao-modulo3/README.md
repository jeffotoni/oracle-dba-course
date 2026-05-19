# Revisao do Modulo 3 - aula 4

> Revisao pratica do modulo 3: backup, recuperacao, `ARCHIVELOG`, `FRA`, `Data Pump` e `RMAN` em Oracle.

## Ideia central

O modulo 3 responde a uma pergunta operacional:

```txt
Se algo der errado, como eu restauro o ambiente com seguranca?
```

Para isso, vamos separar quatro conceitos:

- `Data Pump` - dump logico de schemas, tabelas, dados e metadados.
- `ARCHIVELOG` - preserva redo logs arquivados para recuperacao.
- `FRA` - area gerenciada pelo Oracle para arquivos de recuperacao.
- `RMAN` - ferramenta principal para backup fisico, restore e recovery.

## 1. Backup logico x backup fisico

### Backup logico

Trabalha com objetos Oracle:

- schemas;
- tabelas;
- indices;
- constraints;
- grants;
- dados.

Ferramentas:

- `expdp`
- `impdp`

### Backup fisico

Trabalha com a estrutura fisica do banco:

- datafiles;
- control files;
- archived logs;
- `SPFILE`;
- backups gerados pelo `RMAN`.

Ferramenta:

- `RMAN`

### Regra pratica

```txt
Data Pump = copiar objetos e dados
RMAN = proteger e recuperar o banco fisico
```

## 2. Ambiente padrao da aula

Usaremos a mesma versao padronizada no curso:

- container: `oracle-free-full-23ai`
- imagem: `container-registry.oracle.com/database/free:latest`
- porta host: `1522`
- porta interna: `1521`
- service name: `FREEPDB1`
- senha: `OraclePwd123`

Subir pelo script:

```bash
cd repo/oracle/versoes/free-full-23ai/script
./up.sh
```

Comando explicito equivalente:

```bash
podman run -d \
  --name oracle-free-full-23ai \
  -p 1522:1521 \
  --cap-add SYS_NICE \
  -e ORACLE_PWD=OraclePwd123 \
  -e ORACLE_PDB=FREEPDB1 \
  -v oracle-free-full-23ai-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/free:latest
```

Validar:

```bash
podman ps
podman logs -f oracle-free-full-23ai
```

## 3. Binarios usados na pratica

Algumas atividades rodam melhor dentro do container Oracle.

Entrar no container:

```bash
podman exec -it oracle-free-full-23ai bash
```

Validar binarios:

```bash
command -v sqlplus
command -v expdp
command -v impdp
command -v rman
```

Testar rapidamente:

```bash
sqlplus -v
expdp help=y | head
impdp help=y | head
rman -h | head
```

### O que e cada binario

- `sqlplus` - cliente nativo para SQL e comandos administrativos.
- `expdp` - exporta dump logico Oracle.
- `impdp` - importa dump logico Oracle.
- `rman` - faz backup fisico, restore, recovery, validacao e catalogo.

## 4. Checklist SQL inicial

Executar no cliente SQL ou via `SQL*Plus`.

Conexao recomendada para consultas:

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: system
Password: OraclePwd123
```

Queries:

```sql
SELECT instance_name,
       status
FROM v$instance;

SELECT name,
       open_mode,
       log_mode
FROM v$database;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 5. Preparar diretorios no container

Criar diretorios fisicos para o laboratorio:

```bash
podman exec -it oracle-free-full-23ai mkdir -p /opt/oracle/labbackup/fra
podman exec -it oracle-free-full-23ai mkdir -p /opt/oracle/labbackup/rman
podman exec -it oracle-free-full-23ai mkdir -p /opt/oracle/labbackup/dpump
```

Validar:

```bash
podman exec -it oracle-free-full-23ai ls -lah /opt/oracle/labbackup
```

## 6. Configurar FRA

A `FRA` e configurada no `CDB$ROOT`, como `SYSDBA`.

Conectar pelo terminal do host:

```bash
podman exec -it oracle-free-full-23ai bash -lc "sqlplus / as sysdba"
```

Configurar:

```sql
ALTER SYSTEM SET db_recovery_file_dest_size = 10G SCOPE=BOTH;
ALTER SYSTEM SET db_recovery_file_dest = '/opt/oracle/labbackup/fra' SCOPE=BOTH;
```

Validar:

```sql
SELECT name,
       value
FROM v$parameter
WHERE name IN ('db_recovery_file_dest', 'db_recovery_file_dest_size')
ORDER BY name;
```

## 7. Habilitar ARCHIVELOG

Este bloco reinicia o banco. Use em laboratorio.

Ainda como `SYSDBA`, primeiro verificar:

```sql
SELECT log_mode
FROM v$database;
```

Se o resultado ja for `ARCHIVELOG`, pular os comandos de reinicio.

Se o resultado for `NOARCHIVELOG`, executar:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;

ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;

SELECT log_mode
FROM v$database;
```

Validar PDB:

```sql
SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

Sair:

```sql
EXIT;
```

## 8. Criar schema de laboratorio

Conectar na PDB como `SYSTEM` pelo terminal do host:

```bash
podman exec -it oracle-free-full-23ai sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

Criar usuarios:

```sql
CREATE USER app_rman IDENTIFIED BY AppRman123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

CREATE USER app_rman_clone IDENTIFIED BY AppRmanClone123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO app_rman;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO app_rman_clone;
```

Criar diretório logico para Data Pump:

```sql
CREATE OR REPLACE DIRECTORY dpump_mod3_dir AS '/opt/oracle/labbackup/dpump';

GRANT READ, WRITE ON DIRECTORY dpump_mod3_dir TO system;
GRANT READ, WRITE ON DIRECTORY dpump_mod3_dir TO app_rman;
GRANT READ, WRITE ON DIRECTORY dpump_mod3_dir TO app_rman_clone;
```

Sair:

```sql
EXIT;
```

## 9. Criar tabela e dados

Conectar como `APP_RMAN`:

```bash
podman exec -it oracle-free-full-23ai sqlplus app_rman/AppRman123@//localhost:1521/FREEPDB1
```

Criar tabela:

```sql
CREATE TABLE pedidos_lab (
  id_pedido   NUMBER PRIMARY KEY,
  cliente     VARCHAR2(100),
  valor_total NUMBER(10,2),
  criado_em   DATE DEFAULT SYSDATE
);

INSERT INTO pedidos_lab (id_pedido, cliente, valor_total)
VALUES (1, 'Cliente A', 150.00);

INSERT INTO pedidos_lab (id_pedido, cliente, valor_total)
VALUES (2, 'Cliente B', 280.00);

INSERT INTO pedidos_lab (id_pedido, cliente, valor_total)
VALUES (3, 'Cliente C', 490.00);

COMMIT;
```

Validar:

```sql
SELECT *
FROM pedidos_lab
ORDER BY id_pedido;
```

Sair:

```sql
EXIT;
```

## 10. Data Pump na pratica

### Exportar schema com `expdp`

No terminal do host:

```bash
podman exec -it oracle-free-full-23ai expdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_mod3_dir \
  DUMPFILE=app_rman_m3.dmp \
  LOGFILE=app_rman_m3_exp.log \
  SCHEMAS=APP_RMAN
```

Validar arquivos:

```bash
podman exec -it oracle-free-full-23ai ls -lah /opt/oracle/labbackup/dpump
podman exec -it oracle-free-full-23ai cat /opt/oracle/labbackup/dpump/app_rman_m3_exp.log
```

### Importar com `impdp`

No terminal do host:

```bash
podman exec -it oracle-free-full-23ai impdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_mod3_dir \
  DUMPFILE=app_rman_m3.dmp \
  LOGFILE=app_rman_m3_imp.log \
  REMAP_SCHEMA=APP_RMAN:APP_RMAN_CLONE
```

Validar import:

```bash
podman exec -it oracle-free-full-23ai sqlplus app_rman_clone/AppRmanClone123@//localhost:1521/FREEPDB1
```

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;

SELECT *
FROM pedidos_lab
ORDER BY id_pedido;

EXIT;
```

## 11. RMAN na pratica

Entrar no RMAN pelo terminal do host:

```bash
podman exec -it oracle-free-full-23ai bash -lc "rman target /"
```

Configurar:

```rman
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
SHOW ALL;
```

Backup fisico do banco:

```rman
BACKUP AS BACKUPSET DATABASE
  FORMAT '/opt/oracle/labbackup/rman/db_%U.bkp';
```

Backup dos archived logs:

```rman
BACKUP AS BACKUPSET ARCHIVELOG ALL
  FORMAT '/opt/oracle/labbackup/rman/arch_%U.bkp';
```

Validar:

```rman
LIST BACKUP SUMMARY;
VALIDATE DATABASE;
RESTORE DATABASE VALIDATE;
CROSSCHECK BACKUP;
CROSSCHECK ARCHIVELOG ALL;
```

Sair:

```rman
EXIT;
```

Validar arquivos no host:

```bash
podman exec -it oracle-free-full-23ai ls -lah /opt/oracle/labbackup/rman
```

## 12. Consultas de observacao

### FRA

```sql
SELECT name,
       space_limit / 1024 / 1024 AS fra_limit_mb,
       space_used / 1024 / 1024 AS fra_used_mb,
       space_reclaimable / 1024 / 1024 AS fra_reclaimable_mb
FROM v$recovery_file_dest;
```

### Archived logs

```sql
SELECT sequence#,
       archived,
       status,
       first_time
FROM v$archived_log
ORDER BY sequence# DESC
FETCH FIRST 20 ROWS ONLY;
```

### Jobs RMAN

```sql
SELECT session_key,
       input_type,
       status,
       start_time,
       end_time
FROM v$rman_backup_job_details
ORDER BY start_time DESC
FETCH FIRST 10 ROWS ONLY;
```

## 13. Restore e recovery

Para esta revisao, o foco pratico fica em:

- criar backup;
- listar backup;
- validar backup;
- validar restore com `RESTORE DATABASE VALIDATE`.

Restore real de datafile, tablespace ou banco inteiro deve ser feito em uma simulacao controlada, porque envolve indisponibilidade, arquivos fisicos e risco de quebrar o laboratorio durante a aula.

Exemplos para explicar, sem executar como passo principal:

```rman
RESTORE TABLESPACE users;
RECOVER TABLESPACE users;
```

```rman
RESTORE DATABASE;
RECOVER DATABASE;
```

## 14. Limpeza opcional

Conectar como `SYSTEM` em `FREEPDB1`:

```sql
DROP USER app_rman_clone CASCADE;
DROP USER app_rman CASCADE;
DROP DIRECTORY dpump_mod3_dir;
```

Arquivos do laboratorio:

```bash
podman exec -it oracle-free-full-23ai rm -rf /opt/oracle/labbackup/dpump/*
podman exec -it oracle-free-full-23ai rm -rf /opt/oracle/labbackup/rman/*
```

## 15. Resultado esperado

Ao final da revisao, precisa ficar claro:

- `expdp` e `impdp` resolvem dump logico;
- `ARCHIVELOG` amplia a capacidade de recuperacao;
- `FRA` organiza arquivos de recovery;
- `RMAN` protege a estrutura fisica do banco;
- backup precisa ser validado;
- restore real deve ser testado em ambiente controlado.

## Referencias internas

- `modulo3-material/03-teoria-modulo3.md`
- `modulo3-material/03-pratica-modulo3.md`
