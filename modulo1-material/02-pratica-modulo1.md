# Módulo 1 - Prática
## Arquitetura, Ferramentas Administrativas e Configuração do Ambiente

Este material reúne comandos e procedimentos práticos do Módulo 1, com foco em arquitetura Oracle, modelo multitenant, visões administrativas e parâmetros.

---

## 1. Software necessário para Windows

### Obrigatório

- Podman
- CloudBeaver
- Git

### Recomendado

- SQL Developer
- Visual Studio Code
- Windows Terminal

---

## 2. Ambiente Podman do laboratório

### 2.1. Comando rápido com `podman run`

```bash
podman run -d \
  --name oracle-free \
  -p 1521:1521 \
  -e ORACLE_PASSWORD=Senha123 \
  gvenzl/oracle-free
```

### 2.2. Verificar se o container foi criado

```bash
podman ps -a
```

### 2.3. Acompanhar inicialização do banco

```bash
podman logs -f oracle-free
```

Aguardar até aparecer mensagem de banco pronto para conexão.

### 2.4. Entrar no container

```bash
podman exec -it oracle-free bash
```

---

## 3. Opção com `podman compose`

Criar arquivo `compose.yaml`:

```yaml
services:
  oracle:
    image: gvenzl/oracle-free
    container_name: oracle-free
    ports:
      - "1521:1521"
    environment:
      ORACLE_PASSWORD: Senha123
    volumes:
      - oracle_data:/opt/oracle/oradata

volumes:
  oracle_data:
```

### Subir o ambiente

```bash
podman compose up -d
```

### Ver logs

```bash
podman compose logs -f
```

### Derrubar ambiente

```bash
podman compose down
```

---

## 4. Credenciais e conexão

### Conexão no CloudBeaver

Preencher:

- **Host:** `localhost`
- **Porta:** `1521`
- **Service Name:** `FREEPDB1`
- **Usuário:** `system`
- **Senha:** `Senha123`

### Observação importante

No modelo multitenant, priorizar conexão via **service name** da PDB, e não por SID.

---

## 5. Conexão administrativa no CloudBeaver

### Conectar como SYSDBA

No CloudBeaver, usar `SYS` com papel `SYSDBA` quando a prática exigir escopo administrativo.

### Identificação inicial do ambiente

```sql
SELECT instance_name, status FROM v$instance;
SELECT name, open_mode FROM v$database;
SELECT con_id, name, open_mode FROM v$pdbs ORDER BY con_id;
```

### Ver container atual da sessão

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### Alternar para a PDB de laboratório

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

---

## 6. Comandos básicos de operação

### 6.1. Versão do banco

```sql
SELECT banner FROM v$version;
```

### 6.2. Instância

```sql
SELECT instance_name, host_name, version, startup_time, status
FROM v$instance;
```

### 6.3. Banco

```sql
SELECT name, db_unique_name, open_mode, database_role, log_mode
FROM v$database;
```

### 6.4. PDBs

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

### 6.5. Checklist mínimo de ambiente

```sql
SELECT instance_name,
       status,
       version
FROM v$instance;

SELECT name,
       open_mode,
       database_role,
       log_mode
FROM v$database;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### 6.6. Diagnóstico rápido de arquitetura

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name IN ('open_cursors', 'processes', 'sessions', 'sga_target', 'pga_aggregate_target')
ORDER BY name;

SELECT sid,
       serial#,
       username,
       status,
       program
FROM v$session
WHERE username IS NOT NULL
ORDER BY sid;
```

### 6.7. Validação final do módulo

```sql
SELECT tablespace_name,
       contents,
       status
FROM dba_tablespaces
ORDER BY tablespace_name;

SELECT file_id,
       tablespace_name,
       bytes / 1024 / 1024 AS size_mb
FROM dba_data_files
ORDER BY file_id;
```

---

## 7. Dicionário de dados e visões de sistema

No Oracle, administração e leitura de metadados devem usar **Data Dictionary Views** e **Dynamic Performance Views**.

