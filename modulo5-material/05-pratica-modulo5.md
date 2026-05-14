# Módulo 5 - Prática  
## Oracle 12c Multitenant e Ambiente de Nuvem

## Visão geral

Neste módulo usaremos um laboratório prático para consolidar os principais conceitos de arquitetura multitenant e sua relação com ambientes modernos de nuvem Oracle.

A prática será organizada em blocos progressivos:

1. preparação do ambiente;
2. identificação do CDB e das PDBs;
3. observação do escopo administrativo entre container e pluggable database;
4. operações básicas de abertura, fechamento e persistência de estado de PDB;
5. criação e administração de usuários em contexto multitenant;
6. observação de visões administrativas relacionadas a CDB e PDB;
7. bloco opcional para criação de PDB adicional;
8. bloco final de contextualização prática de OCI, DBaaS e Autonomous Database.

A proposta é manter um laboratório viável em Podman, sem depender obrigatoriamente de uma conta Oracle Cloud, mas conectando a prática local aos conceitos de cloud.

---

## Ambiente utilizado

Usaremos:

- Podman;
- Oracle Database Free em container;
- CloudBeaver para consultas e navegação dos objetos;
- scripts SQL para observação do ambiente multitenant.

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
- **instância**: `FREE`
- **PDB padrão**: `FREEPDB1`

Também poderemos usar, opcionalmente, uma PDB adicional:

- **PDB opcional**: `LABPDB1`

---

## 1. Estrutura recomendada do módulo

```text
modulo5-multitenant-nuvem/
├── compose.yaml
└── scripts/
```

---

## 2. Subida do ambiente com Podman

## 2.1. Opção simples - usar apenas a PDB padrão FREEPDB1

```yaml
services:
  oracle-free:
    image: gvenzl/oracle-free:latest
    container_name: oracle-free
    ports:
      - "1521:1521"
    environment:
      ORACLE_PASSWORD: Senha123
```

## 2.2. Opção com PDB adicional criada na inicialização

> Esta opção deve ser usada apenas quando quisermos começar o laboratório já com mais de uma PDB.

```yaml
services:
  oracle-free:
    image: gvenzl/oracle-free:latest
    container_name: oracle-free
    ports:
      - "1521:1521"
    environment:
      ORACLE_PASSWORD: Senha123
      ORACLE_DATABASE: LABPDB1
```

### Observação importante

A criação de PDB adicional por variável de ambiente ocorre na inicialização do container, especialmente no primeiro bootstrap do banco. Se já houver volume persistente reaproveitado, a criação automática pode não acontecer novamente.

## 2.3. Comandos para subir o ambiente

```bash
podman compose up -d
podman ps
podman logs -f oracle-free
```

## 2.4. Entrar no container

```bash
podman exec -it oracle-free bash
```

## 2.5. Conectar como SYSDBA

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

---

## 3. Bloco prático - identificar o ambiente multitenant

Antes das queries, vale manter este mapa mental:

```txt
Oracle Instance
 └── CDB
      └── PDB
           └── USER
                └── SCHEMA
                     └── TABLES
```

No laboratório do curso, isso normalmente significa:

```txt
FREE
 └── FREEPDB1
```

Regra importante:

- `SID` aponta para a instância;
- `Service Name` aponta para a `PDB`;
- em ambiente multitenant, a conexão de aplicação normalmente usa o `Service Name` da `PDB`.

## 3.1. Ver nome da instância

```sql
SELECT instance_name, status
FROM v$instance;
```

## 3.2. Ver nome do banco e modo de abertura

```sql
SELECT name, open_mode, cdb
FROM v$database;
```

## 3.3. Ver containers disponíveis

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
SELECT SYS_CONTEXT('USERENV', 'CON_ID') AS current_container_id
FROM dual;
```

## 3.4. Listar as PDBs

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status,
       restricted
FROM v$pdbs
ORDER BY con_id;
```

## 3.5. Listar containers de forma mais detalhada

```sql
SELECT con_id, dbid, guid, name, open_mode
FROM v$containers
ORDER BY con_id;
```

## 3.6. Checklist multitenant mínimo

```sql
SELECT instance_name,
       status
FROM v$instance;

SELECT name,
       cdb,
       open_mode
FROM v$database;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT SYS_CONTEXT('USERENV', 'CON_ID') AS current_container_id
FROM dual;
```

### Interpretação

Esse bloco deverá mostrar claramente:

