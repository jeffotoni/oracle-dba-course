# Aula 4 - Módulo 3: CLI, carga e backup lógico no Oracle

Esta aula é um laboratório prático para executar operações do Oracle pela linha de comando. O fluxo usa `Podman`, `SQL*Plus`, `SQL*Loader`, `expdp` e `impdp`.

```text
Podman
  -> container Oracle
      -> SQL*Plus
          -> criar tabela e carregar dados
              -> SQL*Loader
                  -> expdp
                      -> remover objetos
                          -> impdp
                              -> validar restauração
```

## Objetivo

Ao terminar a prática, deve ser possível:

- entrar no container Oracle com Podman;
- localizar e executar os binários nativos do Oracle;
- executar um arquivo `.sql` pelo `SQL*Plus`;
- carregar um arquivo CSV com o `SQL*Loader`;
- exportar tabelas para um dump lógico com `expdp`;
- remover as tabelas do laboratório;
- importar o dump com `impdp`;
- validar se os dados foram restaurados.

## Escopo da aula

Esta é uma aula de prática de CLI e backup lógico. Para manter a sequência objetiva, não entram neste laboratório:

- criação de usuários, perfis e roles;
- auditoria;
- ORDS;
- RMAN;
- backup físico e recuperação de datafiles;
- tuning e monitoramento avançado.

O usuário `SYSTEM` será usado para reduzir a quantidade de preparação. Essa escolha serve apenas para o laboratório. Em um ambiente real, tabelas de aplicação não devem ser criadas no schema `SYSTEM`.

## 1. Preparar o Oracle com Podman

O laboratório usa o mesmo container adotado nas aulas anteriores:

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

Se o container já foi criado, não execute novamente o `run`:

```bash
podman start oracle-free-full-23ai
```

Valide o container:

```bash
podman ps
podman logs --tail 40 oracle-free-full-23ai
```

Parâmetros usados no laboratório:

```text
Container: oracle-free-full-23ai
Host externo: localhost
Porta externa: 1522
Porta interna: 1521
Service Name: FREEPDB1
Usuário: SYSTEM
Senha: OraclePwd123
```

Dentro do container, os binários usam a porta interna `1521`. A porta `1522` é utilizada somente quando a conexão parte do host.

## 2. Confirmar os binários nativos

O `SQL*Plus` executa scripts e consultas SQL. O `SQL*Loader` carrega arquivos externos, como CSV. O `expdp` exporta dados e metadados em um dump lógico. O `impdp` importa esse dump.

Execute no host:

```bash
podman exec -it oracle-free-full-23ai bash
```

Dentro do container:

```bash
command -v sqlplus
command -v sqlldr
command -v expdp
command -v impdp
```

Valide as versões e a ajuda:

```bash
sqlplus -v
sqlldr -help | head
expdp help=y | head
impdp help=y | head
```

O resultado deve mostrar os caminhos dos binários e as versões instaladas na imagem Oracle. Nesta aula, os quatro comandos serão executados dentro do container.

Saia para o host antes de copiar os arquivos:

```bash
exit
```

## 3. Copiar os arquivos do laboratório

Execute os comandos a partir da raiz do repositório:

```bash
podman exec oracle-free-full-23ai mkdir -p /opt/oracle/labdata/dpump
podman cp novos-modulos-enxutos/aula-4-modulo3/produtos-500.sql oracle-free-full-23ai:/opt/oracle/labdata/produtos-500.sql
podman cp novos-modulos-enxutos/aula-4-modulo3/produtos.csv oracle-free-full-23ai:/opt/oracle/labdata/produtos.csv
podman cp novos-modulos-enxutos/aula-4-modulo3/produtos.ctl oracle-free-full-23ai:/opt/oracle/labdata/produtos.ctl
```

Confirme os arquivos:

```bash
podman exec oracle-free-full-23ai ls -lah /opt/oracle/labdata
```

O arquivo `produtos-500.sql` cria as tabelas do laboratório e executa 500 inserts. O arquivo `produtos.csv` será usado pelo `SQL*Loader`. O arquivo `produtos.ctl` explica ao `SQL*Loader` como interpretar o CSV.

## 4. Executar o SQL pelo SQL*Plus

Entre no container:

```bash
podman exec -it oracle-free-full-23ai bash
```

Conecte no PDB como `SYSTEM`:

```bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

O formato da conexão é:

```text
sqlplus usuario/senha@//host:porta/service_name
```

Como estamos dentro do container, usamos `localhost:1521`. A conexão pela IDE no host usaria `localhost:1522`.

No prompt `SQL>`, execute o arquivo:

```sql
@/opt/oracle/labdata/produtos-500.sql
```

O caractere `@` instrui o `SQL*Plus` a ler e executar um arquivo SQL. O script cria:

- `SYSTEM.PRODUTOS`, tabela principal preenchida pelo arquivo SQL;
- `SYSTEM.PRODUTOS_CARGA`, tabela destinada ao `SQL*Loader`.

Também é possível executar o mesmo arquivo sem entrar no prompt interativo:

```bash
sqlplus -s system/OraclePwd123@//localhost:1521/FREEPDB1 @/opt/oracle/labdata/produtos-500.sql
```

O script encerra a sessão ao final com `EXIT`.

## 5. Validar os 500 registros

Ainda dentro do container, abra o `SQL*Plus`:

```bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1
```

Execute:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

```sql
SELECT COUNT(*) AS total_produtos
FROM produtos;
```

```sql
SELECT id_produto,
       nome_produto,
       categoria,
       preco
FROM produtos
ORDER BY id_produto
FETCH FIRST 10 ROWS ONLY;
```

O total esperado em `PRODUTOS` é `500`.

## 6. Carregar CSV com SQL*Loader

O `SQL*Loader` não executa um arquivo `.sql`. Ele lê um arquivo de dados, neste caso `produtos.csv`, e utiliza o arquivo `produtos.ctl` para saber:

- qual tabela receberá os dados;
- qual separador existe entre os campos;
- quais colunas serão preenchidas;
- onde registrar o log, erros e rejeições.

O control file desta aula usa a tabela `PRODUTOS_CARGA` e a opção `TRUNCATE`, permitindo repetir a carga sem acumular registros duplicados.

Saia do `SQL*Plus`:

```sql
EXIT;
```

Execute o binário:

```bash
sqlldr system/OraclePwd123@//localhost:1521/FREEPDB1 \
  control=/opt/oracle/labdata/produtos.ctl \
  log=/opt/oracle/labdata/produtos_sqlldr.log \
  bad=/opt/oracle/labdata/produtos_sqlldr.bad \
  discard=/opt/oracle/labdata/produtos_sqlldr.dsc
```

Leia o log:

```bash
cat /opt/oracle/labdata/produtos_sqlldr.log
```

Valide a carga:

```bash
sqlplus -s system/OraclePwd123@//localhost:1521/FREEPDB1 <<'SQL'
SET PAGESIZE 50
SET LINESIZE 160
SELECT COUNT(*) AS total_produtos_carga
FROM produtos_carga;

SELECT id_produto,
       nome_produto,
       categoria,
       preco
FROM produtos_carga
ORDER BY id_produto
FETCH FIRST 10 ROWS ONLY;

EXIT;
SQL
```

O total esperado em `PRODUTOS_CARGA` também é `500`.

## 7. Preparar o diretório do Data Pump

O Data Pump grava o dump no filesystem do container. Primeiro, confirme que o diretório físico existe:

```bash
mkdir -p /opt/oracle/labdata/dpump
```

Esse comando deve ser executado dentro do container. Se você ainda estiver no host, use:

```bash
podman exec oracle-free-full-23ai mkdir -p /opt/oracle/labdata/dpump
```

Agora crie o objeto `DIRECTORY` no Oracle. O objeto é criado no banco, mas aponta para um caminho físico dentro do container.

```bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1 <<'SQL'
CREATE OR REPLACE DIRECTORY dpump_dir AS '/opt/oracle/labdata/dpump';

SELECT directory_name,
       directory_path
FROM dba_directories
WHERE directory_name = 'DPUMP_DIR';

EXIT;
SQL
```

Como `SYSTEM` é o proprietário do objeto `DPUMP_DIR` e também executará o Data Pump, não é necessário criar outro usuário ou schema para esta prática.

## 8. Exportar as tabelas com expdp

O `expdp` faz um backup lógico. Ele exporta objetos, metadados e dados em um arquivo `.dmp`. Não é um backup físico do banco e não substitui o `RMAN`.

Execute dentro do container:

```bash
expdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=DPUMP_DIR \
  DUMPFILE=produtos_lab.dmp \
  LOGFILE=produtos_lab_exp.log \
  TABLES=SYSTEM.PRODUTOS,SYSTEM.PRODUTOS_CARGA
```

Valide os arquivos criados:

```bash
ls -lah /opt/oracle/labdata/dpump
cat /opt/oracle/labdata/dpump/produtos_lab_exp.log
```

No host, a mesma validação pode ser feita com:

```bash
podman exec oracle-free-full-23ai ls -lah /opt/oracle/labdata/dpump
podman exec oracle-free-full-23ai cat /opt/oracle/labdata/dpump/produtos_lab_exp.log
```

O arquivo `produtos_lab.dmp` é o dump lógico. O arquivo `.log` registra o resultado da exportação.

## 9. Remover as tabelas para simular uma perda lógica

Antes de importar, remova as tabelas do laboratório:

```bash
sqlplus system/OraclePwd123@//localhost:1521/FREEPDB1 <<'SQL'
DROP TABLE produtos_carga PURGE;
DROP TABLE produtos PURGE;

