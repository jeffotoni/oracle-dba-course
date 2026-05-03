# Oracle Database Free / XE - Guia Administrativo Pratico

Este guia foi pensado para o momento em que se abre o Oracle em uma IDE como DBeaver, SQL Developer ou CloudBeaver e aparece uma estrutura grande, cheia de schemas, tipos, tablespaces, roles e objetos de sistema.

A intencao aqui e explicar:

- o que esta aparecendo na IDE;
- o que deve ignorar no primeiro momento;
- o que deve aprender primeiro;
- qual e a sequencia pratica correta para criar objetos no Oracle.

O foco e laboratorio com Oracle Free / XE, usando a PDB ja criada pelo ambiente.

## Guia complementar

Este README e o guia principal de navegacao e administracao inicial no Oracle Free / XE.

Antes de entrar em schemas, tablespaces, roles e objetos da IDE, existe uma duvida anterior que costuma travar o entendimento inicial:

- o que ja vem criado no Oracle Free / XE;
- por que `FREEPDB1` ja existe;
- o que `CREATE DATABASE` realmente faz;
- quando usar `SID` e quando usar `Service Name`;
- quando criar usuario e schema em vez de criar outro banco.

Essa linha de raciocinio comeca aqui no `README.md`, e o aprofundamento dessa duvida esta em [oracle_create_database_guide-v2.md](oracle_create_database_guide-v2.md).

Fluxo recomendado:

1. ler este `README.md` para entender a navegacao inicial na IDE;
2. abrir [oracle_create_database_guide-v2.md](oracle_create_database_guide-v2.md) para aprofundar `CDB`, `PDB`, `SID`, `Service Name` e `CREATE DATABASE`;
3. preparar o ambiente em [podman/README.md](../podman/README.md), porque este guia depende do Oracle ja estar rodando;
4. voltar para este guia e seguir a sequencia pratica de usuario, schema, tabela e consultas.

## 1. Tela de Conexao na IDE

Antes de entrar em schemas, tablespaces e objetos, o primeiro ponto de confusao costuma acontecer na propria tela de conexao da IDE.

Isso vale para:

- DBeaver;
- SQL Developer;
- CloudBeaver;
- outras IDEs e clientes SQL.

O objetivo desta parte e explicar cada campo da tela de conexao e o que ele significa no Oracle.

### 1.1 Exemplo do seu cenario

Em laboratorio, um exemplo comum fica assim:

```txt
Host: localhost
Port: 1522
Database: FREEPDB1
Connection Type: Service Name
User: system
Role: Normal
```

### 1.2 Significado de cada campo

| Campo | O que e | Exemplo |
| :--- | :--- | :--- |
| `Host` | Maquina onde o Oracle esta rodando | `localhost`, IP ou dominio |
| `Port` | Porta do listener Oracle | `1521`, `1522` |
| `Database` | Nome logico usado pela IDE conforme o tipo de conexao | `FREEPDB1` |
| `SID` | Identificador da instancia Oracle | `FREE` |
| `Service Name` | Nome do servico acessavel, geralmente a PDB | `FREEPDB1` |
| `Username` | Usuario Oracle | `system` |
| `Password` | Senha do usuario | sua senha |
| `Role` | Nivel de privilegio da sessao | `Normal`, `SYSDBA` |

### 1.3 SID vs Service Name

Essa diferenca e uma das mais importantes do Oracle.

**SID** significa, na pratica:

- a instancia Oracle;
- o motor principal;
- o nivel do container / CDB.

Exemplo:

```txt
FREE
```

**Service Name** significa, na pratica:

- o servico acessavel;
- o banco utilizavel dentro da instancia;
- normalmente a PDB em ambientes mais novos.

Exemplo:

```txt
FREEPDB1
```

Resumo visual:

```txt
Servidor fisico
 └── Oracle Instance (SID = FREE)
      └── Banco utilizavel (Service Name = FREEPDB1)
```

