# Revisão do Módulo 2 - aula 3

> Revisão do módulo 2: segurança, controle de acesso, auditoria e carga de dados em volume no Oracle.

## Ideia central do módulo

O módulo 2 junta dois temas que andam juntos no ambiente real:

1. controlar quem entra e o que pode fazer;
2. controlar como grandes volumes de dados entram, saem ou são movimentados.

Em outras palavras:

```txt
Segurança = identidade + permissão + rastreabilidade
Carga em volume = entrada e movimentação controlada de dados
```

## O que precisa ficar claro

- autenticação não é a mesma coisa que autorização;
- usuário não é apenas login, também se relaciona com schema e posse de objetos;
- privilégios amplos demais aumentam risco;
- roles ajudam a organizar permissões;
- perfis ajudam a padronizar política;
- auditoria ajuda a provar o que aconteceu;
- SQL*Loader, tabela externa e Data Pump não são a mesma coisa.

## 1. Segurança no Oracle

Segurança em Oracle não deve ser reduzida a senha. Ela envolve:

- identidade;
- acesso;
- permissão;
- segregação de funções;
- rastreabilidade;
- governança.

### Regra prática

```txt
Não basta saber quem entrou.
É preciso saber o que pode fazer e o que ficou registrado.
```

## 2. Autenticação x autorização

### Autenticação

Responde à pergunta:

```txt
Quem está tentando acessar?
```

### Autorização

Responde à pergunta:

```txt
O que essa identidade pode fazer?
```

### Diferença curta

```txt
Autenticação = validar identidade
Autorização = definir permissões
```

## 3. Usuário e schema

No Oracle, quando um usuário é criado, normalmente existe um schema associado ao mesmo nome.

Isso é importante porque o usuário não representa apenas acesso. Ele também se relaciona com:

- dono de objetos;
- organização lógica;
- separação entre aplicação, leitura, carga e administração.

### Regra prática

```txt
Usuário = identidade
Schema = espaço lógico dos objetos
```

## 4. Perfis

Perfis existem para aplicar regras de forma padronizada.

Eles podem controlar:

- tentativas de login;
- bloqueio;
- expiração de senha;
- reutilização;
- limite de sessão;
- tempo ocioso.

### Ideia central

Perfil ajuda a tirar o ambiente do improviso e levar para um padrão administrativo.

## 5. Privilégios e roles

### Privilégios de sistema

Controlam ações amplas no ambiente, como:

- criar sessão;
- criar tabela;
- criar usuário;
- criar procedure.

### Privilégios de objeto

Controlam ações sobre objetos específicos, como:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `EXECUTE`

