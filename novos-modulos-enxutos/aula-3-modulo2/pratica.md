# Laboratório - Aula 3

Este laboratório executa o Módulo 2 em uma sequência única. Os comandos SQL podem ser executados no Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente. Os binários nativos do Oracle são executados dentro do container com Podman.

## 1. Ambiente do laboratório

Use a versão `oracle-free-full-23ai` já adotada nas outras aulas.

### 1.1. Subir o Oracle

Execute no terminal do host:

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

Se o container já existir, não repita o `run`. Neste caso, use:

```bash
podman start oracle-free-full-23ai
```

Valide o estado:

```bash
podman ps
podman logs --tail 40 oracle-free-full-23ai
```

O laboratório usa:

```text
Container: oracle-free-full-23ai
Host: localhost
Porta no host: 1522
Porta no container: 1521
Service Name: FREEPDB1
```

### 1.2. Validar os binários Oracle

Entre no container:

```bash
podman exec -it oracle-free-full-23ai bash
```

Use `command -v`, que está disponível no ambiente, em vez de depender do comando `which`:

```bash
command -v sqlplus
command -v sqlldr
command -v expdp
command -v impdp
```

Valide as versões e ajudas:

```bash
sqlplus -v
sqlldr -help | head
expdp help=y | head
impdp help=y | head
```

Saia do container:

```bash
exit
```

### 1.3. Conectar na IDE

Crie uma conexão com:

```text
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: SYSTEM
Password: OraclePwd123
Role: Normal
```

O `SYSTEM` será usado para preparar o laboratório. O trabalho da aplicação será feito com `APP_OWNER` e as validações de acesso serão feitas com `ANALISTA` e `OPERADOR_CARGA`.

## 2. Validar a sessão

Execute conectado como `SYSTEM` na `FREEPDB1`:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

```sql
SELECT instance_name,
       status
FROM v$instance;
```

```sql
SELECT name,
       open_mode,
       cdb
FROM v$database;
```

```sql
SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

O resultado esperado é uma sessão no container `FREEPDB1`, com a PDB aberta para leitura e escrita.

## 3. Criar o perfil de laboratório

O perfil concentra regras comuns para os usuários do laboratório. Execute como `SYSTEM`:

```sql
CREATE PROFILE prof_lab_m2 LIMIT
  SESSIONS_PER_USER 3
  FAILED_LOGIN_ATTEMPTS 5
  PASSWORD_LIFE_TIME 90
  IDLE_TIME 30;
```

O perfil não concede permissões. Ele define limites de sessão e políticas de senha.

## 4. Criar os usuários

Ainda como `SYSTEM`, crie contas com responsabilidades diferentes:

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
  QUOTA 100M ON USERS
  PROFILE prof_lab_m2;

CREATE USER app_clone IDENTIFIED BY Clone123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA 100M ON USERS
  PROFILE prof_lab_m2;
```

Conceda somente a capacidade básica de conexão e criação necessária:

```sql
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_owner;
GRANT CREATE SESSION TO analista;
GRANT CREATE SESSION TO operador_carga;
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_clone;
```

Valide as contas:

```sql
SELECT username,
       account_status,
       profile,
       default_tablespace
FROM dba_users
WHERE username IN ('APP_OWNER', 'ANALISTA', 'OPERADOR_CARGA', 'APP_CLONE')
ORDER BY username;
```

## 5. Criar roles e organizar o acesso

Ainda como `SYSTEM`, crie roles com responsabilidades claras:

```sql
CREATE ROLE role_leitura_m2;
CREATE ROLE role_carga_m2;
CREATE ROLE role_analise_m2;

GRANT CREATE SESSION TO role_leitura_m2;
GRANT CREATE SESSION TO role_carga_m2;
GRANT CREATE SESSION TO role_analise_m2;

GRANT role_leitura_m2 TO analista;
GRANT role_carga_m2 TO operador_carga;
GRANT role_analise_m2 TO analista;
```

Neste momento as roles têm apenas a permissão de conexão. Os privilégios de objeto serão concedidos depois que `APP_OWNER` criar a tabela.

## 6. Criar a tabela da aplicação

Abra uma nova conexão na IDE:

```text
User: APP_OWNER
Password: AppOwner123
Service Name: FREEPDB1
```