### 1.4 Quando usar SID

Use SID quando o contexto for:

- administracao raiz;
- `SYSDBA`;
- configuracao interna;
- acesso ao CDB;
- tarefas mais baixas de infraestrutura Oracle.

Exemplo:

```txt
Host: localhost
Port: 1522
SID: FREE
```

### 1.5 Quando usar Service Name

Use Service Name quando o contexto for:

- aplicacoes;
- desenvolvimento;
- usuarios comuns;
- tabelas de negocio;
- laboratorios com PDB.

Exemplo:

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
```

### 1.6 O campo `Database` na IDE

Em DBeaver e em outras IDEs, o campo `Database` nem sempre significa um banco fisico independente.

Ele representa o valor do tipo de conexao que voce escolheu:

- se a conexao estiver em modo `SID`, entao `Database = SID`;
- se a conexao estiver em modo `Service Name`, entao `Database = Service Name`.

Por isso, no Oracle:

- `Database` nao significa sempre a mesma coisa;
- o campo depende do tipo de conexao selecionado;
- a IDE simplifica a interface, mas o conceito correto continua sendo `SID` ou `Service Name`.

### 1.7 Exemplos visuais

Conexao por Service Name:

```txt
localhost:1522/FREEPDB1
```

Conexao por SID:

```txt
localhost:1522:FREE
```

### 1.8 String JDBC

Service Name:

```txt
jdbc:oracle:thin:@//localhost:1522/FREEPDB1
```

SID:

```txt
jdbc:oracle:thin:@localhost:1522:FREE
```

### 1.9 TNS / `tnsnames.ora`

Exemplo por Service Name:

```txt
FREEPDB1 =
 (DESCRIPTION =
   (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522))
   (CONNECT_DATA =
     (SERVICE_NAME = FREEPDB1)
   )
 )
```

### 1.10 Como descobrir no Oracle

Ver SID / instance name:

```sql
SELECT instance_name FROM v$instance;
```

Ver services:

```sql
SELECT name AS service_name
FROM v$services;
```

Ver container atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### 1.11 Seu cenario atual

| Elemento | Valor |
| :--- | :--- |
| `Host` | `localhost` |
| `Port` | `1522` |
| `SID` | `FREE` |
| `Service Name` | `FREEPDB1` |
| `User` | `SYSTEM` |
| `Role` | `Normal` |

### 1.12 `SYSDBA` vs `Normal`

| Role | Uso |
| :--- | :--- |
| `Normal` | Operacoes comuns |
| `SYSDBA` | Administracao total |

Regra pratica:

- para aplicacao, aula e tabelas de negocio, use `Normal`;
- para administracao de baixo nivel, use `SYSDBA` apenas quando realmente necessario.

### 1.13 Regra pratica para nao confundir

Se estiver em duvida:

- `SID` aponta para a instancia;
- `Service Name` aponta para o banco utilizavel;
- para laboratorio Free / XE moderno, quase sempre use `Service Name`;
- para trabalhar com tabela, usuario e schema, pense primeiro em `FREEPDB1`.

## 2. Visao Geral da Arquitetura Oracle

| Conceito | O que significa | Uso pratico |
| :--- | :--- | :--- |
| `Instance` | Processos e memoria do Oracle em execucao | Parte viva do banco |
| `CDB` | Container Database | Banco principal que abriga PDBs |
| `PDB` | Pluggable Database | Banco utilizavel para aplicacao e laboratorio |
| `User` | Conta de acesso | Quem autentica no banco |
| `Schema` | Conjunto de objetos de um usuario | Onde ficam tabelas, views, indices e sequences |
| `Tablespace` | Area logica de armazenamento | Onde os dados sao gravados |
| `Role` | Grupo de privilegios | Facilita concessao de permissoes |

Resumo mental:

```txt
Oracle Instance
 └── CDB
      └── PDB
           └── User
                └── Schema
                     ├── Tables
                     ├── Indexes
                     ├── Views
                     └── Other Objects
