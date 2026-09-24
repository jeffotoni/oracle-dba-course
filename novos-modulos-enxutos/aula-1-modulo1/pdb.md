# Extensão prática - Criação e administração de PDB no Oracle

Esta extensão complementa a [prática principal da Aula 1](./pratica.md). O conteúdo foi organizado a partir do manual de criação de PDB e mantém a sequência completa executada no ambiente Oracle com Podman.

## 1. Objetivo da prática

Nesta prática trabalhamos com uma instalação Oracle executada em container utilizando Podman.

O objetivo é entender, na prática:

- como identificar em qual container do Oracle estamos conectados;
- a diferença entre `CDB$ROOT` e uma PDB;
- como criar uma nova Pluggable Database;
- por que ocorre o erro `ORA-65016`;
- como utilizar `FILE_NAME_CONVERT`;
- como abrir uma nova PDB;
- a diferença entre `SYSTEM`, `SYS`, `SYSDBA` e `SYSOPER`;
- como alternar entre PDBs;
- como identificar o schema atual;
- como trabalhar com usuários locais dentro de uma PDB;
- como alterar a senha de um usuário.

Esta é uma extensão administrativa. O fluxo principal continua sendo conectar na `FREEPDB1`, criar um usuário de aplicação e trabalhar com tabelas.

## 2. Ambiente utilizado

O Oracle foi iniciado utilizando Podman:

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

Neste ambiente já existe a PDB:

```text
FREEPDB1
```

O diretório de persistência dos arquivos do Oracle é:

```text
/opt/oracle/oradata
```

Para iniciar a extensão usando `SYSTEM`:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

Para as operações que exigem privilégio administrativo elevado:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus / as sysdba
```

## 3. Tentativa inicial de criação da PDB

Inicialmente tentamos criar uma nova PDB utilizando:

```sql
CREATE PLUGGABLE DATABASE DBJEFFOTONI
ADMIN USER pdbadmin
IDENTIFIED BY Senha123;
```

O Oracle retornou:

```text
ORA-65016: FILE_NAME_CONVERT must be specified
```

Isso ocorre porque o Oracle precisa saber onde criar os arquivos físicos da nova PDB. Antes de resolver o problema, é necessário verificar onde a sessão está conectada e localizar os arquivos da `PDB$SEED`.

## 4. Identificar a PDB atual

Execute:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container
FROM dual;
```

O resultado esperado é:

```text
FREEPDB1
```

Isso mostra que a sessão está conectada diretamente na PDB `FREEPDB1`.

## 5. Alterar a sessão para o `CDB$ROOT`

Para administrar as PDBs, altere a sessão para o container principal:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

Confirme:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container
FROM dual;
```

O resultado esperado é:

```text
CDB$ROOT
```

`ALTER SESSION SET CONTAINER` altera somente a sessão atual. Ele não renomeia, move ou cria uma PDB.

## 6. Identificar os arquivos das PDBs

Execute:

```sql
SELECT p.con_id,
       p.name AS pdb_name,
       d.name AS datafile
FROM v$pdbs p
JOIN v$datafile d
  ON p.con_id = d.con_id
ORDER BY p.con_id, d.name;
```

O resultado mostra arquivos da `PDB$SEED` e da `FREEPDB1`, por exemplo:

```text
2  PDB$SEED   /opt/oracle/oradata/FREE/pdbseed/sysaux01.dbf
2  PDB$SEED   /opt/oracle/oradata/FREE/pdbseed/system01.dbf
2  PDB$SEED   /opt/oracle/oradata/FREE/pdbseed/undotbs01.dbf

