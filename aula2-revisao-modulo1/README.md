# Revisão do Módulo 1 - aula 2

> Revisão do módulo 1: Arquitetura Oracle, instância, banco, memória, processos, arquivos, parâmetros e dicionário de dados.

**Organização:**
  
  1. arquitetura
  2. memória
  3. processos
  4. arquivos
  5. parâmetros
  6. dicionário de dados
  7. resumo final
  
## Ideia central do módulo

O ponto mais importante do módulo 1 é este:

```txt
Instância = memória + processos
Banco = arquivos físicos em disco
```

Leitura prática:

- a **instância** coloca o Oracle em funcionamento;
- o **banco de dados** guarda os arquivos persistidos;
- o Oracle administra memória, processos, arquivos e parâmetros ao mesmo tempo.

## Regra mental do módulo

```txt
Instância -> SGA + PGA + processos
Banco -> datafiles + redo logs + control files
Multitenant -> CDB + PDB
Configuração -> parâmetros
```

## O que precisa ficar claro

- diferença entre `instância` e `banco`;
- visão básica de `CDB` e `PDB`;
- o que é `SGA` e `PGA`;
- quais processos de background aparecem no Oracle;
- quais são os principais arquivos físicos;
- o que é parâmetro;
- diferença entre `PFILE` e `SPFILE`;
- como ler objetos e metadados pelo dicionário de dados.

## Arquitetura essencial

### Instância

- memória + processos em execução;
- parte viva do Oracle;
- responde por operação, cache, concorrência e administração.

### Banco de dados

- conjunto de arquivos físicos;
- persiste os dados em disco;
- continua existindo mesmo sem a instância ativa.

### Multitenant

```txt
CDB = container principal
PDB = banco lógico de trabalho
```

No laboratório:

```txt
CDB / SID: FREE
PDB / Service Name: FREEPDB1
```

## Memória

### SGA

- memória compartilhada da instância;
- usada por múltiplas sessões e processos;
- ajuda no reaproveitamento de blocos e SQL.

### PGA

- memória privada de cada processo;
- usada em ordenação, hash, operações internas e execução individual.

### Regra curta

```txt
SGA = compartilhada
PGA = privada por processo
```

## Processos importantes

Para revisão, estes nomes já resolvem bem:

- `DBWn` - grava blocos alterados em datafiles
- `LGWR` - grava redo logs
- `SMON` - recuperação e manutenção
- `PMON` - limpeza e suporte operacional

## Arquivos físicos essenciais

### Datafiles

- armazenam os dados persistidos;
- sustentam tablespaces, segmentos e objetos.

### Redo log files

- registram alterações;
- são fundamentais para recuperação.

### Control files

- guardam metadados estruturais do banco;
- são críticos para abertura e recuperação do ambiente.

## Estruturas lógicas essenciais

- `tablespace`
- `segment`
- `extent`
- `block`

Regra prática:

```txt
Lógico = tablespace / segmento
Físico = datafile
```

## Parâmetros

Parâmetros controlam comportamento do Oracle, por exemplo:

- memória;
- processos;
- sessões;
- cursores;
- operação geral da instância.

## PFILE e SPFILE

### PFILE

- arquivo texto;
- pode ser editado manualmente;
- mais simples de ler didaticamente.

Exemplo:

```ini
*.memory_target=1G
*.processes=300
*.open_cursors=500
```

### SPFILE

- arquivo persistente de parâmetros;
- é gerenciado pelo Oracle;
- normalmente é o modelo usado no ambiente em produção.

### O que é SPFILE

`SPFILE` (`Server Parameter File`) é o arquivo binário de configuração do Oracle Database.

Ele substitui o antigo `PFILE (init.ora)` textual e permite:

- alterações dinâmicas com `ALTER SYSTEM`;
- persistência automática de parâmetros;
- gerenciamento centralizado pelo Oracle.

### Diferença rápida

| Tipo | Formato | Editável manualmente | Persistente |
|---|---|---:|---:|
| **PFILE** | Texto (`initSID.ora`) | Sim | Sim |
| **SPFILE** | Binário (`spfileSID.ora`) | Não diretamente | Sim |

### Regra prática

```txt
PFILE = texto manual
SPFILE = persistente e gerenciado pelo Oracle
```

### Query importante para verificar SPFILE

```sql
SELECT name,
       value
FROM v$parameter
WHERE name = 'spfile';
```

### Exemplo de alteração persistente

```sql
ALTER SYSTEM SET open_cursors = 500 SCOPE=BOTH;
```

Leitura:

- altera em memória agora;
- persiste também no `SPFILE`.

## Dicionário de dados e visões de sistema

No módulo 1, não basta olhar só memória e processos. Também é importante saber onde observar objetos, metadados e estrutura administrativa.

### Famílias mais importantes

#### USER_