```

### 2.1 Arquitetura mental para nao se perder

Uma forma muito pratica de ler Oracle no inicio e esta:

```txt
Oracle Instance
 └── CDB (Container Database)
      └── PDB (Pluggable Database)
           └── User
                └── Schema
                     └── Tables
                          └── Data (Rows)
```

No ambiente de laboratorio do curso, isso costuma aparecer assim:

```txt
FREE
 └── FREEPDB1
      └── JEFF
           └── JEFF
                └── CHATGPT
```

Leitura correta:

- `FREE` representa a camada principal da infraestrutura Oracle;
- `FREEPDB1` representa o banco lógico de trabalho;
- `JEFF` como usuário cria automaticamente o schema `JEFF`;
- `CHATGPT` representa uma tabela criada dentro desse schema.

### 2.2 Regra fundamental de usuario e schema

Em Oracle, no fluxo comum de laboratório:

```txt
CREATE USER JEFF
=
USER JEFF + SCHEMA JEFF
```

Isso significa que, ao criar um usuário, também nasce um schema com o mesmo nome.

Se a sessão estiver conectada como `JEFF` e for executado:

```sql
CREATE TABLE chatgpt (
  id NUMBER PRIMARY KEY,
  pergunta VARCHAR2(4000)
);
```

o resultado lógico será:

```txt
JEFF.CHATGPT
```

### 2.3 FREE e FREEPDB1 em linguagem direta

Use esta regra mental:

```txt
FREE = infraestrutura principal
FREEPDB1 = banco lógico de desenvolvimento
```

Em outras palavras:

- `FREE` é a camada principal do Oracle;
- `FREEPDB1` é o banco lógico real onde a maior parte do laboratório acontece.

Por isso, em ambiente de desenvolvimento, a regra prática é:

- conectar na `FREEPDB1`;
- criar usuário;
- criar tabela;
- consultar dados.

### 2.4 Múltiplos projetos dentro da mesma PDB

Também é útil visualizar que uma única PDB pode concentrar vários usuários, schemas e tabelas:

```txt
FREE
 └── FREEPDB1
      ├── JEFF
      │    └── CHATGPT
      ├── ERP
      │    └── CLIENTES
      └── CRM
           └── LEADS
```

Isso ajuda a fixar a ideia de que:

- `FREEPDB1` é o banco lógico compartilhado do ambiente;
- cada usuário trabalha no próprio schema;
- as tabelas ficam organizadas por schema, não todas misturadas no mesmo espaço lógico.

### 2.5 Fisico vs logico

Outra confusão comum no início é misturar a camada lógica com a camada física.

Visão lógica:

```txt
FREEPDB1 -> JEFF -> CHATGPT
```

Visão física:

```txt
users01.dbf
```

Leitura prática:

- `PDB`, `schema` e `table` pertencem à camada lógica;
- `datafile` pertence à camada física do Oracle.

### 2.6 Hierarquia interna de armazenamento

Uma forma simples de explicar a camada física interna:

```txt
Datafile (.dbf)
 └── Tablespace
      └── Segment
           └── Extent
                └── Block
                     └── Rows
```

Isso ajuda a entender que:

- a tabela é um objeto lógico;
- mas os dados acabam persistidos em estruturas físicas do banco.

### 2.7 Exemplo completo

```txt
/opt/oracle/oradata/FREE/FREEPDB1/users01.dbf
 └── USERS tablespace
      └── JEFF schema
           └── CHATGPT table
                └── Registros