3  FREEPDB1   /opt/oracle/oradata/FREE/FREEPDB1/sysaux01.dbf
3  FREEPDB1   /opt/oracle/oradata/FREE/FREEPDB1/system01.dbf
3  FREEPDB1   /opt/oracle/oradata/FREE/FREEPDB1/ts_rman_lab01.dbf
3  FREEPDB1   /opt/oracle/oradata/FREE/FREEPDB1/undotbs01.dbf
3  FREEPDB1   /opt/oracle/oradata/FREE/FREEPDB1/users01.dbf
```

Aqui identificamos o diretório da `PDB$SEED`:

```text
/opt/oracle/oradata/FREE/pdbseed/
```

A `PDB$SEED` funciona como base somente leitura para a criação de novas PDBs.

## 7. Criar a nova PDB

Com o caminho correto identificado, execute no `CDB$ROOT`:

```sql
CREATE PLUGGABLE DATABASE DBJEFFOTONI
ADMIN USER pdbadmin
IDENTIFIED BY Senha123
FILE_NAME_CONVERT = (
    '/opt/oracle/oradata/FREE/pdbseed/',
    '/opt/oracle/oradata/FREE/DBJEFFOTONI/'
);
```

O `FILE_NAME_CONVERT` informa ao Oracle:

```text
Origem:  /opt/oracle/oradata/FREE/pdbseed/
Destino: /opt/oracle/oradata/FREE/DBJEFFOTONI/
```

O Oracle copia a estrutura-base da `PDB$SEED` para o diretório da nova PDB. `pdbadmin` é um usuário administrativo local da nova PDB.

## 8. Tentativa de abrir a PDB utilizando `SYSTEM`

Após criar a PDB, ainda utilizando `SYSTEM`, execute:

```sql
ALTER PLUGGABLE DATABASE DBJEFFOTONI OPEN;
```

No cenário praticado, recebemos:

```text
ORA-01031: insufficient privileges
```

O usuário `SYSTEM` executa várias tarefas administrativas, mas não possui automaticamente os mesmos privilégios de `SYS AS SYSDBA`.

## 9. Conectar como `SYSDBA`

Abra uma sessão privilegiada:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus / as sysdba
```

Altere a sessão para o `CDB$ROOT`:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

Agora abra a nova PDB:

```sql
ALTER PLUGGABLE DATABASE DBJEFFOTONI OPEN;
```

A conexão `SYS AS SYSDBA` permitiu executar a operação administrativa. `SYSOPER` também é um modo administrativo do Oracle, mas não será usado como caminho principal desta prática.

## 10. Verificar o estado das PDBs

Execute:

```sql
SELECT name, open_mode
FROM v$pdbs;
```

O resultado esperado é semelhante a:

```text
PDB$SEED        READ ONLY
FREEPDB1        READ WRITE
DBJEFFOTONI     READ WRITE
```

Isso confirma que `DBJEFFOTONI` está aberta e disponível para leitura e escrita. `PDB$SEED` permanece `READ ONLY` porque é um modelo.

## 11. Voltar para a `FREEPDB1`

Como a sessão está no `CDB$ROOT`, retorne à PDB principal:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

Confirme:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container
FROM dual;
```

O resultado esperado é:

```text
FREEPDB1
```

## 12. Entender onde os objetos são criados

A sessão está sempre conectada em algum container:

```text
CDB$ROOT
FREEPDB1
DBJEFFOTONI
```

Ao criar objetos como `TABLE`, `VIEW`, `TRIGGER`, `SEQUENCE`, `PROCEDURE` ou `FUNCTION`, eles pertencem à PDB onde a sessão está conectada.

Se estivermos em `FREEPDB1`, os objetos pertencem à `FREEPDB1`. Se estivermos em `DBJEFFOTONI`, pertencem à nova PDB.

## 13. Entender o schema

No Oracle, o schema normalmente possui o mesmo nome do usuário proprietário dos objetos.

Por exemplo, conectado como `SYSTEM` na `FREEPDB1`:

```sql
CREATE TABLE TESTE (
    ID NUMBER
);
```

A tabela será identificada como:

```text
PDB:     FREEPDB1
Schema:  SYSTEM
Tabela:  TESTE
Objeto:  SYSTEM.TESTE
```

Esse exemplo serve para demonstrar a regra. Para tabelas de aplicação, use o usuário dedicado `APP_AULA1`, e não `SYSTEM` ou `SYS`.

## 14. Identificar o schema e o usuário atuais

Para descobrir o schema da sessão:

```sql
SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
```

Para descobrir o usuário conectado:

```sql
SELECT USER AS current_user
FROM dual;
```

Essas duas informações ajudam a explicar onde os objetos serão criados e quais privilégios estarão disponíveis.

## 15. Usuários locais da PDB

Usuários criados dentro de uma PDB pertencem àquela PDB. Conceitualmente:

```text
FREEPDB1
└── usuários/schemas
    ├── SYSTEM
    └── <SEU_USUARIO>