Acima temos DML (Data Manipulation Language) , DQL (Data Query Language e DCL / TCL / Procedural.
Só não temos acima DDL (Data Definition Language).

### Roles

Roles agrupam privilégios. Isso simplifica:

- concessão;
- revisão;
- revogação;
- padronização.

### Regra prática

```txt
Privilégio de sistema = poder amplo
Privilégio de objeto = poder específico
Role = pacote organizado de permissões
```

## 6. Menor privilégio e segregação

O módulo 2 faz mais sentido quando fecha nesta lógica:

- conta de aplicação;
- conta de leitura;
- conta de carga;
- conta administrativa.

### Regra prática

```txt
Menos privilégio direto
Mais role coerente
Mais rastreabilidade
```

## 7. Auditoria e rastreabilidade

Auditoria registra ações relevantes no banco.

Rastreabilidade permite responder:

- quem fez;
- quando fez;
- em qual objeto;
- com qual resultado.

### O que auditar costuma fazer sentido

- logon;
- acesso a objetos sensíveis;
- operações administrativas;
- concessão de privilégios;
- alterações importantes.

### Regra prática

```txt
Segurança sem rastreabilidade é incompleta
```

## 8. Carga de dados em volume

Carga em volume é a entrada, leitura, importação ou movimentação de grande quantidade de dados de forma planejada.

Ela aparece em cenários como:

- migração;
- carga inicial;
- integração entre sistemas;
- recebimento de arquivo externo;
- refresh de ambiente;
- cópia de schema;
- importação lógica.

## 9. Ferramentas de carga e movimentação

## 9.1. SQL*Loader

Ferramenta clássica do Oracle para carregar arquivo externo estruturado em tabela Oracle.

### Quando pensar em SQL*Loader

- CSV ou TXT bem definido;
- carga repetitiva;
- arquivo com layout conhecido;
- rotina operacional.

## 9.2. Tabela externa

Permite ler arquivo como tabela sem carregar de imediato para tabela interna.

### Quando pensar em tabela externa

- validar arquivo antes da carga;
- consultar com SQL;
- inspecionar conteúdo;
- usar como etapa intermediária em ETL.

## 9.3. Data Pump

Ferramenta de exportação e importação lógica do ecossistema Oracle.

### Quando pensar em Data Pump

- exportar schema;
- importar schema;
- copiar objetos e dados;
- migrar ambiente Oracle para Oracle;
- fazer dump lógico.

## 9.4. Regra prática de escolha

```txt
Arquivo estruturado para tabela = SQL*Loader
Ler arquivo com SQL = tabela externa
Mover objetos e dados Oracle = Data Pump
```

## 9.5. Ponto operacional importante

No módulo 2, parte da prática deixa de ser apenas SQL em cliente gráfico.

Isso acontece porque algumas atividades dependem de **binários nativos do próprio Oracle**, como:

- `sqlldr`
- `expdp`
- `impdp`
- `sqlplus`

### O que é cada binário

- `sqlldr`
  - carrega arquivos externos estruturados, como CSV ou TXT, para tabelas Oracle.
- `expdp`
  - exporta dados e metadados Oracle em formato de dump lógico.
- `impdp`
  - importa dumps lógicos gerados pelo `expdp`.
- `sqlplus`
  - cliente nativo de linha de comando do Oracle para executar SQL e validações operacionais.

Esses binários normalmente são executados **dentro do container Oracle**, porque:

- já fazem parte do ambiente Oracle;
- dependem da instalação interna do banco;
- trabalham melhor no mesmo filesystem onde estão os arquivos de carga e dump;
- reduzem atrito com configuração no host.

### Regra prática

```txt
SQL administrativo e consultas = Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente
Binários nativos do Oracle = terminal dentro do container
```

## 9.6. Entrar no container Oracle

Quando a prática exigir ferramentas nativas, o fluxo normal é entrar no container:

```bash
podman exec -it oracle-free-full-23ai bash
```

### O que isso faz

- abre um shell dentro do container Oracle;
- permite usar utilitários do próprio banco;
- dá acesso aos diretórios internos usados no laboratório.

### Validação rápida

```bash
command -v sqlplus
command -v sqlldr
command -v expdp
command -v impdp
```

```bash
type sqlplus
type sqlldr
type expdp
type impdp
```

Se esses comandos responderem com caminho válido, o ambiente está pronto para a prática operacional.

### Validação curta dos binários

```bash
sqlplus -v
sqlldr -help | head
expdp help=y | head
impdp help=y | head
```

## 10. Segurança e carga andam juntas

Carga de dados não é assunto separado de segurança.

Toda carga relevante deveria levantar perguntas como:

- quem pode executar;
- em qual schema entra;
- quais privilégios a rotina precisa;
- como registrar a operação;
- como validar origem e erro;
- como reduzir impacto operacional.

## 11. Queries essenciais de revisão

### Validação inicial do laboratório

```sql
SELECT USER AS current_user
FROM dual;

SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

### Leitura prática

```txt
Antes de falar de segurança ou carga, vale validar:
- quem está conectado;
- em qual schema a sessão está;
- em qual container a sessão está;
- se a PDB está aberta.
```

### Ver usuários

```sql
SELECT username,
       account_status,
       profile
FROM dba_users
ORDER BY username;
```

### Ver roles

```sql
SELECT role
FROM dba_roles
ORDER BY role;
```

### Ver privilégios de sistema

```sql
SELECT grantee,
       privilege
FROM dba_sys_privs
ORDER BY grantee, privilege;
```

### Ver privilégios de objeto

```sql
SELECT grantee,
       owner,
       table_name,
       privilege
FROM dba_tab_privs
ORDER BY grantee, owner, table_name, privilege;
```

### Ver roles concedidas

```sql
SELECT grantee,
       granted_role
FROM dba_role_privs
ORDER BY grantee, granted_role;
```

### Ver trilha de auditoria

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

### Ver diretórios lógicos

```sql
SELECT directory_name,
       directory_path
FROM dba_directories
ORDER BY directory_name;
```

### Ver schema atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
```

### Ver container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 12. Laboratório prático aplicado

Para a revisão ficar próxima da prática real do módulo, vale manter um laboratório aplicável com os mesmos nomes usados na aula:

- `APP_OWNER`
- `ANALISTA`
- `OPERADOR_CARGA`
- `APP_CLONE`

### Subir o Oracle com Podman

No repositório, já existem versões prontas em:

- `repo/oracle/versoes/free-full-23ai/script/up.sh`

### Versão adotada - `free-full-23ai`

Usando o script do repositório:

```bash
cd repo/oracle/versoes/free-full-23ai/script
./up.sh
```

Comando explícito equivalente:

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

### Validar a subida

```bash
podman ps
podman logs -f oracle-free-full-23ai
```

### Perfil

```sql
CREATE PROFILE prof_lab_m2 LIMIT
  SESSIONS_PER_USER 3
  FAILED_LOGIN_ATTEMPTS 5
  PASSWORD_LIFE_TIME 90
  IDLE_TIME 30;
```

### Usuários

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

### Roles e grants

```sql
CREATE ROLE role_leitura_m2;
CREATE ROLE role_carga_m2;

GRANT CREATE SESSION TO role_leitura_m2;
GRANT CREATE SESSION TO role_carga_m2;

GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_owner;
GRANT CREATE SESSION TO analista;
GRANT CREATE SESSION TO operador_carga;
GRANT CREATE SESSION TO app_clone;

GRANT role_leitura_m2 TO analista;
GRANT role_carga_m2 TO operador_carga;
```

### Tabela base do laboratório

Conectar como `APP_OWNER`:

```sql
CREATE TABLE produtos (
  id_produto    NUMBER PRIMARY KEY,
  nome_produto  VARCHAR2(100),
  categoria     VARCHAR2(50),
  preco         NUMBER(10,2),
  data_cadastro DATE DEFAULT SYSDATE
);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (1, 'Notebook', 'Informatica', 4500.00);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (2, 'Mouse', 'Perifericos', 120.00);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco)
VALUES (3, 'Teclado', 'Perifericos', 250.00);

COMMIT;
```

### Grants sobre a tabela

Conectar como usuário administrativo:

```sql
GRANT SELECT ON app_owner.produtos TO role_leitura_m2;
GRANT SELECT, INSERT ON app_owner.produtos TO role_carga_m2;
```

### Teste por usuário

Conectar como `ANALISTA`:

```sql
SELECT *
FROM app_owner.produtos
ORDER BY id_produto;
```

Conectar como `OPERADOR_CARGA`:

```sql
INSERT INTO app_owner.produtos (id_produto, nome_produto, categoria, preco)
VALUES (4, 'Monitor', 'Perifericos', 980.00);

COMMIT;
```

## 13. Comandos e exemplos que valem aparecer na revisão

## 13.1. Fluxo prático do módulo

```txt
1. Entrar com usuário administrativo
2. Criar perfil, usuários e roles
3. Criar tabela de aplicação
4. Conceder privilégios corretos
5. Validar acesso com usuários diferentes
6. Auditar ações relevantes
7. Usar binários nativos do Oracle para carga e dump
```

### Criar política de auditoria

```sql
CREATE AUDIT POLICY pol_logon_m2 ACTIONS LOGON;
AUDIT POLICY pol_logon_m2;

CREATE AUDIT POLICY pol_select_produtos_m2
  ACTIONS SELECT ON app_owner.produtos;

AUDIT POLICY pol_select_produtos_m2;
```

### Gerar evidência

Conectar como `ANALISTA`:

```sql
SELECT *
FROM app_owner.produtos;
```

### Ler trilha de auditoria

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

### Entrar no container

```bash
podman exec -it oracle-free-full-23ai bash
```

### Conectar com SQL*Plus dentro do container - somente se necessário

```bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

### O que isso resolve

- valida conexão pelo cliente nativo Oracle;
- ajuda a confirmar usuário, serviço e acessibilidade;
- prepara o ambiente para `sqlldr`, `expdp` e `impdp`.

> Regra prática: para consulta e administração diária, usar Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente. `sqlplus` entra aqui só quando fizer sentido validar o cliente nativo Oracle dentro do container.

### Validação real dos binários no container

```bash
command -v sqlplus
command -v sqlldr
command -v expdp
command -v impdp
```

```bash
type sqlplus
type sqlldr
type expdp
type impdp
```

```bash
sqlplus -v
sqlldr -help | head
expdp help=y | head
impdp help=y | head
```

## 13.2. Exemplo de arquivo CSV para SQL*Loader e tabela externa

Arquivo no host:

- `./produtos.csv`

Arquivo no container:

- `/opt/oracle/labdata/produtos.csv`

```csv
10,Headset,Audio,350.00
11,Webcam,Video,280.00
12,SSD 1TB,Armazenamento,620.00
13,Cadeira Gamer,Mobiliario,1400.00
```

## 13.3. Exemplo de arquivo de controle para SQL*Loader

Arquivo no host:

- `./produtos.ctl`

Arquivo no container:

- `/opt/oracle/labdata/produtos.ctl`

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

## 13.4. SQL*Loader na prática

### Criar tabela de destino

Conectar como `APP_OWNER`:

```sql
CREATE TABLE produtos_carga (
  id_produto    NUMBER,
  nome_produto  VARCHAR2(100),
  categoria     VARCHAR2(50),
  preco         NUMBER(10,2)
);
```

### SQL*Loader

Copiar arquivos do host para o container:

```bash
podman cp ./produtos.csv oracle-free-full-23ai:/opt/oracle/labdata/produtos.csv
podman cp ./produtos.ctl oracle-free-full-23ai:/opt/oracle/labdata/produtos.ctl
```

```bash
sqlldr app_owner/AppOwner123@//localhost:1521/FREEPDB1 \
  control=/opt/oracle/labdata/produtos.ctl \
  log=/opt/oracle/labdata/produtos_sqlldr.log
```

### O que o SQL*Loader faz

- lê arquivo externo;
- interpreta o arquivo de controle `.ctl`;
- carrega dados em tabela Oracle;
- gera log técnico da operação.

### Validação da carga

```sql
SELECT *
FROM produtos_carga
ORDER BY id_produto;
```

### Ver log gerado

```bash
cat /opt/oracle/labdata/produtos_sqlldr.log
```

## 13.5. Tabela externa na prática

```sql
CREATE OR REPLACE DIRECTORY lab_dir AS '/opt/oracle/labdata';
```

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
  LOCATION ('produtos.csv')
)
REJECT LIMIT UNLIMITED;
```

### O que a tabela externa faz

- não carrega imediatamente para tabela interna;
- permite validar arquivo com SQL;
- ajuda a separar leitura, validação e carga definitiva.

### Validação da leitura externa

```sql
SELECT *
FROM ext_produtos
ORDER BY id_produto;
```

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

## 13.6. Data Pump na prática

### Criar diretório lógico

```sql
CREATE OR REPLACE DIRECTORY dpump_dir AS '/opt/oracle/labdata';
GRANT READ, WRITE ON DIRECTORY dpump_dir TO system;
GRANT READ, WRITE ON DIRECTORY dpump_dir TO app_owner;
GRANT READ, WRITE ON DIRECTORY dpump_dir TO app_clone;
```

### Exportar schema com `expdp`

```bash
expdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_dir \
  DUMPFILE=app_owner_m2.dmp \
  LOGFILE=exp_app_owner_m2.log \
  SCHEMAS=APP_OWNER
```

### O que o Data Pump faz

- exporta dados e metadados Oracle;
- gera dump lógico;
- ajuda em migração, cópia e refresh de ambientes.

### Validar arquivo gerado no container

```bash
ls -lah /opt/oracle/labdata
```

```bash
cat /opt/oracle/labdata/exp_app_owner_m2.log
```

### Copiar dump para o host

```bash
podman cp oracle-free-full-23ai:/opt/oracle/labdata/app_owner_m2.dmp .
```

### Preparar o usuário clone

Conectar como usuário administrativo:

```sql
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_clone;
```

### Importar com remapeamento usando `impdp`

```bash
impdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_dir \
  DUMPFILE=app_owner_m2.dmp \
  LOGFILE=imp_app_clone_m2.log \
  REMAP_SCHEMA=APP_OWNER:APP_CLONE
```

### Validação do import

Conectar como `APP_CLONE`:

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

```sql
SELECT COUNT(*)
FROM produtos;
```

```bash
cat /opt/oracle/labdata/imp_app_clone_m2.log
```

## 14. Limpeza rápida do laboratório

```sql
NOAUDIT POLICY pol_select_produtos_m2;
NOAUDIT POLICY pol_logon_m2;

DROP AUDIT POLICY pol_select_produtos_m2;
DROP AUDIT POLICY pol_logon_m2;
```

```sql
DROP DIRECTORY lab_dir;
DROP DIRECTORY dpump_dir;

DROP ROLE role_leitura_m2;
DROP ROLE role_carga_m2;

DROP USER analista CASCADE;
DROP USER operador_carga CASCADE;
DROP USER app_clone CASCADE;
DROP USER app_owner CASCADE;

DROP PROFILE prof_lab_m2;
```

## 15. Resultado esperado

Ao final da revisão, o que precisa ficar claro é:

- segurança Oracle é controle de identidade, acesso e governança;
- usuário, schema, privilégio, role e perfil se conectam;
- auditoria existe para registrar e provar ações;
- carga em volume precisa de critério e ferramenta correta;
- parte da prática usa binários nativos do Oracle executados dentro do container;
- SQL*Loader, tabela externa e Data Pump atendem cenários diferentes.

## Scripts originais do módulo

- `modulo2-material/02-teoria-modulo2.md`
  - base conceitual do módulo.
- `modulo2-material/02-pratica-modulo2.md`
  - roteiro prático completo com usuários, roles, auditoria e carga.
- `modulo2-material/modulo2-seguranca-carga/scripts/03-sqlldr.sh`
  - apoio para carga com `SQL*Loader`.
- `modulo2-material/modulo2-seguranca-carga/scripts/04-expdp.sh`
  - apoio para exportação lógica com `Data Pump`.
- `modulo2-material/modulo2-seguranca-carga/scripts/05-impdp.sh`
  - apoio para importação lógica com `Data Pump`.