```

Esse tipo de leitura é importante porque conecta:

- a IDE;
- a query;
- a arquitetura Oracle;
- e a forma como o dado realmente fica armazenado.

### 2.8 SID, Service Name e a regra de conexao

No laboratório, vale manter esta leitura curta:

```txt
SID = FREE
Service Name = FREEPDB1
```

Regra prática:

- `SID` aponta para a instância;
- `Service Name` aponta para o banco lógico utilizável;
- para desenvolvimento, tabelas e queries de negócio, o caminho principal é `FREEPDB1`.

### 2.9 Onde entra CREATE PLUGGABLE DATABASE

Outro ponto importante: em Oracle, existem duas ideias diferentes que costumam ser confundidas no início.

Fluxo comum de desenvolvimento:

- criar usuário;
- conceder privilégios;
- criar tabela;
- inserir e consultar dados.

Fluxo avançado de arquitetura:

```sql
CREATE PLUGGABLE DATABASE vendas;
```

Esse comando cria outra `PDB`, por exemplo:

```txt
FREE
 ├── FREEPDB1
 └── VENDAS
```

Ou seja:

- `CREATE USER` cria identidade de acesso e schema;
- `CREATE PLUGGABLE DATABASE` cria outro banco lógico dentro do container;
- para o início do curso, o fluxo certo continua sendo `FREEPDB1 -> user/schema -> table -> query`.

## 3. Seu Ambiente de Laboratorio

Neste curso, o ambiente mais comum e:

```txt
Host: localhost
Port: 1522
PDB / Service Name: FREEPDB1
```

Isso significa:

- o Oracle esta escutando na porta `1522`;
- a PDB principal do laboratorio e `FREEPDB1`;
- a maior parte do trabalho acontece dentro dessa PDB;
- em Free / XE, o fluxo normal nao e criar um banco do zero, e sim criar usuarios e objetos dentro da PDB existente.

Antes de seguir na IDE, vale preparar o ambiente em [podman/README.md](../podman/README.md), porque sem Oracle rodando este guia perde boa parte do contexto pratico.

Se surgir a duvida "quem criou o `FREEPDB1`?" ou "por que nao comecamos com `CREATE DATABASE`?", aprofunde aqui: [oracle_create_database_guide-v2.md](oracle_create_database_guide-v2.md).

## 4. O Que A IDE Mostra Quando Voce Expande a Conexao

Ao abrir a conexao na IDE, normalmente aparecem areas como:

- schemas / users;
- tablespaces;
- roles;
- views;
- procedures;
- types;
- sequences;
- synonyms;
- links;
- recycle bin;
- metadata global.

No primeiro contato, isso assusta. Mas a leitura correta e:

- uma parte e administrativa e interna do Oracle;
- outra parte e area de trabalho da aplicacao;
- nao e necessario dominar tudo de uma vez;
- o caminho certo e entender primeiro usuario, schema, tabela e consulta.

## 5. Schemas Importantes Que Aparecem na IDE

Ao listar usuarios ou schemas, voce vai encontrar nomes como estes.

### 5.1 Schemas de sistema e componentes internos

| Schema | Resumo pratico |
| :--- | :--- |
| `ANONYMOUS` | Servicos HTTP/XML |
| `APPQOSSYS` | Quality of Service |
| `AUDSYS` | Auditoria |
| `BAASSYS` | Oracle Audit Vault / seguranca |
| `DBSFWUSER` | Firewall / seguranca |
| `DGPDB_INT` | Data Guard interno |
| `DIP` | Directory Integration |
| `DVF` | Database Vault Functions |
| `DVSYS` | Database Vault |
| `GGSHAREDCAP` | GoldenGate |
| `GGSYS` | GoldenGate Admin |
| `GSMADMIN_INTERNAL` | Global Service Manager |
| `GSMCATUSER` | Catalogo GSM |
| `GSMUSER` | GSM |
| `LBACSYS` | Label Security |
| `OJVMSYS` | Java VM |
| `PDBADMIN` | Administrador da PDB |
| `REMOTE_SCHEDULER_AGENT` | Scheduler remoto |
| `SYS$UMF` | Unified Model Framework |
| `SYSBACKUP` | Backup |
| `SYSDG` | Data Guard |
| `SYSKM` | Key Management |
| `SYSRAC` | RAC |
| `VECSYS` | Vetores / IA |
| `XS$NULL` | Seguranca |

Leitura correta:

- esses schemas existem para administracao, seguranca, HA, replicacao, auditoria e componentes do Oracle;
- normalmente nao faz sentido criar tabela de aplicacao neles;
- para aplicacao e laboratorio, o certo e usar `PDBADMIN` ou criar um usuario proprio.

### 5.2 Principais schemas de administracao

| Schema | Funcao |
| :--- | :--- |
| `SYS` | Administracao interna principal |
| `SYSTEM` | Administracao secundaria |
| `PDBADMIN` | Administrador da PDB |
| `XDB` | XML Database |
| `OUTLN` | Otimizador |
| `DBSNMP` | Monitoramento |

Regras praticas:

- nao use `SYS` para aplicacao;
- evite criar tabelas de negocio em `SYSTEM`;
- prefira criar um usuario dedicado;
- em laboratorio, `PDBADMIN` pode ser usado para administracao da PDB.

### 5.3 Consultar usuarios no banco

```sql
SELECT username, account_status, default_tablespace
FROM dba_users
ORDER BY username;
```

## 6. User e Schema: No Oracle Eles Andam Juntos

Em Oracle, quando voce cria um usuario, voce cria tambem um schema com o mesmo nome.

Exemplo:

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;
```