- o container raiz;
- a PDB seed;
- a PDB de trabalho (`FREEPDB1`);
- e, se configurada, uma PDB adicional como `LABPDB1`.

Leitura prática:

- `FREE` representa a instância e o container principal;
- `FREEPDB1` representa o banco lógico de trabalho;
- em vez de `USE database`, a conexão Oracle normalmente entra diretamente na `PDB` correta.

---

## 4. Bloco prático - alternar entre CDB e PDB

## 4.1. Ver container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 4.2. Mudar para a PDB padrão

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 4.3. Voltar para o root

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 4.4. Se existir LABPDB1, acessar a PDB adicional

```sql
ALTER SESSION SET CONTAINER = LABPDB1;
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### Objetivo deste bloco

Deveríamos reforçar que várias operações administrativas dependem do escopo atual:

- operações no root;
- operações no nível da PDB.

---

## 5. Bloco prático - abertura, fechamento e SAVE STATE de PDB

## 5.1. Ver estado atual das PDBs

Conectar no root:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 5.2. Fechar a PDB FREEPDB1

```sql
ALTER PLUGGABLE DATABASE FREEPDB1 CLOSE IMMEDIATE;
```

Validar:

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 5.3. Abrir a PDB FREEPDB1

```sql
ALTER PLUGGABLE DATABASE FREEPDB1 OPEN;
```

Validar:

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 5.4. Salvar o estado da PDB

```sql
ALTER PLUGGABLE DATABASE FREEPDB1 SAVE STATE;
```

## 5.5. Ver PDBs com estado salvo

```sql
SELECT con_id, pdb_name, state
FROM dba_pdb_saved_states
ORDER BY con_id;
```

### Interpretação

Esse bloco é importante para mostrar que a administração de PDB inclui:

- abrir;
- fechar;
- persistir o comportamento de abertura;
- controlar o ciclo de vida operacional.

---

## 6. Bloco prático - criação de usuários em contexto multitenant

Este bloco deverá mostrar a diferença entre usuário comum e usuário local, em nível introdutório.

## 6.1. Criar usuário comum no root

Conectar no root:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

Criar usuário comum:

```sql
CREATE USER c##admin_lab IDENTIFIED BY AdminLab123 CONTAINER=ALL;
GRANT CREATE SESSION TO c##admin_lab CONTAINER=ALL;
```

## 6.2. Validar o usuário comum

```sql
SELECT username, common
FROM cdb_users
WHERE username = 'C##ADMIN_LAB';
```

## 6.3. Criar usuário local na FREEPDB1

Ir para a PDB:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

Criar usuário local:

```sql
CREATE USER app_pdb IDENTIFIED BY AppPdb123;
GRANT CREATE SESSION, CREATE TABLE TO app_pdb;
```

## 6.4. Validar o usuário local

Conectar no root para ver em visão CDB:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

```sql
SELECT username, common, con_id
FROM cdb_users
WHERE username IN ('C##ADMIN_LAB', 'APP_PDB')
ORDER BY username, con_id;
```

### Interpretação

Este bloco é importante para mostrar:

- o usuário comum existe no escopo do container;
- o usuário local pertence à PDB específica;
- multitenant altera o contexto da administração de identidades.

---

## 7. Bloco prático - objetos em PDB

## 7.1. Conectar como usuário local

Conectar no CloudBeaver como `app_pdb`.

## 7.2. Criar tabela de teste

```sql
CREATE TABLE clientes_pdb (
  id_cliente NUMBER PRIMARY KEY,
  nome       VARCHAR2(100),
  cidade     VARCHAR2(50)
);
```

## 7.3. Inserir dados

```sql
INSERT INTO clientes_pdb VALUES (1, 'Ana', 'Belo Horizonte');
INSERT INTO clientes_pdb VALUES (2, 'Bruno', 'São Paulo');
COMMIT;
```

## 7.4. Validar dados

```sql
SELECT * FROM clientes_pdb;
```

## 7.5. Observar objetos na PDB

Conectar como `SYS` com papel `SYSDBA` e entrar na `FREEPDB1`.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;

SELECT owner, object_name, object_type
FROM dba_objects
WHERE owner = 'APP_PDB'
ORDER BY object_type, object_name;
```

### Interpretação

Este bloco reforça que a PDB funciona como ambiente lógico próprio, com seus usuários e objetos locais.

---

## 8. Bloco prático - visões CDB e DBA

Um dos objetivos do laboratório é mostrar como a administração em multitenant amplia a necessidade de leitura correta do escopo.

