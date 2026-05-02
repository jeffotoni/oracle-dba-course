# Módulo 2 – Prática  
## Segurança, Controle de Acesso e Carga de Dados em Volume

## Visão geral

Neste módulo usaremos um laboratório prático para consolidar os tópicos de segurança e carga de dados em volume no Oracle.

A prática será organizada em cinco blocos:

1. preparação do ambiente;
2. criação de usuários, perfis, privilégios e roles;
3. observação das visões de segurança e controle de acesso;
4. auditoria e rastreabilidade;
5. carga de dados com SQL*Loader, tabelas externas e Oracle Data Pump.

A proposta é manter um laboratório simples, reproduzível e alinhado ao ambiente já adotado nos módulos anteriores.

---

## Ambiente utilizado

Usaremos:

- Podman;
- Oracle Database Free em container;
- CloudBeaver para consultas e administração básica;
- arquivos CSV e arquivos de controle para simular carga em volume;
- diretórios internos do container para leitura, escrita, exportação e importação de arquivos.

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
- **diretório de laboratório dentro do container**: `/opt/oracle/labdata`

---

## 1. Subida do ambiente com Podman

## 1.1. Estrutura recomendada de pastas

```text
modulo2-seguranca-carga/
├── compose.yaml
├── labdata/
│   ├── produtos.csv
│   ├── produtos.ctl
│   └── README.txt
└── scripts/
```

## 1.2. compose.yaml

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
      - ./labdata:/opt/oracle/labdata
```

## 1.3. Comandos para subir o ambiente

```bash
podman compose up -d
podman ps
podman logs -f oracle-free
```

## 1.4. Validação inicial

Depois que o banco estiver disponível, deveremos validar:

Conectar no CloudBeaver como `system` em `FREEPDB1`.

Consulta rápida:

```sql
SELECT name, open_mode FROM v$pdbs;
SELECT instance_name, status FROM v$instance;
SELECT USER AS current_user
FROM dual;
```

## 1.5. Checklist SQL mínimo do módulo

```sql
SELECT USER AS current_user
FROM dual;

SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

---

## 2. Bloco prático – criação de perfis, usuários, privilégios e roles

## 2.1. Entrar como administrador

Conectar no CloudBeaver como `system`.

## 2.2. Criar um perfil de laboratório

```sql
CREATE PROFILE prof_lab_m2 LIMIT
  SESSIONS_PER_USER 3
  FAILED_LOGIN_ATTEMPTS 5
  PASSWORD_LIFE_TIME 90
  PASSWORD_REUSE_TIME 30
  PASSWORD_REUSE_MAX 5
  PASSWORD_LOCK_TIME 1/24
  CONNECT_TIME UNLIMITED
  IDLE_TIME 30;
```

## 2.3. Criar usuários do laboratório

```sql
CREATE USER app_owner IDENTIFIED BY AppOwner123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 100M ON USERS
  PROFILE prof_lab_m2;

CREATE USER analista IDENTIFIED BY Analista123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 50M ON USERS
  PROFILE prof_lab_m2;

CREATE USER operador_carga IDENTIFIED BY Carga123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 50M ON USERS
  PROFILE prof_lab_m2;

CREATE USER app_clone IDENTIFIED BY Clone123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 100M ON USERS
  PROFILE prof_lab_m2;
```

## 2.4. Criar roles

```sql
CREATE ROLE role_leitura_m2;
CREATE ROLE role_carga_m2;
CREATE ROLE role_analise_m2;
```

## 2.5. Conceder privilégios básicos às roles

```sql
GRANT CREATE SESSION TO role_leitura_m2;
GRANT CREATE SESSION TO role_carga_m2;
GRANT CREATE SESSION TO role_analise_m2;
```

## 2.6. Conceder privilégios diretos ao dono da aplicação

```sql
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_owner;
GRANT CREATE SESSION TO analista;
GRANT CREATE SESSION TO operador_carga;
GRANT CREATE SESSION TO app_clone;
```

## 2.7. Vincular roles aos usuários

