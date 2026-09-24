# Laboratório - Aula 1

Execute os passos na ordem. Cada bloco confirma a etapa anterior antes de avançar.

## 1. Iniciar o Oracle com Podman

Em um ambiente novo:

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

### Leitura do comando

| Trecho | O que faz |
| :--- | :--- |
| `--name oracle-free-full-23ai` | Dá um nome para controlar o container com `podman ps`, `podman logs`, `podman start` e `podman stop`. |
| `-p 1522:1521` | Liga a porta `1522` do computador à porta `1521` dentro do container. A IDE usa `1522`. |
| `--cap-add SYS_NICE` | Adiciona a capability Linux que permite aos processos Oracle ajustar prioridade e políticas de escalonamento da CPU quando necessário. |
| `-e ORACLE_PWD=OraclePwd123` | Define a senha inicial dos usuários administrativos da imagem. Não define o nome de usuário. |
| `-e ORACLE_PDB=FREEPDB1` | Define o nome da PDB usada pelo laboratório. `FREEPDB1` não é o nome do aluno. |
| `-v oracle-free-full-23ai-data:/opt/oracle/oradata:Z` | Guarda os arquivos do Oracle no volume e os monta em `/opt/oracle/oradata`. O sufixo `:Z` ajusta o contexto de acesso em ambientes que usam SELinux. |
| `container-registry.oracle.com/database/free:latest` | Imagem Oracle Free que será executada. |

O comando não informa um usuário porque o container apenas inicializa o banco. A imagem já prepara usuários administrativos. A senha definida em `ORACLE_PWD` será usada para o login inicial como `SYSTEM`:

```txt
User: system
Password: OraclePwd123
Role: Normal
Service Name: FREEPDB1
```

`FREEPDB1` é o nome da PDB do laboratório. O CDB inicial da imagem é `FREE`:

```txt
CDB FREE
└── PDB FREEPDB1
```

`JEFF`, `JEFFOTONI` ou `APP_AULA1` podem ser nomes de usuários. Eles não alteram automaticamente o nome do CDB ou da PDB.

Se o container já existir e estiver parado:

```bash
podman start oracle-free-full-23ai
```

Verifique o estado:

```bash
podman ps --filter name=oracle-free-full-23ai
```

Acompanhe a inicialização quando necessário:

```bash
podman logs -f oracle-free-full-23ai
```

Interrompa apenas o acompanhamento com `Ctrl+C`. Não pare o container.

## 2. Criar a conexão na IDE

Use Oracle SQL Developer, CloudBeaver, DBeaver ou outra ferramenta disponível.

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: system
Password: OraclePwd123
Role: Normal
```

Não preencha `SID` e `Service Name` ao mesmo tempo. Para esta prática, selecione `Service Name`.

```txt
SID          = FREE
Service Name = FREEPDB1
CDB          = FREE
PDB          = FREEPDB1
```

## 2.1. Tipos de login e ordem correta

O Oracle já possui usuários administrativos quando a imagem é inicializada. A senha informada em `ORACLE_PWD` é usada no laboratório para os acessos administrativos iniciais.

### `SYSTEM`: primeiro login pela IDE

Use `SYSTEM` como a primeira conexão normal da aula:

```txt
User: system
Password: OraclePwd123
Role: Normal
Service Name: FREEPDB1
```

Use esse usuário para:

- validar a instância e a PDB;
- consultar `DBA_*` e `V$`;
- criar o usuário da aplicação;
- conceder quota e privilégios necessários.

Se quiser testar o mesmo login pela linha de comando:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

### `APP_AULA1`: usuário da aplicação

Esse usuário será criado durante a prática. Ele deve ser usado para:

- criar tabelas da aplicação;
- inserir, consultar, alterar e remover dados;
- visualizar os objetos do próprio schema.

Ele não deve receber privilégios administrativos desnecessários.

Depois que o usuário for criado, o login pela linha de comando será:

```bash
sqlplus app_aula1/AppAula1_123@//localhost:1521/FREEPDB1
```

Dentro do container, o listener usa a porta interna `1521`. Pela IDE no computador, a porta publicada é `1522`.

### `SYS`: administração privilegiada

`SYS` é o proprietário do dicionário Oracle. Use-o somente quando a operação exigir `SYSDBA`, como uma tarefa de instância ou recuperação.

Dentro do container, uma conexão administrativa local pode ser aberta assim:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus / as sysdba
```