## 8.1. Ver usuários no nível de CDB

Conectar no root:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

```sql
SELECT con_id, username, common
FROM cdb_users
ORDER BY con_id, username;
```

## 8.2. Ver tablespaces por container

```sql
SELECT con_id, tablespace_name, status
FROM cdb_tablespaces
ORDER BY con_id, tablespace_name;
```

## 8.3. Ver datafiles por container

```sql
SELECT con_id, file_name, tablespace_name
FROM cdb_data_files
ORDER BY con_id, file_name;
```

## 8.4. Ver PDBs no dicionário

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status
FROM v$pdbs
ORDER BY con_id;
```

### Interpretação

Esse bloco é útil para mostrar que o administrador em multitenant precisa entender a diferença entre:

- visões locais;
- visões consolidadas;
- administração no root;
- administração dentro da PDB.

---

## 9. Bloco prático - criação opcional de PDB por SQL

> Este bloco deve ser tratado como opcional. Em laboratório simples, a prática principal poderá ser feita apenas com `FREEPDB1` e, se configurada, com `LABPDB1` criada pela variável de ambiente.

A criação manual de PDB por SQL pode variar conforme layout de arquivos, configuração do ambiente e storage.

## 9.1. Princípio conceitual

No Oracle, a criação de uma PDB a partir da seed é feita com `CREATE PLUGGABLE DATABASE`.

## 9.2. Exemplo conceitual

```sql
CREATE PLUGGABLE DATABASE LABPDB2
  ADMIN USER pdbadmin IDENTIFIED BY PdbAdmin123
  FILE_NAME_CONVERT = (
    '/opt/oracle/oradata/FREE/pdbseed/',
    '/opt/oracle/oradata/FREE/LABPDB2/'
  );
```

## 9.3. Observação importante

Esse comando deverá ser ajustado ao layout real dos arquivos do ambiente. Em laboratório introdutório, faz mais sentido:

- entender o comando;
- entender a lógica da seed;
- tratar a criação real como exercício opcional e controlado.

---

## 10. Bloco prático - clone de PDB (visão introdutória)

O clone é um dos recursos mais interessantes da arquitetura multitenant.

## 10.1. Exemplo conceitual de clone

```sql
CREATE PLUGGABLE DATABASE LABPDB_CLONE FROM FREEPDB1;
```

## 10.2. Observação importante

A viabilidade prática do clone dependerá do ambiente, espaço em disco e permissões. Em laboratório simples com Oracle Free, deveríamos tratar o clone como:

- operação desejável;
- recurso importante de administração;
- demonstração opcional, se o ambiente permitir.

## 10.3. Valor administrativo

O clone é especialmente útil para:

- homologação;
- testes;
- cópia rápida de ambiente;
- criação de variantes controladas.

---

## 11. Bloco prático - plug e unplug (visão conceitual)

Plug e unplug são operações avançadas de ciclo de vida.

## 11.1. O que representam

- **unplug**: retirar logicamente uma PDB de um CDB;
- **plug**: conectar uma PDB a um container adequado.

## 11.2. Valor administrativo

Essas operações são relevantes em:

- reorganização de ambientes;
- migração;
- consolidação;
- movimentação entre estruturas compatíveis.

## 11.3. Abordagem recomendada em laboratório

Deveríamos apresentar:

- o conceito;
- o papel administrativo;
- a sintaxe básica;
- os pré-requisitos.

Mas não é obrigatório executar unplug/plug em toda turma, porque é uma operação mais sensível.

---

## 12. Bloco prático - conexão direta em PDB via cliente

## 12.1. Conectar no CloudBeaver

Configuração de conexão para a PDB padrão:

- Host: `localhost`
- Porta: `1521`
- Service name: `FREEPDB1`
- Usuário: `app_pdb`
- Senha: `AppPdb123`

Se houver PDB adicional:

- Service name: `LABPDB1`

## 12.2. Objetivo

Esse passo ajuda a mostrar que, para a aplicação e para o cliente SQL, a PDB pode ser tratada como ponto lógico de conexão.

---

## 13. Bloco prático - observação do ambiente e reinício

## 13.1. Ver o estado salvo da PDB

Conectar como SYSDBA:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
SELECT con_id, pdb_name, state
FROM dba_pdb_saved_states
ORDER BY con_id;
```

## 13.2. Reiniciar o container

No sistema operacional:

```bash
podman restart oracle-free
podman logs -f oracle-free
```

## 13.3. Validar se a PDB volta conforme o estado salvo