```sql
GRANT role_leitura_m2 TO analista;
GRANT role_carga_m2 TO operador_carga;
```

---

## 3. Bloco prático – criação de objetos no schema da aplicação

## 3.1. Conectar como APP_OWNER

Conectar no CloudBeaver como `app_owner`.

## 3.2. Criar tabela de exemplo

```sql
CREATE TABLE produtos (
  id_produto      NUMBER PRIMARY KEY,
  nome_produto    VARCHAR2(100),
  categoria       VARCHAR2(50),
  preco           NUMBER(10,2),
  data_cadastro   DATE DEFAULT SYSDATE
);
```

## 3.3. Inserir dados de exemplo

```sql
INSERT INTO produtos (id_produto, nome_produto, categoria, preco) VALUES (1, 'Notebook', 'Informatica', 4500.00);
INSERT INTO produtos (id_produto, nome_produto, categoria, preco) VALUES (2, 'Mouse', 'Perifericos', 120.00);
INSERT INTO produtos (id_produto, nome_produto, categoria, preco) VALUES (3, 'Teclado', 'Perifericos', 250.00);
COMMIT;
```

## 3.4. Conceder privilégios de objeto

Conectar novamente como `system` ou outro usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
GRANT SELECT ON app_owner.produtos TO role_leitura_m2;
GRANT SELECT, INSERT ON app_owner.produtos TO role_carga_m2;
```

---

## 4. Bloco prático – consultas de segurança e controle de acesso

## 4.1. Ver usuários existentes

```sql
SELECT username, account_status, profile, created
FROM dba_users
ORDER BY username;
```

## 4.2. Ver roles existentes

```sql
SELECT role
FROM dba_roles
ORDER BY role;
```

## 4.3. Ver privilégios de sistema concedidos a usuários

```sql
SELECT grantee, privilege
FROM dba_sys_privs
WHERE grantee IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA')
ORDER BY grantee, privilege;
```

## 4.4. Ver privilégios de objeto

```sql
SELECT grantee, owner, table_name, privilege
FROM dba_tab_privs
WHERE owner = 'APP_OWNER'
ORDER BY grantee, table_name, privilege;
```

## 4.5. Ver roles concedidas

```sql
SELECT grantee, granted_role
FROM dba_role_privs
WHERE grantee IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA')
ORDER BY grantee, granted_role;
```

## 4.6. Ver perfil do usuário

```sql
SELECT username, profile
FROM dba_users
WHERE username IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA');
```

## 4.7. Teste prático de leitura com o usuário ANALISTA

Conectar no CloudBeaver como `analista`.

```sql
SELECT * FROM app_owner.produtos;
```

## 4.8. Teste prático de carga com o usuário OPERADOR_CARGA

Conectar no CloudBeaver como `operador_carga`.

```sql
INSERT INTO app_owner.produtos (id_produto, nome_produto, categoria, preco)
VALUES (4, 'Monitor', 'Perifericos', 980.00);
COMMIT;
```

---

## 5. Bloco prático – auditoria e rastreabilidade

## 5.1. Criar uma política simples de auditoria de logon

Conectar como usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
CREATE AUDIT POLICY pol_logon_m2 ACTIONS LOGON;
AUDIT POLICY pol_logon_m2;
```

## 5.2. Criar política de auditoria para SELECT na tabela PRODUTOS

```sql
CREATE AUDIT POLICY pol_select_produtos_m2
  ACTIONS SELECT ON app_owner.produtos;

AUDIT POLICY pol_select_produtos_m2;
```

## 5.3. Executar ações para gerar evidência

Conectar como analista:

Conectar no CloudBeaver como `analista`.

```sql
SELECT * FROM app_owner.produtos;
```

## 5.4. Consultar trilha de auditoria unificada

Conectar como usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
SELECT event_timestamp,
       dbusername,
       action_name,
       object_schema,
       object_name,
       return_code
