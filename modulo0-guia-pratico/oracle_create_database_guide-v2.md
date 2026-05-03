# Oracle Free / XE - Entendendo `CREATE DATABASE`, `CDB`, `PDB`, `SID` e `Service Name`

Este guia existe para resolver uma confusao muito comum no inicio:

- o que ja vem criado no Oracle Free / XE;
- o que significa `CREATE DATABASE`;
- quando usar `CDB`, `PDB`, `SID` e `Service Name`;
- quando criar um banco novo;
- quando criar apenas usuario, schema e tabelas.

O foco aqui e laboratorio com Oracle Free / XE, especialmente em ambiente com container.

## 1. Resposta Direta

No Oracle Free / XE moderno, voce normalmente **nao comeca com**:

```sql
CREATE DATABASE
```

Voce normalmente comeca com:

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123;
```

Depois:

```sql
GRANT CONNECT, RESOURCE TO jeff;
```

E entao cria tabelas dentro da PDB de trabalho.

## 2. O que ja vem pronto no Oracle Free / XE

Em um laboratorio tipico, a propria instalacao ou imagem do Oracle cria automaticamente:

```txt
CDB = FREE
PDB = FREEPDB1
```

Em termos práticos:

- `FREE` e o container principal;
- `FREEPDB1` e o banco onde a aplicacao e o laboratorio normalmente trabalham;
- `SYS`, `SYSTEM` e `PDBADMIN` ja existem;
- o aluno nao precisa montar toda a estrutura do zero para comecar.

Resumo visual:

```txt
Servidor / Container
 └── Oracle Instance
      └── CDB (FREE)
           └── PDB (FREEPDB1)
                ├── SYS
                ├── SYSTEM
                ├── PDBADMIN
                └── Users / Schemas / Tables
```

## 3. Conceitos que mais confundem

| Conceito | O que significa | Exemplo pratico |
| :--- | :--- | :--- |
| `SID` | Identificador da instancia Oracle | `FREE` |
| `CDB` | Container principal | `FREE` |
| `PDB` | Banco utilizavel para a aplicacao | `FREEPDB1` |
| `Service Name` | Nome de conexao exposto pelo listener | `FREEPDB1` |
| `User` | Conta de acesso | `SYSTEM`, `JEFF` |
| `Schema` | Conjunto de objetos do usuario | tabelas, views e indices do usuario |

Regra pratica:

- `SID` aponta para a instancia;
- `Service Name` aponta para o banco utilizavel;
- em Free / XE, a conexao de aplicacao normalmente usa `FREEPDB1`.

## 4. Oracle antigo vs Oracle moderno

### Oracle antigo

```txt
1 instalacao = 1 banco principal
```

### Oracle moderno com multitenant

```txt
1 instalacao = 1 CDB + 1 ou mais PDBs
```

Por isso a pergunta "eu preciso criar o banco?" mudou bastante no Oracle moderno.

### 4.1 Leitura mental de multitenant

No Oracle moderno, vale guardar esta estrutura:

```txt
Oracle Instance
 └── CDB
      └── PDB
           └── USER
                └── SCHEMA
                     └── TABLES
```

No laboratório:

```txt
FREE
 └── FREEPDB1
```

Resumo direto:

- `CDB` é o container principal;
- `PDB` é o banco lógico utilizável;
- `schema` não é a mesma coisa que `PDB`;
- `Service Name` normalmente aponta para a `PDB`.

## 5. O que `CREATE DATABASE` realmente faz

O comando tradicional:

```sql
CREATE DATABASE mydb;
```

cria uma base Oracle a partir do zero, incluindo itens como:

- control files;
- datafiles;
- redo logs;
- tablespaces centrais, como `SYSTEM` e `SYSAUX`;
- estrutura interna minima do banco.

Esse comando faz sentido em contexto de:

- instalacao manual;
- administracao avancada;
- infraestrutura enterprise;
- laboratorios especificos de DBA.

Nao e o fluxo principal do aluno que esta aprendendo Oracle Free / XE para desenvolvimento.

## 6. O que voce faz no laboratorio

No laboratorio, o fluxo normal e este:

```txt
Entrar na PDB correta
   └── Criar usuario
         └── Ganhar privilegios
               └── Criar tabela
                     └── Inserir e consultar dados
```

Ou seja:

- nao criar outro banco raiz;
- nao reconstruir a base inteira;
- trabalhar dentro do `FREEPDB1`.

## 7. Como validar onde voce esta

### 7.1 Ver o container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### 7.2 Ver a instancia Oracle

```sql
SELECT instance_name AS instance_name
FROM v$instance;
```

### 7.3 Ver o banco principal

```sql
SELECT name AS database_name
FROM v$database;
```

### 7.4 Ver as PDBs disponiveis

```sql
SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status
FROM v$pdbs
ORDER BY con_id;
```

### 7.5 Ler o resultado corretamente

Em um cenario comum:

| Elemento | Valor |
| :--- | :--- |
| `SID` | `FREE` |
| `CDB` | `FREE` |
| `PDB` | `FREEPDB1` |
| `Service Name` | `FREEPDB1` |

Interpretacao:

- a instancia e `FREE`;
- o banco de trabalho e `FREEPDB1`;
- aplicacao, IDE e laboratorio devem mirar na PDB.

## 8. Como conectar corretamente

### 8.1 Conexao de aplicacao ou laboratorio

Exemplo de leitura mental:

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: system
Role: Normal
```