### 7.1. USER_*

Objetos do usuário conectado.

```sql
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT object_name, object_type FROM user_objects ORDER BY object_type, object_name;
SELECT table_name, column_name, data_type FROM user_tab_columns ORDER BY table_name, column_id;
```

### 7.2. ALL_*

Objetos acessíveis ao usuário.

```sql
SELECT owner, table_name FROM all_tables ORDER BY owner, table_name;
SELECT owner, object_name, object_type FROM all_objects ORDER BY owner, object_type, object_name;
```

### 7.3. DBA_*

Visão administrativa ampla do banco.

```sql
SELECT username, account_status, created FROM dba_users ORDER BY username;
SELECT tablespace_name, status, contents FROM dba_tablespaces ORDER BY tablespace_name;
SELECT file_name, tablespace_name, bytes/1024/1024 AS mb FROM dba_data_files ORDER BY file_name;
SELECT grantee, granted_role FROM dba_role_privs ORDER BY grantee, granted_role;
SELECT grantee, privilege FROM dba_sys_privs ORDER BY grantee, privilege;
SELECT grantee, owner, table_name, privilege FROM dba_tab_privs ORDER BY grantee, owner, table_name;
```

### 7.4. V$*

Visões dinâmicas do estado operacional.

```sql
SELECT name, value FROM v$parameter ORDER BY name;
SELECT * FROM v$sga;
SELECT sid, serial#, username, status FROM v$session ORDER BY sid;
```

---

## 8. Consultas principais para aula

### 8.1. Arquitetura e multitenant

```sql
SELECT instance_name,
       status
FROM v$instance;

SELECT name,
       open_mode,
       database_role
FROM v$database;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### 8.2. Memória (SGA e PGA)

#### Visão da SGA

```sql
SELECT * FROM v$sga;
```

#### Componentes da SGA

```sql
SELECT component, current_size/1024/1024 AS mb
FROM v$sga_dynamic_components
ORDER BY component;
```

#### Parâmetros de memória

```sql
SELECT name, value
FROM v$parameter
WHERE name IN ('memory_target', 'sga_target', 'pga_aggregate_target')
ORDER BY name;
```

#### Exemplo orientado de PGA (ordenação)

```sql
CREATE TABLE mod1_sort_test AS
SELECT level AS id, LPAD(level, 8, '0') AS codigo
FROM dual
CONNECT BY level <= 10000;

SELECT *
FROM mod1_sort_test
ORDER BY codigo DESC;
```

Interpretar em aula: a ordenação pode usar área de PGA do processo servidor da sessão.

### 8.3. Processos

#### Background ativos

```sql
SELECT name, description
FROM v$bgprocess
WHERE paddr <> '00'
ORDER BY name;
```

#### Processos da instância

```sql
SELECT spid, program
FROM v$process
ORDER BY spid;
```

### 8.4. Sessões

```sql
SELECT sid, serial#, username, status, machine, program
FROM v$session
ORDER BY sid;

SELECT sid, serial#, username, osuser, machine, program, status
FROM v$session
WHERE username IS NOT NULL
ORDER BY username;
```

### 8.5. Arquivos físicos

```sql
SELECT name FROM v$datafile ORDER BY name;
SELECT member FROM v$logfile ORDER BY member;
SELECT name FROM v$controlfile ORDER BY name;
```

### 8.6. Tablespaces

```sql
SELECT tablespace_name, status, contents
FROM dba_tablespaces
ORDER BY tablespace_name;
```

### 8.7. Objetos e metadados

```sql
SELECT object_name, object_type, status
FROM user_objects
ORDER BY object_type, object_name;

SELECT owner, table_name, column_name, data_type
FROM all_tab_columns
ORDER BY owner, table_name, column_id;
```

---

## 9. Privilégios e roles para demonstrar

### 9.1. Criar usuário de laboratório na PDB

Executar como SYS/SYSTEM com container na PDB:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;

CREATE USER lab_user IDENTIFIED BY Senha123;
GRANT CREATE SESSION TO lab_user;
GRANT CREATE TABLE TO lab_user;
GRANT SELECT_CATALOG_ROLE TO lab_user;
```