FROM unified_audit_trail
ORDER BY event_timestamp DESC
FETCH FIRST 30 ROWS ONLY;
```

## 5.5. Desabilitar política, se necessário

```sql
NOAUDIT POLICY pol_select_produtos_m2;
NOAUDIT POLICY pol_logon_m2;
```

---

## 6. Bloco prático – carga de dados com SQL*Loader

## 6.1. Criar arquivo CSV em `labdata/produtos.csv`

```csv
10,Headset,Audio,350.00
11,Webcam,Video,280.00
12,SSD 1TB,Armazenamento,620.00
13,Cadeira Gamer,Mobiliario,1400.00
```

## 6.2. Criar tabela de destino

Conectar como `app_owner`:

Conectar no CloudBeaver como `app_owner`.

```sql
CREATE TABLE produtos_carga (
  id_produto      NUMBER,
  nome_produto    VARCHAR2(100),
  categoria       VARCHAR2(50),
  preco           NUMBER(10,2)
);
```

## 6.3. Criar arquivo de controle `labdata/produtos.ctl`

```text
LOAD DATA
INFILE '/opt/oracle/labdata/produtos.csv'
INTO TABLE app_owner.produtos_carga
FIELDS TERMINATED BY ','
(
  id_produto,
  nome_produto,
  categoria,
  preco
)
```

## 6.4. Executar SQL*Loader dentro do container

```bash
podman exec -it oracle-free bash
sqlldr app_owner/AppOwner123@//localhost:1521/FREEPDB1 control=/opt/oracle/labdata/produtos.ctl log=/opt/oracle/labdata/produtos_sqlldr.log
```

## 6.5. Validar carga

Conectar no CloudBeaver como `app_owner`.

```sql
SELECT * FROM produtos_carga ORDER BY id_produto;
```

---

## 7. Bloco prático – leitura com tabelas externas

## 7.1. Criar diretório lógico no banco

Conectar como usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
CREATE OR REPLACE DIRECTORY lab_dir AS '/opt/oracle/labdata';
GRANT READ, WRITE ON DIRECTORY lab_dir TO app_owner;
```

## 7.2. Criar tabela externa

Conectar como `app_owner`:

Conectar no CloudBeaver como `app_owner`.

```sql
CREATE TABLE ext_produtos (
  id_produto      NUMBER,
  nome_produto    VARCHAR2(100),
  categoria       VARCHAR2(50),
  preco           NUMBER(10,2)
)
ORGANIZATION EXTERNAL
(
  TYPE ORACLE_LOADER
  DEFAULT DIRECTORY lab_dir
  ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE
    FIELDS TERMINATED BY ','
    MISSING FIELD VALUES ARE NULL
    (
      id_produto,
      nome_produto,
      categoria,
      preco
    )
  )
  LOCATION ('produtos.csv')
)
REJECT LIMIT UNLIMITED;
```

## 7.3. Consultar tabela externa

```sql
SELECT * FROM ext_produtos ORDER BY id_produto;
```

## 7.4. Inserir o conteúdo da tabela externa em uma tabela interna

```sql
CREATE TABLE produtos_ext_import AS
SELECT * FROM ext_produtos;
```

## 7.5. Validar importação

```sql
SELECT COUNT(*) FROM produtos_ext_import;
SELECT * FROM produtos_ext_import ORDER BY id_produto;
```

---

## 8. Bloco prático – Oracle Data Pump

## 8.1. Criar diretório lógico para exportação/importação

