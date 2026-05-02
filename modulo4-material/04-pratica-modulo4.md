# Módulo 4 – Prática  
## Monitoramento, Tuning e Otimização de Desempenho

## Visão geral

Neste módulo usaremos um laboratório prático para consolidar os principais conceitos de monitoramento, diagnóstico e tuning no Oracle.

A prática será organizada em blocos progressivos:

1. preparação do ambiente;
2. criação de massa de dados para análise;
3. consultas de observação nas visões dinâmicas de desempenho;
4. análise de sessões, waits, locks e consumo de recursos;
5. leitura de planos de execução;
6. comparação entre SQL ruim e SQL melhorado;
7. uso de estatísticas e índices;
8. observação opcional de AWR, ADDM e SQL Tuning Advisor, quando o ambiente permitir.

A proposta é manter um laboratório reproduzível em Podman, alinhado ao ambiente já adotado nos módulos anteriores.

---

## Ambiente utilizado

Usaremos:

- Podman;
- Oracle Database Free em container;
- CloudBeaver para consultas e inspeção visual;
- scripts SQL para geração de carga e observação do ambiente.

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
- **service name**: `FREEPDB1`

Também usaremos um usuário próprio para o laboratório:

- **usuário**: `app_perf`
- **senha**: `AppPerf123`

---

## 1. Estrutura recomendada do módulo

```text
modulo4-monitoramento-tuning/
├── compose.yaml
└── scripts/
```

---

## 2. Subida do ambiente com Podman

## 2.1. compose.yaml

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

## 2.2. Comandos para subir o ambiente

```bash
podman compose up -d
podman ps
podman logs -f oracle-free
```

## 2.3. Entrar no container

```bash
podman exec -it oracle-free bash
```

## 2.4. Validar conexão no CloudBeaver

Conectar no CloudBeaver como `system` em `FREEPDB1`.

Consultas iniciais:

```sql
SELECT instance_name, status FROM v$instance;
SELECT name, open_mode FROM v$pdbs;
SELECT USER AS current_user
FROM dual;
```

## 2.5. Checklist SQL mínimo do módulo

```sql
SELECT instance_name,
       status
FROM v$instance;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT USER AS current_user
FROM dual;
```

---

## 3. Preparação do ambiente de laboratório

## 3.1. Criar usuário do laboratório

Conectar no CloudBeaver como `system`.

```sql
CREATE USER app_perf IDENTIFIED BY AppPerf123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_perf;
```

## 3.2. Conectar como APP_PERF

Conectar no CloudBeaver como `app_perf`.

## 3.3. Criar tabela principal do laboratório

```sql
CREATE TABLE vendas_lab (
  id_venda        NUMBER PRIMARY KEY,
  cliente         VARCHAR2(100),
  categoria       VARCHAR2(50),
  cidade          VARCHAR2(50),
  valor_total     NUMBER(10,2),
  data_venda      DATE,
  status_venda    VARCHAR2(20)
);
```

## 3.4. Gerar massa de dados

```sql
BEGIN
  FOR i IN 1..50000 LOOP
    INSERT INTO vendas_lab (
      id_venda,
      cliente,
      categoria,
      cidade,
      valor_total,
      data_venda,
      status_venda
    ) VALUES (
      i,
      'CLIENTE_' || MOD(i, 1000),
      CASE MOD(i, 5)
        WHEN 0 THEN 'INFORMATICA'
        WHEN 1 THEN 'MOVEIS'
        WHEN 2 THEN 'AUDIO'
        WHEN 3 THEN 'VIDEO'
        ELSE 'PERIFERICOS'
      END,
      CASE MOD(i, 6)
        WHEN 0 THEN 'BELO HORIZONTE'
        WHEN 1 THEN 'SAO PAULO'
        WHEN 2 THEN 'RIO DE JANEIRO'
        WHEN 3 THEN 'CURITIBA'
        WHEN 4 THEN 'SALVADOR'
        ELSE 'RECIFE'
      END,
      ROUND(DBMS_RANDOM.VALUE(50, 5000), 2),
      SYSDATE - MOD(i, 365),
      CASE MOD(i, 4)
        WHEN 0 THEN 'ABERTA'
        WHEN 1 THEN 'FATURADA'
        WHEN 2 THEN 'CANCELADA'
        ELSE 'ENTREGUE'
      END
    );
    IF MOD(i, 1000) = 0 THEN
      COMMIT;
    END IF;
  END LOOP;
  COMMIT;
END;
/
```

