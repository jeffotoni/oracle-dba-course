# Módulo 3 - Prática  
## Rotinas de Backup e Recuperação

## Visão geral

Neste módulo usaremos um laboratório prático para consolidar os fundamentos de backup e recuperação em Oracle.

A prática será organizada em blocos progressivos:

1. preparação do ambiente;
2. validação do modo de arquivamento e configuração da área de recuperação;
3. uso do RMAN para backup completo, incremental e de archivelogs;
4. validação, catálogo e retenção;
5. simulações controladas de recuperação de instância e de mídia;
6. observação de recuperação de bloco em nível conceitual e operacional.

A proposta é manter um laboratório reproduzível em Podman, alinhado ao ambiente já adotado nos módulos anteriores.

---

## Ambiente utilizado

Usaremos:

- Podman;
- Oracle Database Free em container;
- RMAN dentro do container;
- CloudBeaver para consultas de apoio;
- volumes montados para persistência do banco e dos backups.

---

## Software necessário

Em ambiente Windows, deveremos ter instalado:

- Podman;
- CloudBeaver;
- Git;
- editor de texto ou VS Code.

Opcionalmente poderemos utilizar:

- SQL Developer;
- Windows Terminal;
- 7-Zip.

---

## Premissas do laboratório

Neste roteiro, consideraremos o seguinte padrão:

- **nome do container**: `oracle-free`
- **porta do listener**: `1521`
- **senha administrativa**: `Senha123`
- **service name**: `FREEPDB1`
- **SID da instância**: `FREE`
- **diretório de laboratório de backup dentro do container**: `/opt/oracle/labbackup`
- **diretório da fast recovery area**: `/opt/oracle/labbackup/fra`
- **diretório para backups RMAN**: `/opt/oracle/labbackup/rman`

---

## 1. Estrutura recomendada do módulo

```text
modulo3-backup-recuperacao/
├── compose.yaml
├── labbackup/
│   ├── fra/
│   └── rman/
└── scripts/
```

---

## 2. Subida do ambiente com Podman

## 2.1. compose.yaml

```yaml
services:
  oracle-free:
    image: gvenzl/oracle-free:latest
    container_name: oracle-free
    ports:
      - "1521:1521"
    environment:
      ORACLE_PASSWORD: Senha123
    volumes:
      - oracle_data:/opt/oracle/oradata
      - ./labbackup:/opt/oracle/labbackup

volumes:
  oracle_data:
```

## 2.2. Comandos para subir o ambiente

```bash
podman compose up -d
podman ps
podman logs -f oracle-free
```

## 2.3. Entrar no container

```bash
podman exec -it oracle-free bash
```

## 2.4. Validar conexão no CloudBeaver

Conectar no CloudBeaver como `system` em `FREEPDB1`.

Consultas iniciais:

```sql
SELECT instance_name, status FROM v$instance;
SELECT name, open_mode FROM v$pdbs;
SELECT log_mode FROM v$database;
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest';
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest_size';
```

## 2.5. Checklist SQL mínimo do módulo

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
```

---

## 3. Preparação do ambiente para backup e recuperação

## 3.1. Criar diretórios de backup no sistema operacional do container

Dentro do container:

```bash
mkdir -p /opt/oracle/labbackup/fra
mkdir -p /opt/oracle/labbackup/rman
ls -lah /opt/oracle/labbackup
```

## 3.2. Configurar a Fast Recovery Area (FRA)

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

Configurar FRA:

```sql
ALTER SYSTEM SET db_recovery_file_dest_size = 10G SCOPE=BOTH;
ALTER SYSTEM SET db_recovery_file_dest = '/opt/oracle/labbackup/fra' SCOPE=BOTH;
```

Validar:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest';
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest_size';
```

## 3.3. Habilitar ARCHIVELOG

### Passo 1 - verificar o modo atual

```sql
SELECT log_mode
FROM v$database;
```

### Passo 2 - reiniciar em MOUNT

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
```

### Passo 3 - habilitar o modo ARCHIVELOG

```sql
ALTER DATABASE ARCHIVELOG;
```

### Passo 4 - abrir o banco

```sql
ALTER DATABASE OPEN;
```

### Passo 5 - validar

```sql
SELECT log_mode
FROM v$database;
```

### Passo 6 - validar na PDB

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT name, open_mode FROM v$pdbs;
```

