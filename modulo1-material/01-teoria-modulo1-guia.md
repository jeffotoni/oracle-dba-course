# Oracle - Guia Full
## CDB, PDB, Funcionalidades, Engenharia de Dados, Eventos e Comparações de Mercado

---

## 1. O que é Oracle

Oracle Database é um banco relacional corporativo com foco em confiabilidade, transações, segurança e operação em larga escala. Também oferece capacidades multimodelo (JSON, espacial, grafo e vetorial).

---

## 2. Arquitetura multitenant

### CDB (Container Database)

Banco contêiner principal com estrutura administrativa global.

### PDB (Pluggable Database)

Banco conectável dentro do CDB, com isolamento lógico para dados e objetos de aplicação.

### Analogia didática

- CDB: prédio
- PDB: apartamentos

### Consultas de validação

```sql
SELECT name,
       open_mode
FROM v$database;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

---

## 3. Criação de PDB (exemplo)

```sql
CREATE PLUGGABLE DATABASE meu_pdb
  ADMIN USER admin IDENTIFIED BY senha123
  FILE_NAME_CONVERT = ('pdbseed', 'meu_pdb');

ALTER PLUGGABLE DATABASE meu_pdb OPEN;
ALTER SESSION SET CONTAINER = meu_pdb;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

---

## 4. Onde Oracle manda bem (visão rápida)

| Modelo / Carga | Nível no Oracle | Observação prática |
|---|---|---|
| Relacional (OLTP) | Excelente | Ponto forte histórico |
| OLAP / DW | Excelente | Forte com particionamento, MVs e In-Memory |
| JSON | Muito bom | Bom para híbrido relacional + documento |
| Spatial | Excelente | Muito consolidado |
| Vector | Em crescimento forte | Evolução relevante no 23c |
| Graph | Bom | Atende cenários de relacionamento complexo |
| Time Series | Bom | Funciona bem com modelagem correta |
| Streaming / Event Store | Limitado nativo | AQ atende interno; ecossistema externo escala melhor |
| Key-Value | Básico | Viável para casos simples |

---

## 5. Tabela completa de funcionalidades

### 5.1. Estrutura

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Estrutura | CDB / PDB | Multi-tenant (vários bancos em um container) | SaaS / isolamento |
| Estrutura | Tables / Indexes | Estrutura base de dados + índices | Core |
| Estrutura | Partitioning | Divisão de tabelas grandes (range, hash, list) | Alta escala |
| Estrutura | Tablespaces | Organização física de dados | Administração |

### 5.2. SQL / Query

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| SQL / Query | SELECT / JOIN / GROUP BY | Consultas padrão | Core |
| SQL / Query | Analytical Functions | `ROW_NUMBER`, `RANK`, `OVER()` | BI / relatórios |
| SQL / Query | MERGE | UPSERT nativo | Integração |
| SQL / Query | Subqueries | Consultas aninhadas | Queries complexas |

### 5.3. PL/SQL

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| PL/SQL | Procedures | Rotinas armazenadas | Backend no banco |
| PL/SQL | Functions | Rotinas com retorno | Regras de negócio |
| PL/SQL | Packages | Organização de código | Enterprise |
| PL/SQL | Exceptions | Tratamento de erro | Controle operacional |

### 5.4. Eventos

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Eventos | Triggers | Executa código ao alterar dados | Auditoria |
| Eventos | DBMS_SCHEDULER | Jobs agendados | Batch |
| Eventos | DBMS_ALERT | Notificação entre sessões | Sinalização simples |
| Eventos | Oracle AQ | Fila interna (mensageria) | Event-driven interno |

### 5.5. Integração

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Integração | UTL_HTTP | Chamada HTTP externa | Integração API |
| Integração | UTL_FILE | Leitura/escrita de arquivos | ETL |
| Integração | DB Links | Acesso a outros bancos | Integração entre bases |
| Integração | External Tables | Leitura de arquivos como tabela | Big Data / ingestão |

### 5.6. Performance

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Performance | Index (B-tree, Bitmap) | Otimização de busca | Core |
| Performance | Explain Plan | Análise de plano de execução | Tuning |
| Performance | Hints | Influenciar plano de execução | Ajuste fino |
| Performance | Materialized Views | Cache de consulta | BI |