## 3.5. Validar os dados

```sql
SELECT COUNT(*) FROM vendas_lab;
SELECT MIN(id_venda), MAX(id_venda) FROM vendas_lab;
SELECT categoria, COUNT(*) FROM vendas_lab GROUP BY categoria ORDER BY categoria;
```

---

## 4. Coleta inicial de estatísticas

Antes de observar o comportamento do otimizador, deveremos garantir estatísticas coerentes.

Conectar como SYSTEM:

Conectar no CloudBeaver como `system`.

```sql
BEGIN
  DBMS_STATS.GATHER_SCHEMA_STATS(
    ownname => 'APP_PERF',
    cascade => TRUE
  );
END;
/
```

Validar:

```sql
SELECT table_name, num_rows, last_analyzed
FROM dba_tables
WHERE owner = 'APP_PERF'
ORDER BY table_name;
```

---

## 5. Observação básica do ambiente

## 5.1. Estado da instância

```sql
SELECT instance_name, status, database_status
FROM v$instance;
```

## 5.2. Informações do banco

```sql
SELECT name, open_mode, log_mode
FROM v$database;
```

## 5.3. Sessões ativas

```sql
SELECT sid, serial#, username, status, program, machine
FROM v$session
WHERE username IS NOT NULL
ORDER BY username, sid;
```

## 5.4. Processos relacionados

```sql
SELECT p.spid AS os_pid,
       s.sid,
       s.serial#,
       s.username,
       s.status,
       s.program
FROM v$process p
JOIN v$session s
  ON p.addr = s.paddr
WHERE s.username IS NOT NULL
ORDER BY s.sid;
```

## 5.5. Estatísticas gerais do sistema

```sql
SELECT name, value
FROM v$sysstat
WHERE name IN (
  'db block gets',
  'consistent gets',
  'physical reads',
  'physical writes',
  'user commits',
  'parse count (total)'
)
ORDER BY name;
```

## 5.6. Eventos de espera do sistema

```sql
SELECT event, total_waits, time_waited
FROM v$system_event
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC
FETCH FIRST 20 ROWS ONLY;
```

---

## 6. Consultas para monitoramento de sessões e waits

## 6.1. Sessões em espera

```sql
SELECT sid,
       serial#,
       username,
       status,
       event,
       wait_class,
       seconds_in_wait
FROM v$session
WHERE username IS NOT NULL
ORDER BY seconds_in_wait DESC, sid;
```

## 6.2. Sessões ativas por usuário

```sql
SELECT username, status, COUNT(*) AS qtd
FROM v$session
WHERE username IS NOT NULL
GROUP BY username, status
ORDER BY username, status;
```

## 6.3. Eventos por sessão

```sql
SELECT sid, event, total_waits, time_waited
FROM v$session_event
WHERE sid IN (
  SELECT sid FROM v$session WHERE username IS NOT NULL
)
ORDER BY sid, time_waited DESC;
```

---

## 7. Consultas para identificação de SQL custoso

## 7.1. SQLs mais custosos por elapsed time

```sql
SELECT sql_id,
       executions,
       elapsed_time,
       cpu_time,
       buffer_gets,
       disk_reads,
       SUBSTR(sql_text, 1, 100) AS sql_text
FROM v$sql
WHERE parsing_schema_name = 'APP_PERF'
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;
```

## 7.2. SQLs mais custosos por leituras lógicas

```sql
SELECT sql_id,
       executions,
       buffer_gets,
       disk_reads,
       rows_processed,
       SUBSTR(sql_text, 1, 100) AS sql_text
FROM v$sql
WHERE parsing_schema_name = 'APP_PERF'
ORDER BY buffer_gets DESC
FETCH FIRST 10 ROWS ONLY;
```

## 7.3. SQLAREA consolidada

```sql
SELECT sql_id,
       executions,
       buffer_gets,
       disk_reads,
       elapsed_time,
       SUBSTR(sql_text, 1, 100) AS sql_text
FROM v$sqlarea
WHERE parsing_schema_name = 'APP_PERF'
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;
```

---

## 8. Explain Plan e DBMS_XPLAN