---

## 4. Preparação de objetos para o laboratório

Criaremos um tablespace e um schema simples para gerar atividade de dados, backup e recuperação.

## 4.1. Criar usuário de laboratório

Conectar como SYSDBA ou SYSTEM:

```sql
CREATE USER app_rman IDENTIFIED BY AppRman123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO app_rman;
```

## 4.2. Criar tabela de laboratório

Conectar como `app_rman`:

Conectar no CloudBeaver como `app_rman`.

```sql
CREATE TABLE pedidos_lab (
  id_pedido      NUMBER PRIMARY KEY,
  cliente        VARCHAR2(100),
  valor_total    NUMBER(10,2),
  data_pedido    DATE DEFAULT SYSDATE
);

INSERT INTO pedidos_lab (id_pedido, cliente, valor_total) VALUES (1, 'Cliente A', 150.00);
INSERT INTO pedidos_lab (id_pedido, cliente, valor_total) VALUES (2, 'Cliente B', 280.00);
INSERT INTO pedidos_lab (id_pedido, cliente, valor_total) VALUES (3, 'Cliente C', 490.00);
COMMIT;
```

## 4.3. Gerar mais atividade

```sql
BEGIN
  FOR i IN 4..200 LOOP
    INSERT INTO pedidos_lab (id_pedido, cliente, valor_total)
    VALUES (i, 'Cliente ' || i, i * 10);
  END LOOP;
  COMMIT;
END;
/
```

## 4.4. Validar a tabela

```sql
SELECT COUNT(*) FROM pedidos_lab;
SELECT MIN(id_pedido), MAX(id_pedido) FROM pedidos_lab;
```

---

## 5. Bloco prático - dump lógico com Oracle Data Pump

Antes de entrar no `RMAN`, vale fixar a camada de dump lógico do Oracle.

Comparação mental rápida:

- PostgreSQL: `pg_dump`
- MySQL / MariaDB: `mysqldump`
- MongoDB: `mongodump`
- Oracle: `expdp`

Neste módulo, `expdp` e `impdp` entram como:

- exportação lógica;
- restore seletivo;
- movimentação de schema e tabela;
- apoio a laboratório, dev e clonagem controlada.

Já o `RMAN` continua sendo a ferramenta principal para backup físico, restore e recovery estrutural.

## 5.1. Validar o diretório padrão do Data Pump

Conectar no CloudBeaver como `system` ou `sys` e validar:

```sql
SELECT directory_name,
       directory_path
FROM dba_directories
WHERE directory_name = 'DATA_PUMP_DIR';
```

## 5.2. Validar as tabelas do schema de laboratório

Conectar no CloudBeaver como `app_rman`:

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

## 5.3. Exportar o schema de laboratório

Neste curso, os utilitários nativos Oracle podem ser executados dentro do container com `podman exec`.

Exemplo de exportação lógica do schema `APP_RMAN`:

```bash
podman exec -i oracle-free bash -lc "expdp app_rman/AppRman123@//localhost:1521/FREEPDB1 \
schemas=APP_RMAN \
directory=DATA_PUMP_DIR \
dumpfile=app_rman_m3.dmp \
logfile=app_rman_m3_exp.log"
```

Resultado esperado:

- `app_rman_m3.dmp` com o dump lógico;
- `app_rman_m3_exp.log` com o log da operação.

## 5.4. Exportar apenas uma tabela

```bash
podman exec -i oracle-free bash -lc "expdp app_rman/AppRman123@//localhost:1521/FREEPDB1 \
tables=APP_RMAN.PEDIDOS_LAB \
directory=DATA_PUMP_DIR \
dumpfile=pedidos_lab_m3.dmp \
logfile=pedidos_lab_m3_exp.log"
```

## 5.5. Importar para um schema de clone

Primeiro, criar um schema de destino:

```sql
CREATE USER app_rman_clone IDENTIFIED BY AppRmanClone123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO app_rman_clone;
```

Depois, importar com remapeamento:

```bash
podman exec -i oracle-free bash -lc "impdp system/Senha123@//localhost:1521/FREEPDB1 \
schemas=APP_RMAN \
directory=DATA_PUMP_DIR \
dumpfile=app_rman_m3.dmp \
logfile=app_rman_m3_imp.log \
remap_schema=APP_RMAN:APP_RMAN_CLONE"
```

## 5.6. Validar o restore lógico

Conectar no CloudBeaver como `app_rman_clone` e validar:

```sql
SELECT COUNT(*) AS total_rows
FROM pedidos_lab;

SELECT MIN(id_pedido) AS min_id,
       MAX(id_pedido) AS max_id
FROM pedidos_lab;
```

## 5.7. Regra prática do módulo

Use esta leitura:

- `expdp` e `impdp` para dump e restore lógico;
- `RMAN` para backup físico, restore e recovery estrutural;
- em laboratório e desenvolvimento, o primeiro passo mental de dump é `expdp`;
- em produção, a proteção séria do banco exige `RMAN`, `ARCHIVELOG` e estratégia de retenção.

---

## 6. Iniciando o RMAN

Encerrar a sessão administrativa atual, se necessário, antes de entrar no `RMAN`.

Entrar no RMAN:

```bash
rman target /
```

Validação inicial:

```rman
REPORT SCHEMA;
SHOW ALL;
```

---

## 7. Configuração básica do RMAN

## 7.1. Ativar autobackup do control file

```rman
CONFIGURE CONTROLFILE AUTOBACKUP ON;
```

## 7.2. Definir política de retenção

```rman
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
```

## 7.3. Definir tipo de backup padrão

```rman
CONFIGURE DEVICE TYPE DISK PARALLELISM 1 BACKUP TYPE TO BACKUPSET;
```

## 7.4. Definir formato padrão de backup

```rman
CONFIGURE CHANNEL DEVICE TYPE DISK FORMAT '/opt/oracle/labbackup/rman/%d_%T_%U.bkp';
```

## 7.5. Mostrar configuração final

```rman
SHOW ALL;
```

---

## 8. Backup completo do banco

## 8.1. Backup completo com archivelogs

```rman
BACKUP DATABASE PLUS ARCHIVELOG;
```

## 8.2. Backup apenas do control file

```rman
BACKUP CURRENT CONTROLFILE;
```

## 8.3. Backup do SPFILE

```rman
BACKUP SPFILE;
```

## 8.4. Listar backups

```rman
LIST BACKUP SUMMARY;
LIST BACKUP OF DATABASE;
LIST BACKUP OF ARCHIVELOG ALL;
LIST BACKUP OF CONTROLFILE;
LIST BACKUP OF SPFILE;
```

---

## 9. Backup incremental

## 9.1. Backup incremental level 0

```rman
BACKUP INCREMENTAL LEVEL 0 DATABASE TAG 'BKP_L0_MOD3';
```

## 9.2. Gerar novas alterações no banco

Abrir outro terminal ou sair do RMAN momentaneamente e conectar como `app_rman`:

Conectar no CloudBeaver como `app_rman`.

```sql
BEGIN
  FOR i IN 201..350 LOOP
    INSERT INTO pedidos_lab (id_pedido, cliente, valor_total)
    VALUES (i, 'Cliente ' || i, i * 10);
  END LOOP;
  COMMIT;
END;
/
```

Voltar ao RMAN:

```bash
rman target /
```

## 9.3. Backup incremental level 1

```rman
BACKUP INCREMENTAL LEVEL 1 DATABASE TAG 'BKP_L1_MOD3';
```

## 9.4. Verificar backups incrementais

```rman
LIST BACKUP SUMMARY;
```

---

## 10. Backup de archivelogs