- mostra objetos do usuário atual;
- ideal para leitura do próprio schema.

#### ALL_

- mostra objetos acessíveis ao usuário;
- útil para ver o que pode ser consultado além do próprio schema.

#### DBA_

- mostra visão administrativa mais ampla;
- normalmente exige privilégios maiores.

#### V$

- mostra estado dinâmico do Oracle;
- é a família mais usada para arquitetura, memória, processos, sessões e parâmetros.

### Regra prática

```txt
USER_ = meu schema
ALL_ = o que eu consigo acessar
DBA_ = visão administrativa
V$ = estado do Oracle em execução
```

## Queries essenciais de revisão

### Validar instância

```sql
SELECT instance_name,
       status,
       version
FROM v$instance;
```

### Validar banco

```sql
SELECT name,
       dbid,
       cdb,
       open_mode
FROM v$database;
```

### Ver container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### Ver PDBs

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status
FROM v$pdbs
ORDER BY con_id;
```

### Ver versão do Oracle

```sql
SELECT banner
FROM v$version;
```

### Ver componentes instalados

```sql
SELECT product,
       version,
       status
FROM product_component_version;
```

### Ver memória compartilhada

```sql
SELECT * FROM v$sga;
```

### Ver estatísticas da SGA

```sql
SELECT pool,
       name,
       bytes
FROM v$sgastat
ORDER BY pool, bytes DESC;
```

### Ver processos de background

```sql
SELECT name,
       description
FROM v$bgprocess
WHERE paddr <> '00'
ORDER BY name;
```

### Ver sessões

```sql
SELECT sid,
       serial#,
       username,
       status,
       program
FROM v$session
ORDER BY sid;
```

### Ver processos do sistema

```sql
SELECT spid,
       program
FROM v$process
ORDER BY spid;
```

### Ver tablespaces

```sql
SELECT tablespace_name,
       contents,
       status
FROM dba_tablespaces
ORDER BY tablespace_name;
```

### Ver datafiles

```sql
SELECT file_id,
       file_name,
       tablespace_name,
       bytes / 1024 / 1024 AS mb
FROM dba_data_files
ORDER BY file_id;
```

### Ver temp files

```sql
SELECT tablespace_name,
       file_name,
       bytes / 1024 / 1024 AS mb
FROM dba_temp_files
ORDER BY tablespace_name;
```

### Ver redo log files

```sql
SELECT member
FROM v$logfile
ORDER BY member;
```

### Ver control files

```sql
SELECT name
FROM v$controlfile
ORDER BY name;
```

### Ver parâmetros principais

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name IN ('open_cursors', 'processes', 'sessions')
ORDER BY name;
```

### Ver parâmetros específicos

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'open_cursors';
```

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'processes';
```

```sql
SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'sessions';
```

## Queries de dicionário de dados

### Tabelas do usuário atual

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

### Objetos do usuário atual

```sql
SELECT object_name,
       object_type
FROM user_objects
ORDER BY object_type, object_name;
```

### Colunas das tabelas do usuário

```sql
SELECT table_name,
       column_name,
       data_type
FROM user_tab_columns
ORDER BY table_name, column_id;
```

### Tabelas acessíveis ao usuário

```sql
SELECT owner,
       table_name
FROM all_tables
ORDER BY owner, table_name;
```

### Usuários do banco

```sql
SELECT username,
       account_status,
       default_tablespace
FROM dba_users
ORDER BY username;
```

### Roles do banco

```sql
SELECT role
FROM dba_roles
ORDER BY role;
```

## Resumo final

```txt
1. Entender instância vs banco
2. Entender CDB e PDB
3. Entender SGA e PGA
4. Reconhecer processos principais
5. Reconhecer datafiles, redo logs e control files
6. Ler parâmetros
7. Saber a diferença entre PFILE e SPFILE
8. Ler o dicionário de dados e as visões do sistema
```

## Arquivos de apoio

- `modulo1-material/01-teoria-modulo1.md`
- `modulo1-material/02-pratica-modulo1.md`
- `modulo1-material/scripts/01-validacao-ambiente.sql`
- `modulo1-material/scripts/03-memoria-processos-arquivos.sql`
- `modulo1-material/scripts/04-parametros-e-privilegios.sql`

## Scripts originais do módulo

Se for necessário aprofundar a revisão ou repetir a prática completa, estes scripts ajudam bastante:

- `modulo1-material/scripts/01-validacao-ambiente.sql`
  - usar para validar instância, banco, container atual e componentes instalados.
- `modulo1-material/scripts/03-memoria-processos-arquivos.sql`
  - usar para revisar memória, processos, tablespaces, datafiles, redo logs e control files.
- `modulo1-material/scripts/04-parametros-e-privilegios.sql`
  - usar para revisar parâmetros, `SPFILE`, containers e privilégios de laboratório.