### 9.2. Consultar privilégios do usuário

```sql
SELECT * FROM dba_sys_privs WHERE grantee = 'LAB_USER' ORDER BY privilege;
SELECT * FROM dba_role_privs WHERE grantee = 'LAB_USER' ORDER BY granted_role;
```

### 9.3. Validar comportamento de acesso

Conectar como `lab_user` e executar:

```sql
CREATE TABLE t_lab (id NUMBER, nome VARCHAR2(50));
INSERT INTO t_lab VALUES (1, 'teste');
COMMIT;
SELECT * FROM t_lab;
SELECT table_name FROM user_tables ORDER BY table_name;
```

Interpretar em aula:

- `CREATE SESSION`: permite conexão;
- `CREATE TABLE`: permite criar objetos no schema próprio;
- `SELECT_CATALOG_ROLE`: amplia acesso a visões de catálogo.

---

## 10. Parametrização e configuração inicial

### 10.1. Ver SPFILE em uso

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'spfile';
```

### 10.2. Consultar parâmetro específico

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'open_cursors';
```

ou

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'open_cursors';
```

### 10.3. Alterar parâmetro dinâmico

```sql
ALTER SYSTEM SET open_cursors = 500 SCOPE=BOTH;
```

### 10.4. Confirmar alteração

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'open_cursors';
```

### 10.5. Consultar parâmetros de concorrência

```sql
SELECT name, value
FROM v$parameter
WHERE name IN ('processes', 'sessions', 'open_cursors')
ORDER BY name;
```

### 10.6. Exemplo didático de PFILE (gerar a partir do SPFILE)

```sql
CREATE PFILE='/tmp/init_mod1.ora' FROM SPFILE;
```

Interpretar em aula: o PFILE gerado é texto e pode ser inspecionado fora do banco.

---

## 11. Roteiro prático sugerido para aula

### Etapa 1

Subir o banco e aguardar inicialização.

### Etapa 2

Conectar no CloudBeaver em `FREEPDB1`.

### Etapa 3

Validar instância, banco e PDBs (`v$instance`, `v$database`, `v$pdbs`).

### Etapa 4

Explorar memória, processos, sessões e arquivos.

### Etapa 5

Criar `lab_user`, validar privilégios e criar tabela de teste.

### Etapa 6

Consultar e alterar `open_cursors`, validando persistência via SPFILE.

---

## 12. Problemas comuns

### 12.1. Container não sobe

```bash
podman ps -a
podman logs oracle-free
```

### 12.2. Porta 1521 em uso

```bash
podman run -d --name oracle-free -p 1522:1521 -e ORACLE_PASSWORD=Senha123 gvenzl/oracle-free
```

Nesse caso, usar porta `1522` no cliente.

### 12.3. Cliente não conecta

Conferir:

- container em execução;
- inicialização concluída;
- service name `FREEPDB1`;
- usuário e senha corretos.

### 12.4. Erro ao criar usuário comum no CDB (`ORA-65096`)

Causa comum: tentativa de criar usuário local enquanto a sessão está no container raiz.

Ação:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
ALTER SESSION SET CONTAINER = FREEPDB1;
```

### 12.5. Sem acesso a visões administrativas

Validar privilégios/roles do usuário (`SELECT_CATALOG_ROLE`, por exemplo).

---

## 13. Resumo operacional do módulo

Neste módulo, devemos conseguir:

- subir ou acessar Oracle em container;
- conectar na PDB de laboratório (`FREEPDB1`);
- validar arquitetura (instância, banco, PDBs);
- consultar memória, processos, sessões e arquivos;
- usar dicionário de dados e visões `V$`;
- validar privilégio básico com usuário de laboratório;
- aplicar ajuste simples de parâmetro e confirmar efeito.