### 5.7. Segurança

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Segurança | Roles / Grants | Controle de acesso | Core |
| Segurança | Profiles | Limites de recursos e senha | Segurança |
| Segurança | VPD | Segurança por linha | Multi-tenant |
| Segurança | TDE | Criptografia em repouso | Compliance |

### 5.8. Transações

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Transações | COMMIT / ROLLBACK | Controle transacional | Core |
| Transações | Savepoints | Pontos intermediários | Controle fino |
| Transações | Locking | Controle de concorrência | Alta carga |

### 5.9. Alta disponibilidade

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| Alta disponibilidade | Data Guard | Réplica standby | Disaster recovery |
| Alta disponibilidade | Flashback | Voltar dados no tempo | Recuperação |
| Alta disponibilidade | RMAN | Backup e restore | Core |
| Alta disponibilidade | RAC | Cluster ativo | Escala extrema |

### 5.10. ETL e movimentação de dados

| Categoria | Funcionalidade | Descrição prática | Uso real |
|---|---|---|---|
| ETL | External Tables | Ler CSV/arquivo como tabela | Ingestão |
| ETL | SQL*Loader | Carga massiva | Big data |
| ETL | Data Pump | Export/import rápido | Migração |
| ETL | Materialized Views | Pré-processamento de dados | BI |
| ETL | Streams / GoldenGate | Replicação de dados | CDC |

Nota prática: `Oracle Streams` é legado; para CDC moderno em Oracle, `GoldenGate` é o caminho mais comum no mercado.

---

## 6. Eventos e CDC (o ponto crítico)

### O que usar quando

- Eventos internos dentro do próprio Oracle: `Oracle AQ`, `Triggers`, `DBMS_SCHEDULER`.
- CDC corporativo entre ambientes heterogêneos: `GoldenGate`.

### Regra de arquitetura

- Se o evento nasce e morre no banco, AQ pode resolver bem.
- Se o evento precisa ir para múltiplos sistemas, preferir CDC/fila externa e processamento desacoplado.

### Exemplo Oracle AQ (enqueue)

```sql
BEGIN
  DBMS_AQ.enqueue(
    queue_name         => 'fila_eventos',
    enqueue_options    => DBMS_AQ.enqueue_options_t(),
    message_properties => DBMS_AQ.message_properties_t(),
    payload            => 'evento_teste',
    msgid              => NULL
  );
END;
```

---

## 7. Modelos adicionais que Oracle assume

### 7.1. Time Series (sim, dá para fazer bem)

Capacidades principais:

- particionamento por tempo (`RANGE`);
- índice por timestamp;
- compressão;
- materialized views para agregados.

Exemplo mental:

```sql
CREATE TABLE metrics (
  ts TIMESTAMP,
  value NUMBER
)
PARTITION BY RANGE (ts) (
  PARTITION p2026m01 VALUES LESS THAN (TIMESTAMP '2026-02-01 00:00:00'),
  PARTITION p2026m02 VALUES LESS THAN (TIMESTAMP '2026-03-01 00:00:00')
);
```

### 7.2. Graph Database

Oracle suporta grafo para consultas de relacionamentos complexos (fraude, recomendação, lineage).

### 7.3. OLAP / Data Warehouse

Com `partitioning`, `materialized views`, paralelismo e `In-Memory`, Oracle atende muito bem DW corporativo.

### 7.4. Document Store (NoSQL-like)

JSON nativo com SQL funciona bem para arquitetura híbrida relacional + documento.

### 7.5. Streaming / Event Store (limitado nativo)

Há suporte interno com AQ, mas não substitui plataformas de streaming dedicadas em cenários de altíssima escala distribuída.

### 7.6. XML Database

Legado forte e ainda útil em ambientes específicos:

- `XMLType`
- `XPath` / `XQuery`
- armazenamento estruturado XML

### 7.7. In-Memory Database

Capacidades:

- dados em memória;
- formato colunar;
- consultas analíticas muito rápidas.