Conectar como `SYS` com papel `SYSDBA` novamente.

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

### Interpretação

Esse passo ajuda a mostrar o valor administrativo do `SAVE STATE`.

---

## 14. Bloco final - OCI, DBaaS e Autonomous na prática do curso

Como o laboratório principal está em Podman local, a parte de nuvem deverá ser tratada de forma contextual e opcional, a menos que exista uma conta OCI disponível.

## 14.1. O que deveríamos observar mesmo sem OCI

Mesmo sem uma conta Oracle Cloud, este módulo já permite demonstrar:

- a lógica de consolidação com multitenant;
- a ideia de múltiplos bancos lógicos em estrutura compartilhada;
- operações administrativas sobre PDBs;
- a aproximação conceitual entre multitenant e modelos de serviço.

## 14.2. Se houver conta OCI disponível

Se houver ambiente Oracle Cloud disponível, poderemos explorar de forma opcional:

- criação de um serviço de banco;
- visualização de recursos de database service;
- comparação entre provisão local e provisão em nuvem;
- visão geral de DB System e Autonomous Database.

## 14.3. Sem conta OCI

Se não houver conta OCI, deveríamos fechar o módulo com:

- comparação entre laboratório local e cloud;
- discussão de responsabilidades administrativas;
- análise de cenários on-premises, cloud e híbridos.

---

## 15. Consultas úteis de apoio

## 15.1. Container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
SELECT SYS_CONTEXT('USERENV', 'CON_ID') AS current_container_id
FROM dual;
```

## 15.2. PDBs existentes

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 15.3. Diagnóstico enxuto de containers e serviços

```sql
SELECT con_id,
       name,
       open_mode
FROM v$containers
ORDER BY con_id;

SELECT name AS service_name,
       con_id
FROM v$active_services
ORDER BY con_id, service_name;
```

## 15.4. Usuários por container

```sql
SELECT con_id, username, common
FROM cdb_users
ORDER BY con_id, username;
```

## 15.5. Objetos do usuário local

Na PDB:

```sql
SELECT owner, object_name, object_type
FROM dba_objects
WHERE owner = 'APP_PDB'
ORDER BY object_type, object_name;
```

## 15.6. Sessões por container

```sql
SELECT con_id, sid, serial#, username, status
FROM cdb_sessions
ORDER BY con_id, sid;
```

> Observação: a disponibilidade de algumas visões pode variar por versão e privilégios.

## 15.7. Validação final do módulo

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

---

## 16. Limpeza do laboratório

## 16.1. Remover tabela e usuário local na PDB

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA`.

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
DROP USER app_pdb CASCADE;
```

## 16.2. Remover usuário comum

Voltar ao root:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
DROP USER c##admin_lab CASCADE CONTAINER=ALL;
```

## 16.3. Se houver PDB opcional criada automaticamente

A remoção de PDB adicional deverá ser tratada com cuidado, normalmente a partir do root.

Exemplo conceitual:

```sql
ALTER PLUGGABLE DATABASE LABPDB1 CLOSE IMMEDIATE;
DROP PLUGGABLE DATABASE LABPDB1 INCLUDING DATAFILES;
```

> Esse passo só deverá ser executado se realmente quisermos desmontar o laboratório extra.

---

## 17. Resultado esperado da prática

Ao final deste módulo, deveremos ter exercitado:

- identificação do CDB e das PDBs;
- alternância de contexto entre root e PDB;
- abertura, fechamento e `SAVE STATE` de PDB;
- criação de usuário comum e usuário local;
- criação de objetos em PDB;
- leitura de visões `CDB_*`, `DBA_*`, `V$PDBS` e `V$CONTAINERS`;
- compreensão prática do escopo multitenant;
- relação entre laboratório local, multitenant e modelos cloud.

---

## 18. Referências oficiais úteis

### Oracle Database Free em container
- https://github.com/gvenzl/oci-oracle-free

### CREATE PLUGGABLE DATABASE
- https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-PLUGGABLE-DATABASE.html

### Administering PDBs
- https://docs.oracle.com/en/database/oracle/oracle-database/23/multi/administering-pdbs-with-sql-plus.html

### Creating PDBs and Application Containers
- https://docs.oracle.com/en/database/oracle/oracle-database/23/multi/creating-pdbs.html

### OCI - Create a Pluggable Database
- https://docs.oracle.com/en/cloud/paas/base-database/create-pdb/index.html

### Oracle Database and Cloud
- https://www.oracle.com/database/