## 8.1. Query de exemplo sem índice dedicado

Conectar como `app_perf`:

Conectar no CloudBeaver como `app_perf`.

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE categoria = 'AUDIO'
  AND cidade = 'SAO PAULO';
```

## 8.2. Exibir o plano

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

## 8.3. Query agregada de exemplo

```sql
EXPLAIN PLAN FOR
SELECT cidade, categoria, COUNT(*), SUM(valor_total)
FROM vendas_lab
WHERE data_venda >= SYSDATE - 90
GROUP BY cidade, categoria;
```

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

---

## 9. Captura de plano real com DISPLAY_CURSOR

## 9.1. Executar uma query

```sql
SELECT COUNT(*)
FROM vendas_lab
WHERE categoria = 'AUDIO'
  AND cidade = 'SAO PAULO';
```

## 9.2. Descobrir o SQL_ID

```sql
SELECT sql_id,
       SUBSTR(sql_text, 1, 100) AS sql_text
FROM v$sql
WHERE sql_text LIKE 'SELECT COUNT(*)%VENDAS_LAB%'
ORDER BY last_active_time DESC
FETCH FIRST 5 ROWS ONLY;
```

## 9.3. Mostrar o plano do cursor

Substituir `<SQL_ID>` pelo valor encontrado.

```sql
SELECT * 
FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('<SQL_ID>', NULL, 'ALLSTATS LAST'));
```

---

## 10. Comparação entre SQL ruim e SQL melhorado

## 10.1. Exemplo de SQL ruim – função sobre a coluna filtrada

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE UPPER(cidade) = 'SAO PAULO';
```

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

### Interpretação

Ao aplicar função diretamente sobre a coluna filtrada, aumentamos o risco de dificultar o uso eficiente de índices simples.

## 10.2. Exemplo mais limpo

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE cidade = 'SAO PAULO';
```

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

---

## 11. Criação de índice e comparação de plano

## 11.1. Criar índice de apoio

Conectar como `app_perf`:

```sql
CREATE INDEX idx_vendas_lab_cat_cid
ON vendas_lab (categoria, cidade);
```

## 11.2. Coletar estatísticas novamente

Conectar como SYSTEM:

Conectar no CloudBeaver como `system`.

```sql
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(
    ownname => 'APP_PERF',
    tabname => 'VENDAS_LAB',
    cascade => TRUE
  );
END;
/
```

## 11.3. Reexecutar Explain Plan

Conectar como `app_perf`:

Conectar no CloudBeaver como `app_perf`.

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE categoria = 'AUDIO'
  AND cidade = 'SAO PAULO';
```

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

## 11.4. Comparar antes e depois

Deveremos observar se houve mudança de estratégia de acesso, como uso do índice em vez de leitura mais ampla.

---

## 12. Observação das estatísticas do objeto

Conectar no CloudBeaver como `system`.

## 12.1. Estatísticas da tabela

```sql
SELECT owner, table_name, num_rows, blocks, avg_row_len, last_analyzed
FROM dba_tables
WHERE owner = 'APP_PERF'
  AND table_name = 'VENDAS_LAB';
```

## 12.2. Estatísticas do índice

```sql
SELECT owner, index_name, table_name, num_rows, leaf_blocks, distinct_keys, last_analyzed
FROM dba_indexes
WHERE owner = 'APP_PERF'
ORDER BY index_name;
```

## 12.3. Colunas e cardinalidade aproximada

```sql
SELECT owner, table_name, column_name, num_distinct, num_nulls, last_analyzed
FROM dba_tab_col_statistics
WHERE owner = 'APP_PERF'
  AND table_name = 'VENDAS_LAB'
ORDER BY column_name;
```

---

## 13. Simulação de lock

Esse bloco é importante para mostrar que lentidão e espera podem estar associadas a concorrência e bloqueio.

## 13.1. Criar tabela de lock

Conectar como `app_perf`:

```sql
CREATE TABLE lock_lab (
  id NUMBER PRIMARY KEY,
  descricao VARCHAR2(100)
);

INSERT INTO lock_lab VALUES (1, 'registro inicial');
COMMIT;
```

## 13.2. Sessão 1 – iniciar atualização sem commit

Abrir **Terminal 1**:

Abrir uma sessão no CloudBeaver como `app_perf`.