Benefício típico: aproximar OLTP + OLAP no mesmo ecossistema.

### 7.8. Key-Value (limitado)

Funciona para caso simples:

```sql
CREATE TABLE kv (
  key_col VARCHAR2(100),
  value_col CLOB
);
```

Também pode ser modelado com JSON. Não substitui Redis para cenários especializados de latência extrema.

---

## 8. AI Database (23c)

Direção prática do Oracle 23c:

- vetor nativo;
- busca semântica;
- integração com fluxos de IA/GenAI.

Resumo estratégico: Oracle está posicionando a plataforma para aplicações GenAI em cenários empresariais com governança de dados.

---

## 9. Comparação objetiva com ferramentas de mercado

Comparações comuns (em geral):

- JSON muito pesado e arquitetura 100% documento: MongoDB pode ser mais natural.
- Busca vetorial em escala especializada: Pinecone / Weaviate podem simplificar operação dedicada.
- ETL/transformação distribuída: Spark e DuckDB podem ser mais flexíveis em pipelines analíticos.

Critério recomendado:

1. manter Oracle como core transacional e governança;
2. complementar com motor especializado quando o caso exigir;
3. evitar mover tudo para um único produto por conveniência.

---

## 10. Exemplos construídos (rápidos)

### 10.1. SQL analítico

```sql
SELECT deptno,
       ename,
       sal,
       ROW_NUMBER() OVER (PARTITION BY deptno ORDER BY sal DESC) AS rn
FROM emp;
```

### 10.2. MERGE (UPSERT)

```sql
MERGE INTO cliente c
USING (SELECT :id id, :nome nome FROM dual) src
ON (c.id = src.id)
WHEN MATCHED THEN UPDATE SET c.nome = src.nome
WHEN NOT MATCHED THEN INSERT (id, nome) VALUES (src.id, src.nome);
```

### 10.3. Procedure simples

```sql
CREATE OR REPLACE PROCEDURE prc_log(p_msg IN VARCHAR2) AS
BEGIN
  INSERT INTO log_exec(msg, dt_exec) VALUES (p_msg, SYSTIMESTAMP);
END;
```

### 10.4. Trigger de auditoria

```sql
CREATE OR REPLACE TRIGGER trg_aud_cliente
AFTER INSERT OR UPDATE OR DELETE ON cliente
FOR EACH ROW
BEGIN
  INSERT INTO aud_cliente(dt_evento, acao)
  VALUES (SYSTIMESTAMP, ORA_SYSEVENT);
END;
```

### 10.5. Job com DBMS_SCHEDULER

```sql
BEGIN
  DBMS_SCHEDULER.create_job(
    job_name        => 'JOB_LIMPA_LOG',
    job_type        => 'PLSQL_BLOCK',
    job_action      => 'BEGIN DELETE FROM log_exec WHERE dt_exec < SYSTIMESTAMP - INTERVAL ''30'' DAY; COMMIT; END;',
    start_date      => SYSTIMESTAMP,
    repeat_interval => 'FREQ=DAILY;BYHOUR=1;BYMINUTE=0;BYSECOND=0',
    enabled         => TRUE
  );
END;
```

### 10.6. JSON exemplo

```sql
SELECT JSON_VALUE(doc, '$.cliente.nome') AS nome
FROM pedidos_json;
```

---

## 11. Arquitetura recomendada (prática)

Fluxo recomendado:

1. Oracle persiste estado transacional.
2. Eventos são publicados (AQ, CDC ou broker externo).
3. Workers processam assíncrono.
4. APIs expõem dados e comandos.

Evitar no banco:

- lógica de negócio excessiva;
- chamadas HTTP críticas síncronas;
- acoplamento forte com sistemas externos.

Preferir:

- desacoplamento por fila/evento;
- processamento externo;
- observabilidade e retries fora do banco.

---

## 12. Conclusão

Oracle é forte como plataforma enterprise para:

- OLTP relacional;
- DW/OLAP;
- segurança e alta disponibilidade;
- multimodelo com governança.

Estratégia moderna recomendada: Oracle no core + ferramentas especializadas quando o caso exigir.