Depois disso:

- o usuario `jeff` passa a existir;
- o schema `jeff` passa a existir;
- tudo o que `jeff` criar ficara no schema `jeff`.

Essa e uma diferenca importante em relacao a outros bancos em que schema e database podem ser conceitos separados.

## 7. Global Metadata: O Que E Isso Na IDE?

Muitas IDEs mostram uma area global ou administrativa com objetos compartilhados. Alguns itens comuns:

| Item | Funcao |
| :--- | :--- |
| `Types` | Tipos de dados e tipos de objeto |
| `Public Synonyms` | Aliases publicos para objetos |
| `Public Database Links` | Links para outros bancos |
| `User Recycle Bin` | Lixeira de objetos removidos |

No primeiro momento:

- `Types` vale conhecer;
- `Synonyms` e `DB Links` sao mais administrativos;
- `Recycle Bin` ajuda a entender recuperacao de objetos apagados.

## 8. Types: O Que Sao e Por Que Aparecem

Quando a IDE mostra `Types`, o que aparece ali sao tipos nativos ou definidos no banco.

### 8.1 Exemplos de tipos e leitura pratica

| Tipo | Uso |
| :--- | :--- |
| `BLOB` | Binario grande |
| `DECIMAL` | Numero decimal |
| `RAW` | Binario bruto |
| `TIME WITH TZ` | Hora com fuso |
| `TABLE` | Tipo tabela |
| `TIMESTAMP WITH TIME ZONE` | Timestamp com fuso |
| `LONG RAW` | Binario legado |
| `UROWID` | Endereco universal de linha |
| `INTERVAL YEAR TO MONTH` | Intervalo |
| `NAMED COLLECTION` | Colecao |
| `TIMESTAMP` | Data e hora |
| `INTEGER` | Inteiro |
| `NCLOB` | Texto Unicode grande |
| `NUMBER` | Numero generico |
| `OID` | Object ID |
| `VARCHAR2` | Texto principal no Oracle |
| `BOOLEAN` | Booleano |
| `INTERVAL DAY TO SECOND` | Intervalo |
| `DATE` | Data |
| `REAL` | Numero real |
| `VARCHAR` | Texto |
| `TIMESTAMP WITH LOCAL TZ` | Timestamp local |
| `BINARY_DOUBLE` | Double precision |

### 8.2 Quais tipos usar primeiro