## 10.1. Forçar geração de archive log

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
ALTER SYSTEM SWITCH LOGFILE;
ALTER SYSTEM SWITCH LOGFILE;
ALTER SYSTEM ARCHIVE LOG CURRENT;
SELECT log_mode
FROM v$database;
```

Voltar ao RMAN:

```bash
rman target /
```

## 10.2. Executar backup de archivelogs

```rman
BACKUP ARCHIVELOG ALL TAG 'BKP_ARCH_MOD3';
```

## 10.3. Listar archivelogs copiados

```rman
LIST BACKUP OF ARCHIVELOG ALL;
```

---

## 11. Validação de backup e integridade

## 11.1. Validar o banco

```rman
VALIDATE DATABASE;
```

## 11.2. Validar backups existentes

```rman
RESTORE DATABASE VALIDATE;
RESTORE ARCHIVELOG ALL VALIDATE;
```

## 11.3. Validar schema

```rman
REPORT SCHEMA;
```

## 11.4. Procurar arquivos obsoletos

```rman
REPORT OBSOLETE;
```

## 11.5. Cruzar catálogo com arquivos físicos

```rman
CROSSCHECK BACKUP;
CROSSCHECK ARCHIVELOG ALL;
```

---

## 12. Cenário prático 1 - recuperação de instância

Este é o cenário mais simples e ajuda a mostrar o conceito de recuperação automática de instância.

## 12.1. Forçar parada abrupta

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
SHUTDOWN ABORT;
```

## 12.2. Subir o banco novamente

```sql
STARTUP;
```

## 12.3. Validar após o restart

```sql
SELECT instance_name, status FROM v$instance;
SELECT log_mode
FROM v$database;
```

## 12.4. Validar os dados da aplicação

Conectar no CloudBeaver como `app_rman`.

```sql
SELECT COUNT(*) FROM pedidos_lab;
```

### Observação

Nesse cenário, o Oracle executará recuperação de instância automaticamente, usando redo e mecanismos internos para restaurar consistência.

---

## 13. Cenário prático 2 - restore e recovery de um datafile/tablespace de laboratório

Este cenário deve ser executado em objeto próprio de laboratório, nunca em arquivo crítico do sistema.

## 13.1. Descobrir o diretório dos datafiles da PDB

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT file_name FROM dba_data_files ORDER BY file_id;
```

Identificar o diretório usado pelos datafiles existentes.  
Usaremos o mesmo diretório para o datafile do laboratório.

## 13.2. Criar tablespace dedicada de laboratório

Substituir o caminho abaixo conforme o diretório encontrado no passo anterior.

```sql
CREATE TABLESPACE ts_rman_lab
  DATAFILE '/opt/oracle/oradata/FREE/FREEPDB1/ts_rman_lab01.dbf'
  SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE 500M;
```

## 13.3. Atribuir cota ao usuário

```sql
ALTER USER app_rman QUOTA UNLIMITED ON ts_rman_lab;
```

## 13.4. Criar tabela na nova tablespace

Conectar como `app_rman`:

Conectar no CloudBeaver como `app_rman`.

```sql
CREATE TABLE pedidos_ts_rman
TABLESPACE ts_rman_lab
AS
SELECT * FROM pedidos_lab;
```

Gerar mais dados:

```sql
INSERT INTO pedidos_ts_rman
SELECT id_pedido + 1000, cliente || ' X', valor_total + 1, SYSDATE
FROM pedidos_lab;

COMMIT;
SELECT COUNT(*) FROM pedidos_ts_rman;
```

## 13.5. Fazer backup da tablespace

Voltar ao RMAN:

```bash
rman target /
```

```rman
BACKUP TABLESPACE ts_rman_lab TAG 'BKP_TS_RMAN_LAB';
```

## 13.6. Identificar o datafile da tablespace

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT file_id, file_name
FROM dba_data_files
WHERE tablespace_name = 'TS_RMAN_LAB';
```

Anotar o `file_id` e o `file_name`.

## 13.7. Simular falha de mídia

### Passo 1 - colocar a tablespace offline

```sql
ALTER TABLESPACE ts_rman_lab OFFLINE IMMEDIATE;
```

### Passo 2 - encerrar a sessão administrativa atual

### Passo 3 - renomear o datafile no sistema operacional

Dentro do container:

```bash
mv /opt/oracle/oradata/FREE/FREEPDB1/ts_rman_lab01.dbf /opt/oracle/oradata/FREE/FREEPDB1/ts_rman_lab01.dbf.broken
```

## 13.8. Restaurar e recuperar com RMAN

```bash
rman target /
```

Se quiser usar o número do datafile:

```rman
RESTORE DATAFILE <FILE_ID>;
RECOVER DATAFILE <FILE_ID>;
```

Ou, se preferir por tablespace:

```rman
RESTORE TABLESPACE ts_rman_lab;
RECOVER TABLESPACE ts_rman_lab;
```

