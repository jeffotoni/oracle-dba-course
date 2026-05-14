# Revisão do Módulo 4 - aula 5

> Revisão do módulo 4: monitoramento, tuning, waits, locks, planos de execução, estatísticas e leitura de desempenho no Oracle.

## Ideia central do módulo

O módulo 4 trata de uma mudança importante de postura:

```txt
Lentidão é sintoma
Tuning exige evidência
Monitoramento e análise andam juntos
```

Em termos práticos:

- não basta dizer que “o banco está lento”;
- é preciso observar sessões, SQL, waits, locks, consumo e plano de execução;
- tuning bom começa com diagnóstico, não com chute.

## O que precisa ficar claro

- monitoramento preventivo é diferente de monitoramento corretivo;
- lentidão percebida não é diagnóstico;
- `V$ Views` são base da observabilidade Oracle;
- sessões, processos, waits e locks ajudam a localizar gargalos;
- plano de execução e estatísticas influenciam o comportamento do SQL;
- índice ajuda, mas não resolve tudo sozinho;
- tuning sem evidência costuma piorar o ambiente.

## 1. Monitoramento do ambiente Oracle

Monitorar Oracle significa observar continuamente como o ambiente está se comportando.

Isso inclui:

- instância;
- sessões;
- CPU;
- memória;
- I/O;
- waits;
- locks;
- SQL custoso;
- crescimento de objetos;
- geração de redo;
- uso de tablespaces.

### Regra prática

```txt
Monitorar não é só ver se o banco está no ar
Monitorar é produzir evidência sobre o comportamento do ambiente
```

## 2. Monitoramento preventivo x corretivo

### Preventivo

Busca antecipar problema, antes da reclamação do usuário.

Exemplos:

- aumento de waits;
- crescimento anormal;
- saturação de sessão;
- piora progressiva de tempo de resposta.

### Corretivo

É acionado quando o incidente já apareceu.

Exemplos:

- usuários reclamando de lentidão;
- sessões presas;
- job demorando demais;
- fila de espera crescendo.

### Regra curta

```txt
Preventivo = antecipar
Corretivo = responder
```

## 3. Fontes de observação

No Oracle, a leitura de desempenho passa por:

- `alert log`;
- `V$ Views`;
- planos de execução;
- estatísticas;
- `DBMS_XPLAN`;
- eventualmente `AWR`, `ADDM` e `SQL Tuning Advisor`, quando o ambiente permitir.

## 4. Sessões e processos

### Sessão

Representa a interação lógica de um usuário ou aplicação com o banco.

Ajuda a responder:

- quem está conectado;
- o que está executando;
- quem está esperando;
- quem está travando;
- quem está consumindo mais.

### Processo

Ajuda a conectar atividade Oracle com suporte operacional interno.

### Regra prática

```txt
Sessão = atividade lógica
Processo = execução associada
```

## 5. Waits

Wait é o tempo em que uma sessão está aguardando algo para continuar.

Isso pode estar ligado a:

- disco;
- lock;
- redo;
- rede;
- contenção interna;
- concorrência.

### Regra prática

```txt
Se o tempo está em espera, o problema pode não ser CPU pura
```

### Ponto importante

O evento de espera dominante é pista forte, mas não substitui análise de causa raiz.

## 6. Locks e deadlocks

### Lock

É parte normal do controle de concorrência.

### Quando vira problema

- retenção longa;
- bloqueio de transações importantes;
- fila de espera;
- pico com contenção;
- desenho ruim da aplicação.

### Deadlock

É espera circular entre transações.

### Regra prática

```txt
Lock não é sempre erro
Lock prolongado e concorrência mal desenhada viram problema
```

## 7. SQL custoso

Nem sempre o problema está “no banco inteiro”.

Muitas vezes o custo está concentrado em:

- poucas consultas;
- poucas sessões;
- plano ruim;
- uso ruim de função na coluna filtrada;
- ausência de índice adequado;
- estatísticas ruins ou desatualizadas.

## 8. Plano de execução

Plano de execução mostra como o Oracle decidiu acessar os dados.

Ele ajuda a entender:

- se houve leitura ampla;
- se houve uso de índice;
- se a estratégia de acesso mudou;
- se o custo estimado faz sentido para a consulta.

### Ferramentas que aparecem no módulo

- `EXPLAIN PLAN`
- `DBMS_XPLAN.DISPLAY`
- `DBMS_XPLAN.DISPLAY_CURSOR`

## 9. Estatísticas

As estatísticas ajudam o otimizador a tomar decisão.

Sem estatísticas coerentes, o plano pode ficar inadequado.

### Regra prática

```txt
Estatística ruim ou ausente pode levar a plano ruim
```

## 10. Índice

Índice pode melhorar bastante a consulta certa, mas não deve ser tratado como solução automática.

Ele precisa ser lido junto com:

- seletividade;
- padrão de filtro;
- plano;
- custo de manutenção;
- comportamento do workload.

## 11. Binários e ferramentas usados no módulo

Neste módulo, a maior parte da prática é feita com SQL em:

- `Oracle SQL Developer`
- `CloudBeaver`
- `DBeaver`
- ou equivalente

Mas também aparece o sistema operacional do container para apoio operacional.

### Exemplo importante

Leitura do alert log:

```bash
podman exec -it oracle-free bash
tail -n 100 /opt/oracle/diag/rdbms/*/*/trace/alert_*.log
```

### Regra prática

```txt
Diagnóstico principal = SQL + V$ Views + plano
Diagnóstico complementar = alert log e apoio operacional no container
```

## 12. Queries essenciais de revisão

### Estado da instância

```sql
SELECT instance_name,
       status,
       database_status
FROM v$instance;
```

### Informações do banco

```sql
SELECT name,
       open_mode,
       log_mode
FROM v$database;
```

### Sessões ativas

```sql
SELECT sid,
       serial#,
       username,
       status,
       program,
       machine
FROM v$session
WHERE username IS NOT NULL
ORDER BY username, sid;
```

### Processos relacionados

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

### Estatísticas gerais

```sql
SELECT name,
       value
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

### Esperas do sistema

```sql
SELECT event,
       total_waits,
       time_waited
FROM v$system_event
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC
FETCH FIRST 20 ROWS ONLY;
```

### Sessões em espera

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

### SQL custoso

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

### Locks

```sql
SELECT sid,
       type,
       id1,
       id2,
       lmode,
       request,
       block
FROM v$lock
ORDER BY sid;
```

### Objetos bloqueados

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

## 13. Fluxo prático mínimo do módulo

```txt
1. Subir Oracle e validar a instância
2. Criar usuário APP_PERF
3. Criar tabela e massa de dados
4. Coletar estatísticas
5. Observar sessões, waits e SQL
6. Gerar e ler planos de execução
7. Comparar SQL ruim e SQL melhorado
8. Criar índice e observar mudança de plano
9. Simular lock
10. Ler o alert log como apoio ao diagnóstico
```

## 14. Comandos e blocos que valem aparecer na revisão

### Criar usuário do laboratório

```sql
CREATE USER app_perf IDENTIFIED BY AppPerf123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_perf;
```

### Criar tabela principal

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

### Coletar estatísticas

```sql
BEGIN
  DBMS_STATS.GATHER_SCHEMA_STATS(
    ownname => 'APP_PERF',
    cascade => TRUE
  );
END;
/
```

### Explain Plan

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE categoria = 'AUDIO'
  AND cidade = 'SAO PAULO';
```

```sql
SELECT *
FROM TABLE(DBMS_XPLAN.DISPLAY);
```

### Plano real do cursor

```sql
SELECT *
FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('<SQL_ID>', NULL, 'ALLSTATS LAST'));
```

### SQL ruim

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE UPPER(cidade) = 'SAO PAULO';
```

### SQL melhorado

```sql
EXPLAIN PLAN FOR
SELECT *
FROM vendas_lab
WHERE cidade = 'SAO PAULO';
```

### Criar índice

```sql
CREATE INDEX idx_vendas_lab_cat_cid
ON vendas_lab (categoria, cidade);
```

### Simular lock

Sessão 1:

```sql
UPDATE lock_lab
SET descricao = 'sessao1'
WHERE id = 1;
```

Sessão 2:

```sql
UPDATE lock_lab
SET descricao = 'sessao2'
WHERE id = 1;
```

### Ler alert log

```sql
SELECT value
FROM v$diag_info
WHERE name = 'Diag Trace';
```

```bash
tail -n 100 /opt/oracle/diag/rdbms/*/*/trace/alert_*.log
```

## 15. Exemplos práticos que valem reforçar

## 15.1. Massa de dados importa

Sem massa de dados, o plano e o custo ficam menos interessantes para leitura.

## 15.2. Estatísticas influenciam o plano

Coletar estatísticas antes da comparação melhora o valor didático da prática.

## 15.3. Função na coluna filtrada pode piorar acesso

Esse exemplo é forte para mostrar por que SQL ruim gera custo extra.

## 15.4. Índice precisa ser observado no plano

Criar o índice e não conferir o plano deixa a aula incompleta.

## 15.5. Lock ajuda a conectar banco e aplicação

Esse bloco é bom porque mostra que concorrência e desenho de transação também influenciam desempenho.

## 16. Resultado esperado

Ao final da revisão, o que precisa ficar claro é:

- monitoramento é produção de evidência;
- tuning começa em diagnóstico;
- `V$SESSION`, `V$PROCESS`, `V$SYSTEM_EVENT`, `V$SQL`, `V$LOCK` e `V$LOCKED_OBJECT` são centrais;
- plano de execução e estatísticas mudam a leitura da consulta;
- índice deve ser interpretado junto com o plano;
- waits e locks ajudam a localizar gargalos reais;
- alert log entra como apoio complementar ao diagnóstico.

## Scripts originais do módulo

- `modulo4-material/04-teoria-modulo4.md`
  - base conceitual de monitoramento, tuning e desempenho.
- `modulo4-material/04-pratica-modulo4.md`
  - roteiro prático completo com massa de dados, waits, locks, planos, estatísticas e alert log.