Confirme o contexto:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
```

Crie a tabela no schema `APP_OWNER`:

```sql
CREATE TABLE produtos (
  id_produto    NUMBER PRIMARY KEY,
  nome_produto  VARCHAR2(100) NOT NULL,
  categoria     VARCHAR2(50) NOT NULL,
  preco         NUMBER(10,2) NOT NULL,
  data_cadastro DATE DEFAULT SYSDATE NOT NULL
);
```

Insira os dados iniciais:

```sql
INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (1, 'Notebook', 'Informatica', 4500.00);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (2, 'Mouse', 'Perifericos', 120.00);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (3, 'Teclado', 'Perifericos', 250.00);

COMMIT;
```

Valide como proprietário:

```sql
SELECT *
FROM produtos
ORDER BY id_produto;
```

## 7. Conceder privilégios de objeto

Volte para a conexão `SYSTEM` e conceda os privilégios depois que a tabela existir:

```sql
GRANT SELECT ON app_owner.produtos TO role_leitura_m2;
GRANT SELECT, INSERT ON app_owner.produtos TO role_carga_m2;
GRANT SELECT ON app_owner.produtos TO role_analise_m2;
```

Confira as roles e os privilégios:

```sql
SELECT grantee,
       granted_role
FROM dba_role_privs
WHERE grantee IN ('ANALISTA', 'OPERADOR_CARGA')
ORDER BY grantee, granted_role;
```

```sql
SELECT grantee,
       owner,
       table_name,
       privilege
FROM dba_tab_privs
WHERE owner = 'APP_OWNER'
  AND table_name = 'PRODUTOS'
ORDER BY grantee, privilege;
```

## 8. Testar as responsabilidades

### 8.1. Testar como `ANALISTA`

Conecte como:

```text
User: ANALISTA
Password: Analista123
Service Name: FREEPDB1
```

A consulta deve funcionar:

```sql
SELECT *
FROM app_owner.produtos
ORDER BY id_produto;
```

Uma tentativa de inserir deve falhar, pois `ANALISTA` recebeu leitura:

```sql
INSERT INTO app_owner.produtos (id_produto, nome_produto, categoria, preco)
VALUES (99, 'Teste Analista', 'Teste', 1.00);
```

O erro de privilégio é parte da demonstração do menor privilégio.

### 8.2. Testar como `OPERADOR_CARGA`

Conecte como:

```text
User: OPERADOR_CARGA
Password: Carga123
Service Name: FREEPDB1
```

A consulta e a inserção devem funcionar:

```sql
SELECT *
FROM app_owner.produtos
ORDER BY id_produto;
```

```sql
INSERT INTO app_owner.produtos (id_produto, nome_produto, categoria, preco)
VALUES (4, 'Monitor', 'Video', 900.00);

COMMIT;
```

O operador de carga não deve criar usuários ou alterar a estrutura administrativa do banco.

## 9. Habilitar auditoria e gerar evidência

Volte para `SYSTEM`. Se ocorrer erro de privilégio na criação da política, repita esta etapa em uma sessão `SYS AS SYSDBA`.

Crie uma política de logon:

```sql
CREATE AUDIT POLICY pol_logon_m2
  ACTIONS LOGON;

AUDIT POLICY pol_logon_m2;
```

Crie uma política para leitura da tabela:

```sql
CREATE AUDIT POLICY pol_select_produtos_m2
  ACTIONS SELECT ON app_owner.produtos;

AUDIT POLICY pol_select_produtos_m2;
```

Gere evidência conectando como `ANALISTA` e executando:

```sql
SELECT *
FROM app_owner.produtos
ORDER BY id_produto;
```

Volte para `SYSTEM` e leia a trilha:

```sql
SELECT event_timestamp,
       dbusername,
       action_name,
       object_schema,
       object_name,
       return_code
FROM unified_audit_trail
WHERE dbusername IN ('ANALISTA', 'OPERADOR_CARGA')
ORDER BY event_timestamp DESC
FETCH FIRST 30 ROWS ONLY;
```

### 9.1. Acompanhar a trilha em outro terminal

O `SQL*Plus` não possui um `watch` nativo. Para uma demonstração contínua, use outro terminal do host:

```bash
while true; do
  clear
  podman exec oracle-free-full-23ai sqlplus -s system/OraclePwd123@//localhost:1521/FREEPDB1 <<'SQL'
SET PAGESIZE 50
SET LINESIZE 180
SELECT event_timestamp,
       dbusername,
       action_name,
       object_schema,
       object_name,
       return_code