```sql
UPDATE lock_lab
SET descricao = 'sessao1'
WHERE id = 1;
```

**Não executar COMMIT ainda.**

## 13.3. Sessão 2 – tentar atualizar o mesmo registro

Abrir **Terminal 2**:

Abrir uma segunda sessão no CloudBeaver como `app_perf`.

```sql
UPDATE lock_lab
SET descricao = 'sessao2'
WHERE id = 1;
```

Essa segunda sessão deverá ficar aguardando.

## 13.4. Sessão administrativa – observar o lock

Abrir **Terminal 3**:

Abrir uma sessão administrativa no CloudBeaver como `system`.

### Ver sessões do usuário APP_PERF

```sql
SELECT sid, serial#, username, status, event, blocking_session
FROM v$session
WHERE username = 'APP_PERF'
ORDER BY sid;
```

### Ver locks

```sql
SELECT sid, type, id1, id2, lmode, request, block
FROM v$lock
ORDER BY sid;
```

### Ver objetos bloqueados

```sql
SELECT lo.session_id,
       lo.oracle_username,
       lo.object_id,
       o.object_name,
       lo.locked_mode
FROM v$locked_object lo
JOIN dba_objects o
  ON lo.object_id = o.object_id
ORDER BY lo.session_id;
```

## 13.5. Liberar o lock

Voltar ao **Terminal 1** e executar:

```sql
COMMIT;
```

A Sessão 2 deverá prosseguir.

---

## 14. Monitoramento de sessões bloqueadoras

Conectar como SYSTEM:

Conectar no CloudBeaver como `system`.

```sql
SELECT sid,
       serial#,
       username,
       blocking_session,
       event,
       seconds_in_wait
FROM v$session
WHERE blocking_session IS NOT NULL
   OR sid IN (
      SELECT blocking_session
      FROM v$session
      WHERE blocking_session IS NOT NULL
   )
ORDER BY sid;
```

---

## 15. Leituras e interpretação de waits

## 15.1. Waits do sistema

```sql
SELECT event,
       total_waits,
       time_waited,
       average_wait
FROM v$system_event
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC
FETCH FIRST 20 ROWS ONLY;
```

## 15.2. Waits por sessão

```sql
SELECT s.sid,
       s.serial#,
       s.username,
       se.event,
       se.total_waits,
       se.time_waited
FROM v$session s
JOIN v$session_event se
  ON s.sid = se.sid
WHERE s.username IS NOT NULL
ORDER BY s.sid, se.time_waited DESC;
```

---

## 16. Alert log e diagnóstico operacional

## 16.1. Descobrir o trace file da instância

Conectar como SYSDBA:

Conectar como `SYS` com papel `SYSDBA` no CloudBeaver.

```sql
SELECT value
FROM v$diag_info
WHERE name = 'Diag Trace';
```

## 16.2. Ler o alert log no sistema operacional

Dentro do container, ajustar o caminho conforme o valor retornado:

```bash
tail -n 100 /opt/oracle/diag/rdbms/*/*/trace/alert_*.log
```

### Observação

Esse passo ajuda a mostrar como o alert log complementa o diagnóstico de desempenho e operação.

---

## 17. Bloco opcional – AWR, ADDM e SQL Tuning Advisor

Este bloco deverá ser tratado como **opcional** no laboratório com Oracle Free em Podman.

## 17.1. Verificar o parâmetro de acesso a packs

Conectar como SYSTEM ou SYS:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'control_management_pack_access';
```

## 17.2. Interpretação

Se o valor estiver como `NONE`, o ambiente não está habilitado para os recursos associados aos packs diagnósticos e de tuning.

Se o ambiente estiver licenciado e configurado apropriadamente, poderemos tratar conceitualmente:

- AWR;
- ADDM;
- SQL Tuning Advisor.

## 17.3. Observação prática

Em laboratório simples com Oracle Free, o foco principal deverá ficar em:

- `V$ Views`;
- `EXPLAIN PLAN`;
- `DBMS_XPLAN.DISPLAY_CURSOR`;
- estatísticas;
- locks;
- waits;
- análise de SQL.

---

## 18. Consultas úteis de apoio

## 18.1. Diagnóstico enxuto de sessões

```sql
SELECT sid,
       serial#,
       username,
       status,
       event,
       wait_class,
       program