Conectar como usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
CREATE OR REPLACE DIRECTORY dpump_dir AS '/opt/oracle/labdata';
GRANT READ, WRITE ON DIRECTORY dpump_dir TO system;
GRANT READ, WRITE ON DIRECTORY dpump_dir TO app_owner;
GRANT READ, WRITE ON DIRECTORY dpump_dir TO app_clone;
```

## 8.2. Exportar o schema APP_OWNER

Dentro do container:

```bash
podman exec -it oracle-free bash
expdp system/Senha123@//localhost:1521/FREEPDB1   DIRECTORY=dpump_dir   DUMPFILE=app_owner_m2.dmp   LOGFILE=exp_app_owner_m2.log   SCHEMAS=APP_OWNER
```

## 8.3. Preparar o schema APP_CLONE

Conectar como usuário administrativo:

Conectar no CloudBeaver como `system`.

```sql
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_clone;
```

## 8.4. Importar para APP_CLONE com remapeamento

Dentro do container:

```bash
podman exec -it oracle-free bash
impdp system/Senha123@//localhost:1521/FREEPDB1   DIRECTORY=dpump_dir   DUMPFILE=app_owner_m2.dmp   LOGFILE=imp_app_clone_m2.log   REMAP_SCHEMA=APP_OWNER:APP_CLONE
```

## 8.5. Validar importação

Conectar no CloudBeaver como `app_clone`.

```sql
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT COUNT(*) FROM produtos;
SELECT * FROM produtos ORDER BY id_produto;
```

---

## 9. Consultas úteis para observação do laboratório

## 9.1. Diagnóstico enxuto de segurança

```sql
SELECT username,
       account_status,
       default_tablespace,
       profile
FROM dba_users
WHERE username IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA', 'APP_CLONE')
ORDER BY username;

SELECT grantee,
       granted_role
FROM dba_role_privs
WHERE grantee IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA', 'APP_CLONE')
ORDER BY grantee, granted_role;

SELECT privilege
FROM session_privs
ORDER BY privilege;
```

## 9.2. Diagnóstico enxuto de objetos e grants

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;

SELECT owner,
       table_name,
       privilege,
       grantee
FROM dba_tab_privs
WHERE owner = 'APP_OWNER'
ORDER BY table_name, privilege, grantee;
```

## 9.3. Validação final do módulo

```sql
SELECT username,
       account_status
FROM dba_users
WHERE username IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA', 'APP_CLONE')
ORDER BY username;

SELECT owner,
       object_name,
       object_type
FROM all_objects
WHERE owner = 'APP_OWNER'
ORDER BY object_type, object_name;
```

## 9.4. Diretórios criados

```sql
SELECT directory_name, directory_path
FROM dba_directories
ORDER BY directory_name;
```

## 9.5. Objetos do schema APP_OWNER

```sql
SELECT object_name, object_type, status
FROM dba_objects
WHERE owner = 'APP_OWNER'
ORDER BY object_type, object_name;
```

## 9.6. Tabelas do schema atual

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

## 9.7. Colunas de uma tabela

```sql
SELECT column_name, data_type, data_length
FROM user_tab_columns
WHERE table_name = 'PRODUTOS'
ORDER BY column_id;
```

## 9.8. Sessões ativas

```sql
SELECT sid, serial#, username, status
FROM v$session
WHERE username IS NOT NULL
ORDER BY username;
```

---

## 10. Limpeza do laboratório

Se quisermos repetir a prática do zero, poderemos remover os objetos criados.

## 10.1. Remover políticas de auditoria

```sql
NOAUDIT POLICY pol_select_produtos_m2;
NOAUDIT POLICY pol_logon_m2;

DROP AUDIT POLICY pol_select_produtos_m2;
DROP AUDIT POLICY pol_logon_m2;
```

## 10.2. Remover tabelas

Conectar como `app_owner`:

```sql
DROP TABLE produtos_ext_import PURGE;
DROP TABLE ext_produtos;
DROP TABLE produtos_carga PURGE;
DROP TABLE produtos PURGE;
```

Conectar como `app_clone`:

```sql
DROP TABLE produtos PURGE;
```

## 10.3. Remover diretórios, roles, usuários e perfil

Conectar como usuário administrativo:

```sql
DROP DIRECTORY lab_dir;
DROP DIRECTORY dpump_dir;

DROP ROLE role_leitura_m2;
DROP ROLE role_carga_m2;
DROP ROLE role_analise_m2;

DROP USER analista CASCADE;
DROP USER operador_carga CASCADE;
DROP USER app_clone CASCADE;
DROP USER app_owner CASCADE;

DROP PROFILE prof_lab_m2;
```

---

## 11. Resultado esperado da prática

Ao final deste módulo, deveremos ter exercitado:

- criação e administração de usuários;
- aplicação de perfis;
- concessão de privilégios e roles;
- consulta a visões administrativas relacionadas a segurança;
- geração e leitura de evidências de auditoria;
- carga em volume com SQL*Loader;
- leitura de arquivos com tabelas externas;
- exportação e importação lógica com Oracle Data Pump.

---

## 12. Referências oficiais úteis

### Oracle Database Free em container
- https://github.com/gvenzl/oci-oracle-free

### Privilégios e roles
- https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-privilege-and-role-authorization.html

### Unified Audit
- https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-audit-policies.html

### SQL*Loader
- https://docs.oracle.com/en/database/oracle/oracle-database/21/sutil/oracle-sql-loader.html
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/sql-loader-control-file.html

### External Tables
- https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-external-tables.html
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/using-oracle-external-tables-examples.html

### Oracle Data Pump
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/oracle-data-pump.html
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/examples-using-oracle-data-pump-export.html
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/examples-using-oracle-data-pump-import.html

---

## 13. Compatibilidade com Podman

Este roteiro foi pensado para execução em `gvenzl/oracle-free` em container.

### 13.1. Checklist rápido antes de iniciar

No host:

```bash
podman ps --format '{{.Names}}\t{{.Status}}' | grep oracle-free
```

No container:

```bash
podman exec -it oracle-free bash
```

```bash
which sqlplus
which sqlldr
which expdp
which impdp
```

Se algum utilitário não estiver disponível, ajustar a imagem/tag do Oracle Free antes da aula.

### 13.2. Checklist SQL inicial (sempre executar)

Conectar no CloudBeaver como `system`.

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id, name, open_mode FROM v$pdbs ORDER BY con_id;
```

Regra: todos os objetos de laboratório devem ser criados na PDB (`FREEPDB1`).

### 13.3. Auditoria no container

Se houver erro de privilégio ao criar política de auditoria com `SYSTEM`, executar etapa de auditoria com `SYS AS SYSDBA`.

### 13.4. Volumes e arquivos de carga

A pasta mapeada no compose deve existir no host e no container:

- host: `./labdata`
- container: `/opt/oracle/labdata`

Validação:

```bash
podman exec -it oracle-free bash -lc 'ls -la /opt/oracle/labdata'
```

### 13.5. Resultado esperado de compatibilidade

Antes da prática completa, validar:

- conexão ao `FREEPDB1` funcionando;
- utilitários `sqlldr`, `expdp`, `impdp` disponíveis;
- diretório `/opt/oracle/labdata` acessível;
- criação de usuário/tabela de teste executando sem erro.

---

## 14. Automação opcional do laboratório (bash)

Para acelerar execução em aula, foi gerada a estrutura:

`/Users/jeffotoni/gitprojetos/puc/modulo2-material/modulo2-seguranca-carga`

Com conteúdo:

- `compose.yaml`
- `labdata/produtos.csv`
- `labdata/produtos.ctl`
- `labdata/README.txt`
- `scripts/01-up.sh`
- `scripts/02-validate.sh`
- `scripts/03-sqlldr.sh`
- `scripts/04-expdp.sh`
- `scripts/05-impdp.sh`
- `scripts/06-down.sh`

### Sequência sugerida

```bash
cd /Users/jeffotoni/gitprojetos/puc/modulo2-material/modulo2-seguranca-carga
./scripts/01-up.sh
./scripts/02-validate.sh
```

Depois de executar os blocos SQL de segurança/perfis/roles conforme este roteiro:

```bash
./scripts/03-sqlldr.sh
./scripts/04-expdp.sh
./scripts/05-impdp.sh
```

Finalização:

```bash
./scripts/06-down.sh
```

### Observação sobre CDC no Oracle Free do laboratório

O módulo teórico cita CDC (`GoldenGate`) como referência corporativa. Neste laboratório com Oracle Free em Podman, o escopo prático fica em:

- SQL*Loader;
- tabela externa;
- Data Pump.

Isso mantém a prática executável no ambiente de aula sem dependências extras de licenciamento e infraestrutura.