SELECT table_name
FROM user_tables
WHERE table_name IN ('PRODUTOS', 'PRODUTOS_CARGA')
ORDER BY table_name;

EXIT;
SQL
```

O `SELECT` não deve retornar as duas tabelas. O dump continua preservado em `/opt/oracle/labdata/dpump`.

## 10. Importar as tabelas com impdp

O `impdp` lê o dump lógico e recria os objetos e dados no Oracle.

Execute:

```bash
impdp system/OraclePwd123@//localhost:1521/FREEPDB1 \
  DIRECTORY=DPUMP_DIR \
  DUMPFILE=produtos_lab.dmp \
  LOGFILE=produtos_lab_imp.log \
  TABLES=SYSTEM.PRODUTOS,SYSTEM.PRODUTOS_CARGA \
  TABLE_EXISTS_ACTION=REPLACE
```

Leia o log:

```bash
cat /opt/oracle/labdata/dpump/produtos_lab_imp.log
```

## 11. Validar a restauração

Execute:

```bash
sqlplus -s system/OraclePwd123@//localhost:1521/FREEPDB1 <<'SQL'
SET PAGESIZE 50
SET LINESIZE 160

SELECT table_name
FROM user_tables
WHERE table_name IN ('PRODUTOS', 'PRODUTOS_CARGA')
ORDER BY table_name;

SELECT COUNT(*) AS total_produtos
FROM produtos;

SELECT COUNT(*) AS total_produtos_carga
FROM produtos_carga;

SELECT id_produto,
       nome_produto,
       categoria,
       preco
FROM produtos
ORDER BY id_produto
FETCH FIRST 10 ROWS ONLY;

EXIT;
SQL
```

Resultado esperado:

```text
PRODUTOS          -> 500 registros
PRODUTOS_CARGA    -> 500 registros
```

## 12. Repetir o laboratório

Para repetir desde o início:

1. execute novamente `produtos-500.sql` com `SQL*Plus`;
2. execute novamente o `SQL*Loader`;
3. remova o dump anterior para não receber erro de arquivo existente;
4. execute novamente o `expdp`;
5. remova as tabelas;
6. execute o `impdp`;
7. valide as duas contagens.

Remova somente o dump anterior quando quiser gerar outro arquivo com o mesmo nome:

```bash
rm -f /opt/oracle/labdata/dpump/produtos_lab.dmp
rm -f /opt/oracle/labdata/dpump/produtos_lab_exp.log
rm -f /opt/oracle/labdata/dpump/produtos_lab_imp.log
```

## 13. Problemas comuns

### ORA-39000 ou ORA-27038: arquivo de dump já existe

O `expdp` não sobrescreve automaticamente um dump existente. Remova o arquivo anterior ou use outro nome:

```bash
rm -f /opt/oracle/labdata/dpump/produtos_lab.dmp
```

### ORA-39087: diretório inválido

Confira os dois lados do diretório:

```text
Oracle DIRECTORY: /opt/oracle/labdata/dpump
Filesystem:       /opt/oracle/labdata/dpump
```

O caminho precisa existir dentro do container e ser exatamente igual ao caminho configurado no `CREATE DIRECTORY`.

### SQL*Loader não carrega registros

Confira:

```bash
cat /opt/oracle/labdata/produtos_sqlldr.log
ls -lah /opt/oracle/labdata/produtos.csv
cat /opt/oracle/labdata/produtos.ctl
```

Também confirme se a tabela `PRODUTOS_CARGA` foi criada pelo arquivo `produtos-500.sql`.

### ORA-12514 ou falha de conexão

Confira o service name e o container:

```text
Service Name: FREEPDB1
Dentro do container: localhost:1521
No host: localhost:1522
```

## 14. Comparação final

| Necessidade | Ferramenta | Resultado |
| :--- | :--- | :--- |
| Executar SQL e scripts | `sqlplus` | Cria objetos, insere e consulta dados |
| Carregar CSV | `sqlldr` | Insere registros usando `.ctl` |
| Exportar dados e metadados | `expdp` | Cria o dump lógico `.dmp` |
| Importar o dump | `impdp` | Recria tabelas e dados |

## Resultado mental esperado

```text
SQL*Plus
  -> executa produtos-500.sql
      -> 500 produtos criados

SQL*Loader
  -> lê produtos.csv
      -> 500 produtos carregados em PRODUTOS_CARGA

expdp
  -> exporta PRODUTOS e PRODUTOS_CARGA
      -> produtos_lab.dmp

impdp
  -> lê produtos_lab.dmp
      -> recria as tabelas
          -> 500 + 500 registros validados
```

Referências relacionadas:

- [Aula 3 - Módulo 2](../aula-3-modulo2/README.md)
- [Laboratório anterior com segurança e carga](../aula-3-modulo2/pratica.md)
- [Versões Oracle com Podman](../../repo/oracle/versoes/README.md)