FROM v$session
WHERE username IS NOT NULL
ORDER BY sid;

SELECT username,
       status,
       COUNT(*) AS total_sessions
FROM v$session
WHERE username IS NOT NULL
GROUP BY username, status
ORDER BY username, status;
```

## 18.2. Diagnóstico enxuto de waits e locks

```sql
SELECT event,
       total_waits,
       time_waited
FROM v$system_event
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC
FETCH FIRST 10 ROWS ONLY;

SELECT lo.session_id,
       do.object_name,
       lo.locked_mode
FROM v$locked_object lo
JOIN dba_objects do
  ON do.object_id = lo.object_id
ORDER BY lo.session_id;
```

## 18.3. Diagnóstico enxuto de SQL

```sql
SELECT sql_id,
       executions,
       elapsed_time,
       cpu_time,
       buffer_gets
FROM v$sqlarea
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;
```

## 18.4. Validação final do módulo

```sql
SELECT COUNT(*) AS total_rows
FROM vendas_lab;

SELECT categoria,
       COUNT(*) AS total_rows
FROM vendas_lab
GROUP BY categoria
ORDER BY categoria;
```

## 18.5. Objetos do schema APP_PERF

```sql
SELECT object_name, object_type, status
FROM dba_objects
WHERE owner = 'APP_PERF'
ORDER BY object_type, object_name;
```

## 18.6. Índices do usuário

```sql
SELECT index_name, table_name, status
FROM user_indexes
ORDER BY index_name;
```

## 18.7. Tabelas do usuário

```sql
SELECT table_name
FROM user_tables
ORDER BY table_name;
```

## 18.8. SQL executados recentemente pelo schema

```sql
SELECT sql_id,
       last_active_time,
       executions,
       elapsed_time,
       SUBSTR(sql_text, 1, 100) AS sql_text
FROM v$sql
WHERE parsing_schema_name = 'APP_PERF'
ORDER BY last_active_time DESC
FETCH FIRST 15 ROWS ONLY;
```

---

## 19. Limpeza do laboratório

Se quisermos repetir a prática do zero, poderemos remover os objetos criados.

Conectar como `app_perf`:

Conectar no CloudBeaver como `app_perf`.

```sql
DROP TABLE lock_lab PURGE;
DROP TABLE vendas_lab PURGE;
DROP INDEX idx_vendas_lab_cat_cid;
```

Conectar como SYSTEM:

Conectar no CloudBeaver como `system`.

```sql
DROP USER app_perf CASCADE;
```

> Observação: se a tabela `vendas_lab` for removida antes do índice, o índice será removido automaticamente junto com a tabela.

---

## 20. Resultado esperado da prática

Ao final deste módulo, deveremos ter exercitado:

- observação da instância e das sessões;
- uso de `V$SESSION`, `V$PROCESS`, `V$SYSSTAT`, `V$SYSTEM_EVENT`, `V$SQL`, `V$LOCK` e `V$LOCKED_OBJECT`;
- leitura de waits e identificação de locks;
- geração e inspeção de planos com `EXPLAIN PLAN`;
- captura de plano real com `DBMS_XPLAN.DISPLAY_CURSOR`;
- coleta de estatísticas com `DBMS_STATS`;
- comparação entre SQL menos eficiente e SQL melhorado;
- impacto de índice e estatísticas no comportamento do plano;
- leitura do alert log como apoio ao diagnóstico.

---

## 21. Referências oficiais úteis

### Oracle Database Free em container
- https://github.com/gvenzl/oci-oracle-free

### V$SESSION
- https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-SESSION.html

### V$LOCK
- https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOCK.html

### V$LOCKED_OBJECT
- https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOCKED_OBJECT.html

### DBMS_XPLAN
- https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_XPLAN.html

### Explain Plan
- https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/generating-and-displaying-execution-plans.html

### DBMS_STATS
- https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_STATS.html

### Gather Optimizer Statistics
- https://docs.oracle.com/en/database/oracle/oracle-database/18/tgsql/gathering-optimizer-statistics.html

### CONTROL_MANAGEMENT_PACK_ACCESS
- https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/CONTROL_MANAGEMENT_PACK_ACCESS.html

### Data Concurrency and Consistency
- https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/data-concurrency-and-consistency.html