## 13.9. Colocar a tablespace online novamente

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
ALTER TABLESPACE ts_rman_lab ONLINE;
```

## 13.10. Validar a recuperação

Conectar como `app_rman`:

Conectar no CloudBeaver como `app_rman`.

```sql
SELECT COUNT(*) FROM pedidos_ts_rman;
SELECT * FROM pedidos_ts_rman FETCH FIRST 10 ROWS ONLY;
```

---

## 14. Cenário prático 3 - recuperação de tablespace

Como o restore/recovery por tablespace já foi demonstrado no cenário anterior, podemos reforçar a ideia executando novamente os comandos em termos de tablespace, em vez de datafile específico.

Exemplo de sequência:

```rman
SQL "ALTER TABLESPACE ts_rman_lab OFFLINE IMMEDIATE";
RESTORE TABLESPACE ts_rman_lab;
RECOVER TABLESPACE ts_rman_lab;
SQL "ALTER TABLESPACE ts_rman_lab ONLINE";
```

Esse cenário é útil para mostrar que a recuperação pode ser orientada por unidade lógica do banco.

---

## 15. Blocos corrompidos - abordagem prática controlada

A recuperação de bloco corrompido existe no Oracle, mas a simulação intencional de corrupção em laboratório pode ser arriscada e desnecessariamente destrutiva.

Por isso, a abordagem recomendada neste módulo é:

1. explicar o conceito;
2. usar comandos de validação para detectar corrupção;
3. mostrar a forma do comando de recuperação de bloco, sem necessariamente induzir corrupção real em aula.

## 15.1. Validar buscando corrupção

```rman
BACKUP VALIDATE DATABASE;
```

ou

```rman
VALIDATE DATABASE;
```

## 15.2. Consultar visões de corrupção

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
SELECT * FROM v$database_block_corruption;
```

## 15.3. Exemplo de comando de block recover

```rman
BLOCKRECOVER DATAFILE <FILE_ID> BLOCK <BLOCK_NUMBER>;
```

### Observação

Esse comando deverá ser apresentado como recurso avançado. Em laboratório simples, faz mais sentido demonstrar a observação e a capacidade da ferramenta do que provocar corrupção manualmente.

---

## 16. Control file, SPFILE e metadados

## 16.1. Backup do control file

```rman
BACKUP CURRENT CONTROLFILE;
```

## 16.2. Backup do SPFILE

```rman
BACKUP SPFILE;
```

## 16.3. Listar esses backups

```rman
LIST BACKUP OF CONTROLFILE;
LIST BACKUP OF SPFILE;
```

## 16.4. Restaurar apenas para validação conceitual

A restauração real de control file deverá ser tratada como tópico mais sensível. Em laboratório básico, faz mais sentido mostrar os comandos e discutir o papel desses arquivos.

Exemplo:

```rman
RESTORE CONTROLFILE FROM AUTOBACKUP;
```

ou

```rman
RESTORE SPFILE FROM AUTOBACKUP;
```

Esses comandos não precisam ser executados em todas as turmas, mas devem constar do material.

---

## 17. Retenção e limpeza

## 17.1. Ver backups obsoletos

```rman
REPORT OBSOLETE;
```

## 17.2. Remover backups obsoletos

```rman
DELETE NOPROMPT OBSOLETE;
```

## 17.3. Listar backups após limpeza

```rman
LIST BACKUP SUMMARY;
```

---

## 18. Consultas úteis para observação do laboratório

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

## 18.1. Ver modo de arquivamento

```sql
SELECT log_mode
FROM v$database;
```

## 18.2. Ver parâmetros da FRA

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest';
SELECT name, value
FROM v$parameter
WHERE name = 'db_recovery_file_dest_size';
```

## 18.3. Ver datafiles

```sql
SELECT file_id, file_name, tablespace_name, status
FROM dba_data_files
ORDER BY file_id;
```

## 18.4. Ver archived logs conhecidos

```sql
SELECT sequence#, archived, status, first_time, next_time
FROM v$archived_log
ORDER BY sequence#;
```

## 18.5. Ver status das tablespaces

```sql
SELECT tablespace_name, status
FROM dba_tablespaces
ORDER BY tablespace_name;
```

## 18.6. Ver sessões

```sql
SELECT sid, serial#, username, status
FROM v$session
WHERE username IS NOT NULL
ORDER BY username;
```

## 18.7. Diagnóstico enxuto da FRA

```sql
SELECT name,
       space_limit / 1024 / 1024 AS fra_limit_mb,
       space_used / 1024 / 1024 AS fra_used_mb,
       space_reclaimable / 1024 / 1024 AS fra_reclaimable_mb