FROM unified_audit_trail
ORDER BY event_timestamp DESC
FETCH FIRST 10 ROWS ONLY;
EXIT;
SQL
  sleep 5
done
```

Esse loop é apenas uma visualização. As ações devem ser executadas em outra conexão.

## 10. Preparar os arquivos de carga

Os arquivos de apoio já existem em:

- [`produtos.csv`](../../aula3-revisao-modulo2/produtos.csv);
- [`produtos.ctl`](../../aula3-revisao-modulo2/produtos.ctl).

O CSV contém:

```csv
10,Headset,Audio,350.00
11,Webcam,Video,280.00
12,SSD 1TB,Armazenamento,620.00
13,Cadeira Gamer,Mobiliario,1400.00
```

O arquivo de controle informa ao `SQL*Loader` como interpretar o CSV:

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

Execute os comandos de cópia a partir da raiz do repositório:

```bash
podman exec -it oracle-free-full-23ai mkdir -p /opt/oracle/labdata
podman cp aula3-revisao-modulo2/produtos.csv oracle-free-full-23ai:/opt/oracle/labdata/produtos.csv
podman cp aula3-revisao-modulo2/produtos.ctl oracle-free-full-23ai:/opt/oracle/labdata/produtos.ctl
```

Confirme os arquivos:

```bash
podman exec oracle-free-full-23ai ls -lah /opt/oracle/labdata
```

## 11. SQL*Loader na prática

O `SQL*Loader` faz a carga definitiva de um arquivo externo em uma tabela Oracle.

### 11.1. Criar a tabela de destino

Conecte como `APP_OWNER` e execute antes do `sqlldr`:

```sql
CREATE TABLE produtos_carga (
  id_produto    NUMBER,
  nome_produto  VARCHAR2(100),
  categoria     VARCHAR2(50),
  preco         NUMBER(10,2)
);
```

A tabela precisa existir antes da execução do binário, porque o arquivo `.ctl` aponta para `APP_OWNER.PRODUTOS_CARGA`.

### 11.2. Executar o binário dentro do container

No terminal do host:

```bash
podman exec -it oracle-free-full-23ai bash
```

Dentro do container:

```bash
sqlldr app_owner/AppOwner123@//localhost:1521/FREEPDB1 \
  control=/opt/oracle/labdata/produtos.ctl \
  log=/opt/oracle/labdata/produtos_sqlldr.log