Exemplo JDBC:

```txt
jdbc:oracle:thin:@//localhost:1522/FREEPDB1
```

### 8.2 Quando `SID` entra na historia

O `SID` aparece mais em:

- administracao de baixo nivel;
- conexao ao CDB raiz;
- operacoes mais internas;
- contexto `SYSDBA`.

Exemplo mental:

```txt
localhost:1522:FREE
```

Para o aluno iniciante, a conexao correta quase sempre sera por `Service Name`.

## 9. Sequencia correta para aprender

### 9.1 Primeiro

- entender `SID` vs `Service Name`;
- entender `CDB` vs `PDB`;
- saber que `FREEPDB1` ja existe;
- saber em qual banco esta conectado.

### 9.2 Depois

- criar um usuario;
- conceder privilegios;
- criar tabela;
- inserir dados;
- consultar dados.

### 9.3 Mais adiante

- criar nova PDB;
- administrar CDB;
- estudar tablespaces;
- estudar backup, recovery e HA.

## 10. Exemplo pratico completo

### 10.1 Criar usuario

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON users;
```

### 10.2 Conceder privilegios

Laboratorio simples:

```sql
GRANT CONNECT, RESOURCE TO jeff;
```

Laboratorio administrativo:

```sql
GRANT DBA TO jeff;
```

### 10.3 Conectar com o usuario

Exemplo em SQL*Plus:

```txt
CONNECT jeff/StrongPass123@localhost:1522/FREEPDB1
```

Exemplo em IDE:

```txt
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: jeff
Password: StrongPass123
Role: Normal
```

### 10.4 Criar tabela

```sql
CREATE TABLE clients (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(150),
    created_at DATE DEFAULT SYSDATE
);
```

### 10.5 Inserir dados

```sql
INSERT INTO clients (name, email)
VALUES ('Jefferson', 'jeff@email.com');

INSERT INTO clients (name, email)
VALUES ('Arthur', 'arthur@email.com');

COMMIT;
```

### 10.6 Consultar

```sql
SELECT id,
       name,
       email,
       created_at
FROM clients
ORDER BY id;
```

## 11. O que significa "criar schema" no Oracle

Em Oracle, ao criar um usuario, voce cria automaticamente um schema com o mesmo nome.

Se voce executa:

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123;
```

entao passa a existir:

- usuario `JEFF`;
- schema `JEFF`.

Se o usuario `JEFF` cria a tabela `CLIENTS`, o objeto fica logicamente em:

```txt
JEFF.CLIENTS
```

Por isso, no laboratorio, "criar schema" normalmente significa:

- criar usuario;
- conceder privilegios;
- conectar com ele;
- criar objetos.

## 12. E quando faz sentido criar uma nova PDB

Esse passo e avancado. Exemplo:

```sql
CREATE PLUGGABLE DATABASE vendas
ADMIN USER vendas_admin IDENTIFIED BY StrongPass123
FILE_NAME_CONVERT = ('pdbseed', 'vendas');
```

Depois:

```sql
ALTER PLUGGABLE DATABASE vendas OPEN;
```

Esse fluxo faz mais sentido quando voce quer:

- separar ambientes;
- isolar um conjunto de aplicacoes;
- estudar multitenant de forma administrativa.

Nao e o primeiro passo para quem so quer criar tabelas e testar consultas.

## 13. Erros comuns no inicio

| Erro | Causa comum | Leitura pratica |
| :--- | :--- | :--- |
| `ORA-12505` | `SID` incorreto | tentou conectar na instancia errada |
| `ORA-12514` | `Service Name` incorreto | tentou conectar em servico inexistente |
| `ORA-01017` | usuario ou senha incorretos | credencial invalida |
| `ORA-00900` | comando nao SQL | usou comando de cliente como se fosse SQL |

O ultimo ponto e importante:

- `SHOW PDBS` e comando de cliente SQL*Plus / SQLcl;
- `SELECT ... FROM v$pdbs` e SQL Oracle propriamente dito.

## 14. Regra profissional

Se voce quer:

- trabalhar com tabela, dado e aplicacao -> use `FREEPDB1`;
- administrar a raiz Oracle -> pense em `FREE` / `CDB$ROOT`;
- aprender Oracle no inicio -> comece por usuario, schema e tabela;
- aprender infraestrutura Oracle -> depois avance para PDB, CDB e parametros.

## 15. Resumo mental final

```txt
FREE = motor principal Oracle (CDB / SID)
FREEPDB1 = banco padrao de trabalho (PDB / Service Name)
JEFF = seu usuario e seu schema de trabalho
```

## 16. Consultas praticas para repetir em aula

```sql
SELECT name AS database_name
FROM v$database;

SELECT instance_name AS instance_name
FROM v$instance;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id AS pdb_id,
       name AS pdb_name,
       open_mode AS status
FROM v$pdbs
ORDER BY con_id;
```

## 17. Conclusao

No Oracle Free / XE, o raciocinio inicial correto e:

1. entender a conexao;
2. entrar na PDB certa;
3. criar usuario;
4. criar tabela;
5. inserir e consultar.

O raciocinio incorreto para o inicio e:

1. tentar criar a base inteira do zero;
2. confundir `SID` com `Service Name`;
3. achar que `CREATE DATABASE` e sempre o primeiro passo.
