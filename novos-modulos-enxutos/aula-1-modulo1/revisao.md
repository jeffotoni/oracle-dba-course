# Revisão - Fundamentos do Oracle

Use esta página depois da prática para consolidar o raciocínio.

## 1. Explique o caminho completo

```txt
Podman -> container -> instância -> CDB -> PDB -> usuário -> schema -> tabela -> query
```

Cada termo responde a uma pergunta:

| Termo | Pergunta respondida |
| :--- | :--- |
| Podman | Como o ambiente foi executado? |
| Container | Onde o Oracle está rodando? |
| Instância | Qual parte ativa mantém memória e processos? |
| CDB | Qual container administrativo organiza o ambiente? |
| PDB | Em qual banco lógico a sessão trabalha? |
| Usuário | Quem está autenticando? |
| Schema | De quem são os objetos? |
| Tabela | Onde os registros são armazenados? |
| Query | Como os dados são consultados? |

## Ordem de login

```txt
SYSTEM     -> primeira conexão normal da aula
APP_AULA1  -> usuário da aplicação e proprietário do schema
SYS        -> administração privilegiada, somente quando necessária
```

O primeiro login deve ser feito como `SYSTEM` na `FREEPDB1`. A partir dele, o ambiente é validado e o usuário `APP_AULA1` é criado. Depois, a conexão muda para `APP_AULA1` para demonstrar o trabalho da aplicação.

`SYS` não é um usuário comum de laboratório. Evite criar tabelas ou executar o CRUD com `SYS`.

## Administração de PDB

O Oracle multitenant organiza o ambiente desta forma:

```text
CDB$ROOT
├── PDB$SEED       -> modelo somente leitura
├── FREEPDB1       -> PDB inicial do laboratório
└── DBJEFFOTONI    -> PDB criada na extensão prática
```

Antes de qualquer comando, confirme o container atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container
FROM dual;
```

Para administrar PDBs, altere a sessão para o `CDB$ROOT`:

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
```

Para retornar ao laboratório:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

`PDB$SEED` é a base usada para criar outras PDBs. O `FILE_NAME_CONVERT` informa a origem dos datafiles e o destino da nova PDB. A abertura pode exigir `SYS AS SYSDBA`:

```bash
podman exec -it oracle-free-full-23ai bash
sqlplus / as sysdba
```

```sql
ALTER SESSION SET CONTAINER = CDB$ROOT;
ALTER PLUGGABLE DATABASE DBJEFFOTONI OPEN;

SELECT name, open_mode
FROM v$pdbs;
```

`SYSTEM` executa tarefas administrativas comuns, mas não possui automaticamente os mesmos privilégios de `SYSDBA`. `ALTER SESSION SET CONTAINER` muda apenas a sessão atual. Usuários criados dentro de uma PDB são locais àquela PDB, e os objetos pertencem ao schema do usuário conectado.

O fluxo completo está no [manual prático de criação e administração de PDB](./pdb.md).

## O que existe na PDB

Quando o container inicia, `FREEPDB1` já possui:

- usuários internos e administrativos;
- tablespaces como `SYSTEM`, `SYSAUX`, `TEMP` e `USERS`;
- datafiles;
- objetos do dicionário;
- serviços e metadados da arquitetura Oracle.

A tabela da aplicação não existe inicialmente. Ela aparece depois do comando `CREATE TABLE` executado por `APP_AULA1`.

Para observar o ambiente:

```sql
SELECT username, account_status
FROM dba_users
ORDER BY username;
```

```sql
SELECT tablespace_name, status, contents
FROM dba_tablespaces
ORDER BY tablespace_name;
```

```sql
SELECT owner, object_type, COUNT(*) AS total_objects
FROM dba_objects
GROUP BY owner, object_type
ORDER BY owner, object_type;
```

Use `DBA_*` e `V$` com `SYSTEM`. Use `USER_*` com `APP_AULA1`. Não consulte diretamente as tabelas internas de `SYS`.

## 2. Conexão do laboratório

```txt
Host: localhost
Port: 1522
SID: FREE
Service Name: FREEPDB1
CDB: FREE
PDB: FREEPDB1
```

Para a prática com tabelas, a escolha principal é:

```txt
Service Name = FREEPDB1
```

## 3. Respostas que precisam estar claras

### Por que não usar `CREATE DATABASE`?

Porque o Oracle Free já disponibiliza o ambiente de laboratório. A tarefa é conectar na PDB existente, criar o usuário e trabalhar no schema.

### Usuário e schema são iguais?

Não exatamente. O usuário autentica e o schema representa os objetos associados a ele. No uso comum do Oracle, os nomes aparecem iguais.

### Instância e banco são iguais?

Não. A instância é formada por memória e processos. O banco é formado pelos arquivos persistentes.

### O que é `PFILE`?

Arquivo de parâmetros em formato texto.

### O que é `SPFILE`?

Arquivo de parâmetros em formato binário, normalmente usado na inicialização do Oracle.

## 4. Cinco consultas essenciais

```sql
SELECT instance_name, status
FROM v$instance;
```

```sql
SELECT name, open_mode, cdb
FROM v$database;
```

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

```sql
SELECT con_id, name, open_mode
FROM v$pdbs
ORDER BY con_id;
```

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
```

## 5. Diagnóstico por camada

Quando algo falhar, siga a ordem:

```txt
1. Podman: o container está em execução?
2. Rede: host e porta estão corretos?
3. Serviço: o Service Name é FREEPDB1?
4. Sessão: o usuário entrou na PDB correta?
5. Privilégio: o usuário pode executar a operação?
6. Schema: a tabela pertence ao usuário esperado?
7. SQL: a consulta aponta para o objeto correto?
```

Consultas `V$` e `DBA_*` normalmente exigem uma conexão administrativa, como `system`. Consultas `USER_*` mostram os objetos do usuário atual.

## 6. Exercício de fechamento

Explique em voz alta, sem consultar o material:

> Eu subi um container com Podman. Dentro dele, o Oracle iniciou uma instância. A conexão usa o serviço `FREEPDB1`, que direciona a sessão para a PDB. O usuário `APP_AULA1` possui o schema de mesmo nome, criou uma tabela e consultou seus registros. A instância usa memória e processos, enquanto os arquivos persistem o banco.

## 7. Referências para aprofundar

- [Revisão do Módulo 0](../../aula1-revisao-modulo0/README.md)
- [Guia prático do Módulo 0](../../modulo0-guia-pratico/README.md)
- [Revisão do Módulo 1](../../aula2-revisao-modulo1/README.md)
- [Material completo do Módulo 1](../../modulo1-material/README.md)