```

Na PDB criada durante a prática:

```text
DBJEFFOTONI
└── PDBADMIN
```

O usuário local pode se conectar usando o `Service Name` da PDB à qual pertence.

## 16. Alterar a senha de um usuário

Estando na PDB correta e utilizando uma conta administrativa com privilégio suficiente:

```sql
ALTER USER <SEU_USUARIO>
IDENTIFIED BY NovaSenha123;
```

Exemplo com o nome utilizado no manual original:

```sql
ALTER USER jeffotoni
IDENTIFIED BY NovaSenha123;
```

Depois da alteração, o usuário deverá utilizar a nova senha ao se conectar ao `Service Name` da PDB.

## 17. Tipos de conexão utilizados

### `SYSTEM`

`SYSTEM` é um usuário administrativo do Oracle. Ele pode ser usado dentro da PDB para diversas tarefas administrativas, como consultar o ambiente e criar usuários de laboratório.

### `SYS`

`SYS` possui o nível administrativo mais alto do Oracle e é usado com modos privilegiados, como `SYSDBA`.

### `SYSDBA`

`SYS AS SYSDBA` permitiu abrir a PDB criada:

```sql
ALTER PLUGGABLE DATABASE DBJEFFOTONI OPEN;
```

### `SYSOPER`

`SYSOPER` é outro modo de conexão administrativa. Nesta prática ele é apresentado como conceito, mas não faz parte do caminho principal de execução.

Ao conectar no Oracle, observe sempre o usuário e o privilégio administrativo aplicado à conexão.

## 18. Estrutura observada na prática

Após a prática, o ambiente ficou conceitualmente assim:

```text
Oracle
│
├── CDB$ROOT
│
├── PDB$SEED
│
├── FREEPDB1
│   └── usuários/schemas
│       ├── SYSTEM
│       └── <SEU_USUARIO>
│
└── DBJEFFOTONI
    └── PDBADMIN
```

A `PDB$SEED` é usada como base para novas PDBs. A `FREEPDB1` já existia no ambiente. A `DBJEFFOTONI` foi criada durante a prática.

## 19. Comandos principais utilizados

Identificar o container atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container
FROM dual;
```

Ir para o container raiz:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

Ir para a `FREEPDB1`:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

Listar PDBs e seus datafiles:

```sql
SELECT p.con_id,
       p.name AS pdb_name,
       d.name AS datafile
FROM v$pdbs p
JOIN v$datafile d
  ON p.con_id = d.con_id
ORDER BY p.con_id, d.name;
```

Criar a nova PDB:

```sql
CREATE PLUGGABLE DATABASE DBJEFFOTONI
ADMIN USER pdbadmin
IDENTIFIED BY Senha123
FILE_NAME_CONVERT = (
    '/opt/oracle/oradata/FREE/pdbseed/',
    '/opt/oracle/oradata/FREE/DBJEFFOTONI/'
);
```

Abrir a nova PDB:

```sql
ALTER PLUGGABLE DATABASE DBJEFFOTONI OPEN;
```

Listar o estado das PDBs:

```sql
SELECT name, open_mode
FROM v$pdbs;
```

Verificar o schema atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA')
FROM dual;
```

Verificar o usuário conectado:

```sql
SELECT USER
FROM dual;
```

Alterar a senha de um usuário:

```sql
ALTER USER <SEU_USUARIO>
IDENTIFIED BY NovaSenha123;
```

## 20. Conclusão

Nesta prática foi criada a Pluggable Database:

```text
DBJEFFOTONI
```

O Oracle trabalha com a estrutura:

```text
CDB
↓
PDB
↓
USUÁRIO / SCHEMA
↓
OBJETOS
```

O ponto principal é confirmar, antes de executar comandos administrativos ou criar objetos:

```text
Em qual PDB estou?
Com qual usuário e schema estou conectado?
```

Essas informações determinam onde os objetos serão criados e quais operações poderão ser executadas.