Não use `SYS` como usuário da aplicação e não comece a prática criando tabelas com ele.

### Resumo da ordem

```txt
SYSTEM    -> observa e prepara
APP_AULA1 -> trabalha nos próprios objetos
SYS       -> administra a instância quando necessário
```

## 2.2. Onde o Oracle é colocado no container

O arquivo usado para a versão construída localmente é:

Conteúdo relevante:

```dockerfile
FROM container-registry.oracle.com/database/free:latest

ENV ORACLE_PWD=OraclePwd123
ENV ORACLE_PDB=FREEPDB1

EXPOSE 1521
```

Leitura de cada linha:

| Linha | Significado |
| :--- | :--- |
| `FROM` | Usa a imagem Oracle Free como base do container. |
| `ORACLE_PWD` | Define a senha inicial dos usuários administrativos da imagem. |
| `ORACLE_PDB` | Define a PDB criada ou usada na inicialização. |
| `EXPOSE 1521` | Documenta a porta interna usada pelo listener Oracle. |

O `Containerfile` não é o banco em si. Ele descreve como montar uma imagem baseada no Oracle. No comando `podman run` desta aula, usamos diretamente a imagem oficial do registry para reduzir etapas.

Se quiser visualizar o arquivo no terminal:

```bash
cat repo/oracle/versoes/free-full-23ai/containerfile/Containerfile
```

O [Containerfile completo](../../repo/oracle/versoes/free-full-23ai/containerfile/Containerfile) fica disponível como referência ao final desta explicação.

## 3. Confirmar instância e banco

Execute conectado como `system` no serviço `FREEPDB1`.

### Instância ativa

```sql
SELECT instance_name,
       host_name,
       status
FROM v$instance;
```

Resultado esperado: `INSTANCE_NAME` semelhante a `FREE` e `STATUS` igual a `OPEN`.

### Banco e arquitetura multitenant

```sql
SELECT name AS database_name,
       open_mode,
       cdb
FROM v$database;
```

Resultado esperado: `CDB` igual a `YES`.

### Container da sessão

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container,
       SYS_CONTEXT('USERENV', 'SESSION_USER') AS session_user,
       SYS_CONTEXT('USERENV', 'SERVICE_NAME') AS service_name
FROM dual;
```

Resultado esperado: container `FREEPDB1` e service name compatível com a PDB usada.

### PDBs existentes

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

### Services disponíveis

```sql
SELECT name AS service_name
FROM v$services
ORDER BY name;
```

## 3.1. O que existe dentro da PDB

A PDB `FREEPDB1` já possui estrutura administrativa antes de qualquer tabela da aula ser criada. Execute as consultas abaixo ainda como `system`.

### Usuários e contas

Um usuário é uma identidade que pode autenticar no banco. Usuários internos existem para o funcionamento e a administração do Oracle; não devem ser tratados como usuários da aplicação.

```sql
SELECT username,
       account_status,
       common,
       default_tablespace
FROM dba_users
ORDER BY username;
```

Não memorize todos os nomes retornados. Observe que existem usuários internos e administrativos. Eles pertencem ao funcionamento do Oracle e não devem ser alterados sem necessidade.

### Tablespaces

`Tablespace` é uma área lógica de armazenamento. Ela organiza onde segmentos, tabelas e índices podem ser gravados.

No laboratório:

- `SYSTEM`: metadados centrais do Oracle;
- `SYSAUX`: dados auxiliares de componentes Oracle;
- `TEMP`: operações temporárias, como ordenações;
- `USERS`: tablespace normalmente usado pelos objetos de laboratório.

```sql
SELECT tablespace_name,
       status,
       contents,
       extent_management