FROM v$recovery_file_dest;

SELECT file_type,
       percent_space_used,
       percent_space_reclaimable
FROM v$flash_recovery_area_usage
ORDER BY file_type;
```

## 18.8. Diagnóstico enxuto de archived logs e RMAN

```sql
SELECT sequence#,
       archived,
       status,
       first_time
FROM v$archived_log
WHERE rownum <= 10
ORDER BY sequence# DESC;

SELECT session_key,
       input_type,
       status,
       start_time,
       end_time
FROM v$rman_backup_job_details
ORDER BY start_time DESC
FETCH FIRST 10 ROWS ONLY;
```

## 18.9. Validação final do módulo

```sql
SELECT name,
       open_mode,
       log_mode
FROM v$database;

SELECT name,
       value
FROM v$parameter
WHERE name IN ('db_recovery_file_dest', 'db_recovery_file_dest_size')
ORDER BY name;
```

---

## 18.10. Exemplos adicionais de backup e recuperação

### Backup com formato de arquivo definido

Quando houver necessidade de controlar explicitamente o nome e local dos arquivos, podemos usar `FORMAT`:

```rman
BACKUP DATABASE
FORMAT '/opt/oracle/labbackup/rman/db_%U.bkp';
```

### Restore e recover completos do banco

Exemplo clássico de recuperação completa:

```rman
RESTORE DATABASE;
RECOVER DATABASE;
```

### Exemplo de Point-in-Time Recovery (PITR)

Em cenário de erro lógico ou necessidade de voltar para um ponto específico no tempo:

```rman
RUN {
  SET UNTIL TIME "TO_DATE('2026-04-14 10:00:00','YYYY-MM-DD HH24:MI:SS')";
  RESTORE DATABASE;
  RECOVER DATABASE;
}
```

Após PITR, validar a necessidade de abertura com `RESETLOGS` conforme o cenário e o estado do banco.

## 19. Limpeza do laboratório

Se quisermos repetir a prática do zero, poderemos remover os objetos criados.

## 19.1. Remover tabela e tablespace de laboratório

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;

DROP TABLESPACE ts_rman_lab INCLUDING CONTENTS AND DATAFILES;
```

Conectar como `app_rman` e remover a tabela base, se desejado:

Conectar no CloudBeaver como `app_rman`.

```sql
DROP TABLE pedidos_lab PURGE;
```

## 19.2. Remover usuário

Conectar como SYSDBA ou SYSTEM:

```sql
DROP USER app_rman CASCADE;
```

## 19.3. Opcional - voltar o banco para NOARCHIVELOG

### Atenção
Esse passo não é obrigatório e só deverá ser executado se houver real necessidade de reverter o laboratório.

Conectar como SYSDBA:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE NOARCHIVELOG;
ALTER DATABASE OPEN;
SELECT log_mode
FROM v$database;
```

---

## 20. Resultado esperado da prática

Ao final deste módulo, deveremos ter exercitado:

- configuração da FRA;
- habilitação do modo ARCHIVELOG;
- uso básico do RMAN;
- backup completo;
- backup incremental;
- backup de archivelogs;
- validação de backups;
- uso de retenção e limpeza;
- recuperação automática de instância;
- restore e recovery de datafile/tablespace em cenário controlado;
- observação de recursos para validação e block recover.

---

## 21. Referências oficiais úteis

### Oracle Database Free em container
- https://github.com/gvenzl/oci-oracle-free

### RMAN - Getting Started
- https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/getting-started-rman.html

### RMAN Backup Concepts
- https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-backup-concepts.html

### RESTORE command
- https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/RESTORE.html

### Archived Redo Log Files
- https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-archived-redo-log-files.html

### Configure Recovery Settings tutorial
- https://docs.oracle.com/en/database/oracle/oracle-database/tutorial-conf-rec/index.html