Para comecar, quase sempre basta dominar:

- `NUMBER`
- `VARCHAR2`
- `DATE`
- `TIMESTAMP`
- `CLOB` ou `NCLOB` quando houver texto grande

Exemplo simples:

```sql
CREATE TABLE products (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(120) NOT NULL,
    preco NUMBER(10,2),
    criado_em DATE DEFAULT SYSDATE
);
```

## 9. Storage e Tablespaces

Quando `Storage` ou `Tablespaces` aparecem na IDE, o que se ve ali e a organizacao logica onde os objetos sao armazenados.

### 9.1 Tablespaces mais comuns

| Tablespace | Funcao |
| :--- | :--- |
| `SYSTEM` | Dicionario principal do Oracle |
| `SYSAUX` | Componentes auxiliares e metadados adicionais |
| `USERS` | Dados de usuarios comuns |
| `TEMP` | Operacoes temporarias |
| `UNDOTBS1` | Undo / rollback |

### 9.2 Exemplo de leitura de storage

No ambiente atual, voce pode ver algo como:

| Tablespace | Tamanho | Funcao |
| :--- | :--- | :--- |
| `SYSAUX` | `338M` | Metadados auxiliares |
| `SYSTEM` | `283M` | Core do Oracle |
| `TEMP` | variavel | Operacoes temporarias |

### 9.3 Consultar tablespaces

```sql
SELECT tablespace_name, status, contents
FROM dba_tablespaces;
```

Leitura correta:

- `SYSTEM` e `SYSAUX` nao sao para tabela de aplicacao;
- `USERS` costuma ser o tablespace padrao para laboratorio;
- `TEMP` atende sorts, joins e operacoes temporarias;
- `UNDO` ajuda a manter consistencia e rollback.

## 10. Roles Importantes

As `roles` agrupam privilegios.

| Role | Uso |
| :--- | :--- |
| `DBA` | Controle total |
| `CONNECT` | Conexao basica |
| `RESOURCE` | Criacao de objetos |
| `CDB_DBA` | Administracao do container |

Consultar:

```sql
SELECT role
FROM dba_roles
ORDER BY role;
```

## 11. Ordem Correta de Aprendizado no Laboratorio

Para nao se perder na IDE, a sequencia recomendada e:

1. Conectar na PDB correta.
2. Entender qual usuario esta usando.
3. Entender que user e schema andam juntos no Oracle.
4. Ver tablespaces e roles principais.
5. Criar um usuario proprio.
6. Conceder privilegios.
7. Entrar com esse usuario.
8. Criar tabela.
9. Inserir dados.
10. Consultar.
11. Atualizar.
12. Deletar.
13. Criar indice.
14. Ver objetos do schema.
15. Remover objetos quando necessario.

## 12. Criar Usuario de Laboratorio

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;
```

Dar privilegios minimos para laboratorio:

```sql
GRANT CONNECT, RESOURCE TO jeff;
```

Dar `DBA` apenas em ambiente de teste:

```sql
GRANT DBA TO jeff;
```

## 13. Testar Login

```sql
CONNECT jeff/StrongPass123@localhost:1522/FREEPDB1
```

Ou na IDE:

- Host: `localhost`
- Port: `1522`
- Service Name: `FREEPDB1`
- User: `jeff`
- Password: `StrongPass123`

## 14. Criar Tabela

```sql
CREATE TABLE clients (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    email VARCHAR2(150),
    created_at DATE DEFAULT SYSDATE
);
```

Leitura pratica:

- a tabela sera criada no schema do usuario conectado;
- se o usuario conectado for `jeff`, a tabela sera `jeff.clients`;
- a IDE normalmente mostrara isso em `Schemas > JEFF > Tables`.

## 15. Inserir Dados

```sql
INSERT INTO clients (name, email)
VALUES ('Jefferson', 'jeff@email.com');