```

O `sqlldr` lê o CSV, usa o arquivo de controle, insere os registros e cria um log da operação.

Saia do container e leia o log:

```bash
exit
podman exec oracle-free-full-23ai cat /opt/oracle/labdata/produtos_sqlldr.log
```

### 11.3. Validar a carga

Conecte como `APP_OWNER`:

```sql
SELECT *
FROM produtos_carga
ORDER BY id_produto;
```

O resultado esperado é a presença dos quatro registros do CSV.

## 12. Tabela externa na prática

Uma tabela externa permite consultar um arquivo como se fosse uma tabela Oracle, sem carregá-lo definitivamente na primeira etapa.

### 12.1. Criar o `DIRECTORY`

Conecte como `SYSTEM`:

```sql
CREATE OR REPLACE DIRECTORY lab_dir AS '/opt/oracle/labdata';
GRANT READ, WRITE ON DIRECTORY lab_dir TO app_owner;
```

O caminho físico precisa existir dentro do container, e o objeto `DIRECTORY` precisa apontar para esse mesmo caminho.

### 12.2. Criar a tabela externa

Conecte como `APP_OWNER`:

```sql
CREATE TABLE ext_produtos (
  id_produto    NUMBER,
  nome_produto  VARCHAR2(100),
  categoria     VARCHAR2(50),
  preco         NUMBER(10,2)
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

### 12.3. Consultar e materializar os dados

Consulte o arquivo com SQL:

```sql
SELECT *
FROM ext_produtos
ORDER BY id_produto;
```

Depois da validação, materialize os registros em uma tabela interna:

```sql
CREATE TABLE produtos_ext_import AS
SELECT *
FROM ext_produtos;
```

```sql
SELECT *
FROM produtos_ext_import
ORDER BY id_produto;
```

A tabela externa é apropriada quando o arquivo precisa ser lido, filtrado ou validado antes da carga definitiva.

## 13. Data Pump na prática

`expdp` e `impdp` movimentam dados e metadados Oracle em um dump lógico. Eles não substituem RMAN e não são o mesmo mecanismo do `SQL*Loader`.

### 13.1. Preparar o diretório e o schema clone

Conecte como `SYSTEM`:

Confirme o schema clone:

```sql
SELECT username,
       account_status,
       default_tablespace
FROM dba_users
WHERE username = 'APP_CLONE';
```

Crie o diretório lógico que apontará para o diretório físico usado pelo container:

```sql
CREATE OR REPLACE DIRECTORY dpump_dir AS '/opt/oracle/labdata';
GRANT READ, WRITE ON DIRECTORY dpump_dir TO app_clone;
```

O usuário `SYSTEM`, que executará `expdp` e `impdp`, é o proprietário do diretório criado por ele e possui acesso ao objeto.

### 13.2. Exportar o schema

Entre no container:

```bash
podman exec -it oracle-free-full-23ai bash
```

Execute o `expdp`:

```bash
expdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_dir \
  DUMPFILE=app_owner_m2.dmp \
  LOGFILE=exp_app_owner_m2.log \
  SCHEMAS=APP_OWNER
```

O dump e o log serão criados no diretório físico associado ao objeto `DPUMP_DIR`:

```bash
ls -lah /opt/oracle/labdata
cat /opt/oracle/labdata/exp_app_owner_m2.log
```

No terminal do host, também é possível validar:

```bash
podman exec oracle-free-full-23ai ls -lah /opt/oracle/labdata
podman exec oracle-free-full-23ai cat /opt/oracle/labdata/exp_app_owner_m2.log
```

### 13.3. Importar com `REMAP_SCHEMA`

Ainda dentro do container, execute:

```bash
impdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_dir \
  DUMPFILE=app_owner_m2.dmp \
  LOGFILE=imp_app_clone_m2.log \
  REMAP_SCHEMA=APP_OWNER:APP_CLONE
```

O `REMAP_SCHEMA` faz com que os objetos exportados de `APP_OWNER` sejam recriados em `APP_CLONE`.

### 13.4. Validar o clone

Conecte como `APP_CLONE`:

```text
User: APP_CLONE
Password: Clone123
Service Name: FREEPDB1
```

Consulte as tabelas importadas:

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

Valide os dados:

```sql
SELECT COUNT(*)
FROM produtos;
```

Leia o log de importação:

```bash
podman exec oracle-free-full-23ai cat /opt/oracle/labdata/imp_app_clone_m2.log
```

## 14. Comparação final das ferramentas

| Necessidade | Ferramenta |
| :--- | :--- |
| Executar SQL e consultas | IDE ou `sqlplus` |
| Carregar CSV em tabela | `sqlldr` |
| Ler CSV antes de carregar | Tabela externa |
| Copiar schema Oracle | `expdp` e `impdp` |
| Registrar ações | Auditoria unificada |

## 15. Limpeza do laboratório

Execute como `SYSTEM`, depois de concluir as validações:

```sql
NOAUDIT POLICY pol_select_produtos_m2;
NOAUDIT POLICY pol_logon_m2;

DROP AUDIT POLICY pol_select_produtos_m2;
DROP AUDIT POLICY pol_logon_m2;

DROP DIRECTORY lab_dir;
DROP DIRECTORY dpump_dir;

DROP ROLE role_leitura_m2;
DROP ROLE role_carga_m2;
DROP ROLE role_analise_m2;

DROP USER app_owner CASCADE;
DROP USER analista CASCADE;
DROP USER operador_carga CASCADE;
DROP USER app_clone CASCADE;

DROP PROFILE prof_lab_m2;
```

Os arquivos físicos do laboratório podem ser removidos do container quando não forem mais necessários:

```bash
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/produtos.csv
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/produtos.ctl
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/produtos_sqlldr.log
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/app_owner_m2.dmp
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/exp_app_owner_m2.log
podman exec oracle-free-full-23ai rm -f /opt/oracle/labdata/imp_app_clone_m2.log
```

## 16. Resultado esperado

O laboratório estará consolidado quando for possível explicar e executar:

```text
criar identidade
  -> organizar permissões
      -> criar objeto
          -> testar acesso
              -> auditar ação
                  -> carregar arquivo
                      -> mover ou clonar dados
                          -> validar resultado
```

Referências complementares:

- [Material teórico completo do Módulo 2](../../modulo2-material/02-teoria-modulo2.md)
- [Prática original do Módulo 2](../../modulo2-material/02-pratica-modulo2.md)
- [Revisão anterior do Módulo 2](../../aula3-revisao-modulo2/README.md)
