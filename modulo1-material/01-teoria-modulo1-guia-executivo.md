# Oracle - Guia Executivo (1 página)
## Visão prática para aula

## 1. Posição do Oracle no cenário atual

Oracle é forte como plataforma enterprise para:

- OLTP relacional crítico;
- OLAP/Data Warehouse corporativo;
- segurança, auditoria e compliance;
- alta disponibilidade e recuperação.

## 2. Multitenant em 30 segundos

- **CDB**: contêiner administrativo principal.
- **PDB**: banco isolado para aplicação.
- Conexão de aplicação normalmente na PDB (ex.: `FREEPDB1`).

SQL de validação:

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

## 3. Onde Oracle manda bem

- Relacional (OLTP): excelente.
- OLAP/DW: excelente.
- Spatial: excelente.
- JSON: muito bom.
- Vector (23c): em crescimento forte.
- Graph/Time Series: bom (com modelagem adequada).
- Streaming e Key-Value: suporte básico/limitado nativo.

## 4. ETL, Eventos e CDC (decisão rápida)

- **ETL**: `External Tables`, `SQL*Loader`, `Data Pump`, `Materialized Views`.
- **Eventos internos**: `Triggers`, `DBMS_SCHEDULER`, `Oracle AQ`.
- **CDC corporativo**: `GoldenGate` (Streams é legado).

Regra prática:

- evento interno no próprio banco: AQ resolve bem;
- integração com vários sistemas: usar CDC/fila externa e workers desacoplados.

## 5. Recursos multimodelo relevantes

- JSON nativo (`JSON_VALUE`, `JSON_TABLE`, etc.);
- espacial (`SDO_GEOMETRY`, índices espaciais);
- XML (`XMLType`, XPath/XQuery) para legados específicos;
- In-Memory (colunar em memória para acelerar analytics);
- vetores no 23c para busca semântica.

## 6. Comparação objetiva com mercado

- JSON 100% documento pesado: MongoDB pode ser mais natural.
- Busca vetorial especializada em larga escala: Pinecone/Weaviate podem simplificar.
- ETL distribuído de alto volume: Spark/DuckDB podem ser mais flexíveis.

Estratégia recomendada:

1. Oracle como core transacional e governança.
2. Motor especializado apenas quando houver ganho real.
3. Evitar centralizar tudo em uma única tecnologia por conveniência.

## 7. Conclusão para arquitetura moderna

Oracle funciona melhor como:

- núcleo confiável de dados e transações;
- base com segurança e HA robustas;
- fonte de eventos integrada a processamento externo.

Modelo recomendado: **Oracle no core + ecossistema desacoplado para analytics, IA e streaming em escala**.