FROM dba_tablespaces
ORDER BY tablespace_name;
```

No laboratório, os nomes mais importantes costumam ser `SYSTEM`, `SYSAUX`, `TEMP` e `USERS`. A lista exata pode variar conforme a versão da imagem.

### Datafiles

`Datafile` é o arquivo físico que implementa uma tablespace permanente no armazenamento. A tablespace é lógica; o datafile é físico.

```sql
SELECT file_id,
       file_name,
       tablespace_name,
       ROUND(bytes / 1024 / 1024) AS size_mb,
       status
FROM dba_data_files
ORDER BY file_id;
```

Essa consulta mostra os arquivos físicos que sustentam as tablespaces permanentes.

### Objetos por proprietário

Um objeto é uma estrutura registrada no banco, como tabela, índice, view, sequence ou procedure. O proprietário indica o schema ao qual ele pertence.

```sql
SELECT owner,
       object_type,
       COUNT(*) AS total_objects
FROM dba_objects
GROUP BY owner, object_type
ORDER BY owner, object_type;
```

O objetivo não é estudar todos os objetos neste momento. É perceber que o banco já contém objetos internos antes da criação da tabela `AMBIENTE_AULA1`.

### Tabelas administrativas com segurança

Não consulte diretamente as tabelas internas do usuário `SYS`. Use as visões do dicionário:

```sql
SELECT owner,
       table_name,
       tablespace_name
FROM dba_tables
WHERE owner IN ('SYSTEM', 'APP_AULA1')
ORDER BY owner, table_name;
```

Depois que `APP_AULA1` for criado, a lista dele estará inicialmente vazia. Após o `CREATE TABLE`, a tabela `AMBIENTE_AULA1` aparecerá.

## 4. Criar o usuário de laboratório

Ainda como `system`, garanta que a sessão está na PDB:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

Crie a identidade que será usada para criar objetos:

```sql
CREATE USER app_aula1
IDENTIFIED BY AppAula1_123
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA 100M ON USERS;

GRANT CREATE SESSION,
      CREATE TABLE,
      CREATE VIEW,
      CREATE SEQUENCE
TO app_aula1;
```

Confirme o usuário:

```sql
SELECT username,
       account_status,
       default_tablespace
FROM dba_users
WHERE username = 'APP_AULA1';
```

O usuário `APP_AULA1` também será o proprietário do schema `APP_AULA1`.

## 5. Conectar com o usuário da aplicação

Crie uma segunda conexão na IDE:

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: app_aula1
Password: AppAula1_123
Role: Normal
```

Confirme a identidade da sessão:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 6. Criar a primeira tabela

Agora o usuário cria objetos dentro do próprio schema:

```sql
CREATE TABLE ambiente_aula1 (
    id          NUMBER GENERATED BY DEFAULT AS IDENTITY,
    conceito    VARCHAR2(80) NOT NULL,
    observacao  VARCHAR2(200),
    criado_em   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT pk_ambiente_aula1 PRIMARY KEY (id)
);
```

Confirme a tabela:

```sql
SELECT table_name
FROM user_tables
WHERE table_name = 'AMBIENTE_AULA1';
```

## 7. Inserir, consultar, alterar e remover

```sql
INSERT INTO ambiente_aula1 (conceito, observacao)
VALUES ('PDB', 'Banco lógico de trabalho');

INSERT INTO ambiente_aula1 (conceito, observacao)
VALUES ('Schema', 'Objetos pertencentes ao usuário');

COMMIT;
```

Consulte os dados:

```sql
SELECT id,
       conceito,
       observacao,
       criado_em
FROM ambiente_aula1
ORDER BY id;
```

Atualize um registro:

```sql
UPDATE ambiente_aula1
SET observacao = 'Objetos pertencentes ao usuário APP_AULA1'
WHERE conceito = 'Schema';

COMMIT;
```

Valide novamente:

```sql
SELECT *
FROM ambiente_aula1
ORDER BY id;
```

Se quiser demonstrar `DELETE`, remova apenas um registro de teste:

```sql
DELETE FROM ambiente_aula1
WHERE conceito = 'PDB';

COMMIT;
```

## 8. Observar o schema como usuário

```sql
SELECT table_name,
       tablespace_name
FROM user_tables
ORDER BY table_name;
```

```sql
SELECT object_name,
       object_type,
       status
FROM user_objects
ORDER BY object_type, object_name;
```

A regra é simples: `USER_*` mostra os objetos acessíveis ou pertencentes ao usuário atual.

## 9. Observar a arquitetura como system

Volte para a conexão `system`.

### Memória

`SGA` é a área de memória compartilhada da instância. `PGA` é a memória privada usada por processos e sessões. As consultas abaixo mostram parâmetros e componentes observáveis.

```sql
SELECT component,
       current_size
FROM v$sga_dynamic_components
WHERE current_size > 0
ORDER BY component;
```

```sql
SELECT name,
       value
FROM v$parameter
WHERE name IN ('memory_target', 'sga_target', 'pga_aggregate_target')
ORDER BY name;
```

Leitura mental:

```txt
SGA = memória compartilhada da instância
PGA = memória privada de processos e sessões
```

### Processos

Processos de background executam tarefas internas do Oracle. Eles não são usuários e não são tabelas; são processos que mantêm a instância funcionando.

```sql
SELECT name,
       description
FROM v$bgprocess
WHERE name IN ('PMON', 'SMON', 'DBW0', 'LGWR')
ORDER BY name;
```

Leitura mental:

```txt
PMON = limpeza e suporte a processos
SMON = recuperação e manutenção
DBW0 = grava blocos nos datafiles
LGWR = grava alterações nos redo logs
```

### PFILE e SPFILE

`PFILE` é um arquivo de parâmetros em texto. `SPFILE` é um arquivo binário de parâmetros, normalmente usado pelo Oracle para iniciar a instância.

```sql
SELECT value AS spfile_in_use
FROM v$parameter
WHERE name = 'spfile';
```

Interpretação:

```txt
valor preenchido = inicialização usando SPFILE
valor nulo       = inicialização usando PFILE
```

Não altere parâmetros nesta primeira execução. O objetivo é reconhecer o arquivo em uso.

### Arquivos persistentes

- `Datafiles`: armazenam tabelas, índices e outros segmentos.
- `Redo logs`: registram alterações para garantir recuperação.
- `Control files`: guardam informações estruturais sobre o banco e seus arquivos.

```sql
SELECT file_id,
       file_name,
       tablespace_name,
       status
FROM dba_data_files
ORDER BY file_id;
```

```sql
SELECT group#,
       member
FROM v$logfile
ORDER BY group#, member;
```

```sql
SELECT name
FROM v$controlfile;
```

## Extensão: criar e administrar uma nova PDB

Depois de concluir o fluxo principal, siga o [manual completo de criação e administração de PDB](./pdb.md). A sequência inclui a conexão como `SYSTEM` na `FREEPDB1`, a mudança para `CDB$ROOT`, a consulta dos datafiles da `PDB$SEED`, a criação da `DBJEFFOTONI` com `FILE_NAME_CONVERT`, os erros `ORA-65016` e `ORA-01031`, a abertura com `SYS AS SYSDBA`, a validação dos modos `READ ONLY` e `READ WRITE`, o retorno para `FREEPDB1` e a explicação de usuários, schemas e objetos.

## 10. Desafio final

Sem copiar a sequência anterior, tente executar:

1. consultar o container atual;
2. conectar como `app_aula1`;
3. listar as tabelas do próprio schema;
4. inserir um terceiro conceito;
5. consultar os dados;
6. explicar qual parte foi Podman, qual parte foi Oracle e qual parte foi SQL.

## 11. Limpeza opcional

Se precisar remover somente o laboratório criado:

```sql
DROP USER app_aula1 CASCADE;
```

Execute como `system` dentro da `FREEPDB1`. Não remova o usuário em um ambiente compartilhado sem confirmar antes.