INSERT INTO clients (name, email)
VALUES ('Arthur', 'arthur@email.com');

COMMIT;
```

## 16. Consultar Dados

Todos:

```sql
SELECT * FROM clients;
```

Ordenado:

```sql
SELECT id, name, email
FROM clients
ORDER BY id DESC;
```

Com filtro:

```sql
SELECT *
FROM clients
WHERE name LIKE 'J%';
```

## 17. Atualizar e Deletar

```sql
UPDATE clients
SET email = 'novo@email.com'
WHERE id = 1;

DELETE FROM clients
WHERE id = 2;

COMMIT;
```

## 18. Ver Objetos do Seu Schema

Tabelas do usuario atual:

```sql
SELECT table_name
FROM user_tables;
```

Objetos do schema:

```sql
SELECT object_name, object_type
FROM user_objects;
```

Sessao atual:

```sql
SELECT username
FROM user_users;
```

Isso ajuda a conectar a IDE com o SQL:

- o que aparece em `Tables` geralmente vem de `USER_TABLES`;
- o que aparece em `Views`, `Indexes`, `Sequences` e outros agrupamentos aparece em `USER_OBJECTS`.

## 19. Criar Indice

```sql
CREATE INDEX idx_clients_email
ON clients(email);
```

Uso pratico:

- acelerar busca por coluna muito consultada;
- melhorar leitura em alguns cenarios;
- evitar criar indice sem criterio, porque escrita tambem tem custo.

## 20. Drop de Objetos

```sql
DROP TABLE clients;
DROP USER jeff CASCADE;
```

Leitura pratica:

- `DROP TABLE` remove a tabela;
- `DROP USER ... CASCADE` remove o usuario e todos os objetos do schema.

## 21. Sobre `CREATE DATABASE`

No Oracle Free / XE via container, o banco normalmente ja vem pre-criado.

Ambiente comum:

- CDB: `FREE`
- PDB: `FREEPDB1`

Por isso, no laboratorio, o fluxo correto normalmente e:

1. usar a PDB existente;
2. criar usuario;
3. criar schema automaticamente via usuario;
4. criar tabela e objetos.

Em Oracle tradicional de instalacao manual, existe `CREATE DATABASE`, por exemplo:

```sql
CREATE DATABASE mydb;
```

Mas esse nao e o fluxo principal em Free / XE de laboratorio.

## 22. Diagnostico Rapido

Ver PDB atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

Listar PDBs:

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status
FROM v$pdbs
ORDER BY con_id;
```

Trocar para a PDB correta:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

Ver nome do banco e do container atual:

```sql
SELECT
  SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name,
  SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 23. Boas Praticas

- nunca use `SYS` para aplicacao;
- use `PDBADMIN` ou usuario dedicado;
- separe tabelas por schema;
- controle quota e privilegios;
- use indices com criterio;
- execute `COMMIT` conscientemente;
- entenda primeiro schema, tabela e dados antes de explorar objetos avancados da IDE.

## 24. Exercicios Recomendados

1. Listar usuarios do banco.
2. Identificar `SYS`, `SYSTEM` e `PDBADMIN`.
3. Consultar tablespaces.
4. Criar usuario proprio.
5. Dar privilegios.
6. Conectar com o novo usuario.
7. Criar tabela.
8. Inserir dados.
9. Consultar.
10. Atualizar.
11. Deletar.
12. Criar indice.
13. Ver objetos do schema.
14. Dropar tabela e usuario.

## 25. Atalho Mental Final

Quando abrir a IDE, pense assim:

```txt
1. Onde estou? -> PDB
2. Com quem estou? -> User
3. O que posso criar? -> Schema Objects
4. Onde isso fica? -> Tablespace
5. Que permissoes tenho? -> Roles / Grants
```

Quando essa sequencia fica clara, fica muito mais facil se orientar dentro do Oracle Free / XE e entender o que a IDE esta mostrando.
