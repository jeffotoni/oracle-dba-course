# Módulo 0: Fundamentos de Banco de Dados, Oracle e Decisão Técnica

> Evolução do armazenamento de dados, surgimento dos SGBDs, modelo relacional, Oracle no mercado e panorama atual com NoSQL, bancos vetoriais, cloud e IA.

## 1. Visão Geral
Este módulo prepara a base conceitual para todo o curso. A ideia é sair daqui entendendo **por que bancos de dados existem**, como os SGBDs resolveram problemas clássicos de armazenamento, por que o modelo relacional continua importante e como o Oracle se posiciona em ambientes reais.

Além da teoria, o módulo também conecta tecnologia com decisão prática: edição Oracle, custo, licenciamento, escala vertical/horizontal, cloud, Autonomous Database, Exadata, RAC e o papel do DBA moderno.

Em outras palavras: este módulo não é apenas uma introdução. Ele é o mapa inicial para entender banco de dados como **tecnologia, arquitetura, operação e decisão de negócio**.

## 2. Objetivos de Aprendizagem
Ao concluir o módulo, você deve conseguir:
- Explicar a diferença entre arquivos isolados, banco de dados e SGBD.
- Descrever a evolução dos modelos de dados: arquivos, hierárquico, rede, relacional, NoSQL, vetorial e cloud.
- Entender os fundamentos do modelo relacional, incluindo tabelas, chaves, schema, normalização e SQL.
- Descrever, com exemplos simples, os princípios ACID e o Teorema CAP.
- Identificar as principais edições e linhas Oracle: XE, Free, SE2, EE, RAC, Exadata e Autonomous.
- Avaliar, em alto nível, custo, licenciamento, TCO e critérios de decisão inicial em Oracle.
- Diferenciar escala vertical, Data Guard, Active Data Guard, RAC, Exadata e Sharding.
- Reconhecer os principais modelos de banco no mercado e seus casos de uso.
- Entender o papel do DBA em segurança, disponibilidade, performance, custo, cloud e conformidade.

## 3. Mapa do Módulo

| Bloco | Tema | Resultado esperado |
| :--- | :--- | :--- |
| **Fundamentos** | Arquivos isolados, SGBD, schema, chaves e normalização | Entender por que bancos de dados surgiram |
| **Modelo relacional** | SQL, ACID, transações e integridade | Compreender a base dos bancos corporativos |
| **Oracle no tempo** | Linha histórica do Oracle e evolução para 23ai | Situar versões e marcos importantes |
| **Edições Oracle** | XE, Free, SE2, EE, RAC, Exadata e Autonomous | Escolher edição conforme cenário |
| **Custo e escala** | Licenciamento, TCO, vertical, horizontal, cloud e multicloud | Conectar arquitetura com orçamento |
| **Panorama atual** | NoSQL, OLAP, grafos, vetoriais, lakehouse e IA | Entender onde Oracle se encaixa no ecossistema moderno |
| **Carreira DBA** | Segurança, backup, performance, disponibilidade e cloud | Visualizar responsabilidades reais do DBA |

## 4. Materiais Complementares

- [Guia de Licenciamento e Custos Oracle](./oracle-custo.md): aprofunda custo, TCO, licenciamento, cloud, escala vertical/horizontal, RAC, Exadata e matriz de decisão.

## 5. Pré-requisitos
- Leitura prévia: noções básicas de sistemas, arquivos, redes e aplicações web.
- Ferramentas: editor de texto, navegador e acesso ao material do curso.

## 6. Antes dos Bancos de Dados
Antes dos SGBDs, os dados ficavam em arquivos separados por sistema ou departamento. Esse modelo gerava três problemas clássicos:
- Redundância: o mesmo dado repetido em vários lugares.
- Inconsistência: cada sistema acabava com uma versão diferente da verdade.
- Concorrência ruim: alteração simultânea quase sempre virava conflito.

Exemplo prático:
- Se o cliente muda de endereço, a atualização precisa ser repetida em faturamento, CRM, cobrança e logística.
- Quando uma dessas áreas não atualiza, o dado fica divergente e a operação quebra.

## 7. Evolução do Oracle em Linha do Tempo
- 1970: Edgar F. Codd publica o modelo relacional na IBM.
- 1977: Larry Ellison, Bob Miner e Ed Oates fundam a SDL.
- 1979: Oracle V2 é lançado comercialmente com SQL.
- 1992: Oracle 7 fortalece PL/SQL e triggers.
- 2001: Oracle 9i introduz RAC de forma madura para alta disponibilidade.
- 2013: Oracle 12c populariza a arquitetura Multitenant.
- 2024: Oracle 23ai amplia capacidades nativas para IA e vetores.

### 7.1 Evolução histórica dos modelos de dados
A história dos dados não começa no relacional. A evolução aconteceu em etapas:
- Arquivos isolados: cada sistema guardava seus próprios dados, com alta redundância.
- Modelo hierárquico: organização em árvore, bom para estruturas rígidas.
- Modelo em rede: mais flexível que o hierárquico, mas complexo de manter.
- Modelo relacional: tabelas, chaves e linguagem SQL padronizada.
- NoSQL e distribuídos: foco em escala horizontal e novos tipos de carga.
- Modelos modernos para IA: bancos vetoriais e arquiteturas lakehouse.

Esse caminho explica por que o modelo relacional segue central em sistemas críticos, mesmo com novas tecnologias no mercado.

## 8. Regras que Governam os Dados

### 8.0 Nascimento dos SGBDs e conceitos gerais
Os SGBDs nasceram para resolver problemas dos arquivos isolados: redundância, inconsistência e baixa concorrência.

Conceitos gerais que formam a base de administração:
- Banco de dados: conjunto organizado de dados com regras de acesso.
- SGBD: software que controla armazenamento, segurança e concorrência.
- Esquema (schema): estrutura lógica de tabelas, colunas e relacionamentos.
- Chave primária (PK): identifica um registro de forma única.
- Chave estrangeira (FK): liga tabelas e protege integridade referencial.
- Normalização: técnica para reduzir redundância e anomalias de atualização.

### 8.1 ACID
**ACID** é a base do comportamento transacional em bancos relacionais:
- **Atomicidade:** ou a transação acontece inteira, ou não acontece.
- **Consistência:** o banco sai de um estado válido para outro estado válido.
- **Isolamento:** transações concorrentes não devem se corromper.
- **Durabilidade:** após confirmar, o dado persiste mesmo com falha.

### 8.2 CAP em linguagem prática
CAP é a sigla para:
- **C (Consistency):** todos os nós enxergam o mesmo dado ao mesmo tempo.
- **A (Availability):** toda requisição recebe resposta, mesmo com parte do sistema degradada.
- **P (Partition Tolerance):** o sistema continua operando mesmo com falhas de comunicação entre nós.

Em sistemas distribuídos, o Teorema CAP mostra que, na presença de partição de rede, não dá para maximizar ao mesmo tempo consistência forte e disponibilidade total.

Resumo útil para o dia a dia:
- Oracle tradicional em arquitetura centralizada prioriza consistência transacional.
- Sistemas web massivos, em alguns casos, aceitam consistência eventual para manter disponibilidade.

### 8.3 Linguagens principais no SQL
No dia a dia de DBA e desenvolvedor, SQL costuma ser dividido assim:

| Grupo | Significado | Para que serve | Exemplo |
| :--- | :--- | :--- | :--- |
| **DDL** | Data Definition Language | Definir estrutura de objetos | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| **DML** | Data Manipulation Language | Inserir, alterar e remover dados | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** | Data Query Language | Consultar dados | `SELECT` |
| **DCL** | Data Control Language | Permissões e segurança | `GRANT`, `REVOKE` |
| **TCL** | Transaction Control Language | Controle transacional | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

### 8.4 Conceitos técnicos importantes

| Conceito | O que é | Impacto prático |
| :--- | :--- | :--- |
| **Índice** | Estrutura auxiliar para acelerar busca | Reduz custo de leitura, pode aumentar custo de escrita |
| **B-Tree** | Estrutura de índice balanceada para busca por faixa e igualdade | Muito usada em índices padrão de bancos relacionais |
| **Hash** | Estrutura orientada a comparação direta por chave | Boa para igualdade, menos eficiente para faixa ordenada |
| **Join** | Operação que combina linhas entre tabelas relacionadas | Fundamental para relatórios e consultas de negócio |
| **Transação** | Unidade lógica de trabalho com garantia ACID | Protege consistência em operações críticas |

### 8.5 Ponte para a arquitetura Oracle

Antes de entrar no laboratório, vale fixar uma leitura mental simples da arquitetura Oracle:

```txt
Oracle Instance
 └── CDB
      └── PDB
           └── User
                └── Schema
                     └── Tables
                          └── Rows
```

Essa leitura ajuda a ligar a teoria relacional ao ambiente real do curso:

- a **instância** é o motor Oracle em execução;
- o **CDB** é o container principal;
- a **PDB** é o banco lógico de trabalho;
- o **user** é a identidade de acesso;
- o **schema** é o espaço lógico associado ao usuário;
- as **tables** guardam os dados consultados e manipulados por SQL.

Uma analogia simples ajuda bastante no início:

- **CDB** = prédio;
- **PDB** = empresa;
- **user/schema** = sala;
- **table** = armário;
- **rows** = documentos.

No laboratório do curso, essa hierarquia normalmente aparece assim:

```txt
FREE
 └── FREEPDB1
      └── USER / SCHEMA
           └── TABLE
```

Em linguagem prática:

- `FREE` representa a instância e o container principal;
- `FREEPDB1` representa o banco lógico de trabalho;
- em vez de pensar primeiro em `CREATE DATABASE`, o fluxo inicial é pensar em `CREATE USER`, `CREATE TABLE` e queries dentro da `FREEPDB1`;
- `CREATE PLUGGABLE DATABASE` existe, mas entra como tema avançado, não como primeiro passo do laboratório.

Essa ponte é importante porque prepara a entrada no `modulo0-guia-pratico`, onde essa estrutura passa a ser observada na IDE e nas queries do ambiente.

## 9. Edições Oracle e Decisão Inicial

Antes de instalar Oracle, subir um container ou estimar custo, a primeira decisão é entender **qual edição ou serviço combina com o objetivo do projeto**.

Para estudo, laboratório e desenvolvimento local, normalmente faz sentido começar por **Oracle XE** ou **Oracle Free**. Para produção corporativa, a decisão passa por custo, suporte, recursos avançados, alta disponibilidade, cloud e requisitos de negócio.

### 9.1 Visão resumida para decisão inicial

| Edição | Perfil de Uso | Características principais |
| :--- | :--- | :--- |
| **Express Edition (XE)** | Estudo, laboratório e protótipo | Gratuita, simples para aprender e testar; possui limites de CPU, RAM e armazenamento. |
| **Oracle Database Free** | Desenvolvimento moderno, aprendizado e pequenos testes | Gratuita, atual, boa para laboratórios com versões recentes do Oracle. |
| **Standard Edition 2 (SE2)** | Pequenas e médias cargas corporativas | Menor custo que EE, boa para workloads previsíveis, mas com menos recursos avançados. |
| **Enterprise Edition (EE)** | Missão crítica e ambientes corporativos robustos | Mais recursos, maior flexibilidade de arquitetura e possibilidade de options/add-ons pagos. |
| **Cloud / Autonomous** | Projetos em nuvem, elasticidade e operação gerenciada | Cobrança por consumo ou assinatura; reduz esforço operacional, mas exige controle financeiro. |

### 9.2 Matriz completa de versões e linhas Oracle

A tabela abaixo amplia a visão anterior e ajuda a posicionar versões antigas, versões atuais, opções enterprise e serviços cloud.

| Oracle Edition / Versão | Nome comercial / Linha | Licenciamento / Cobrança | Limites principais | Suporte / Status | Uso mais comum no mercado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Oracle XE 11g** | Express Edition | Gratuito | Muito limitado em CPU, RAM e storage | Legado / obsoleto | Sistemas antigos, homologação e labs legados |
| **Oracle XE 18c** | Express Edition | Gratuito | Limitado | Dev/teste | Laboratórios e pequenos ambientes |
| **Oracle XE 21c** | Express Edition | Gratuito | Limitado | Dev/teste | Desenvolvimento local e aprendizado |
| **Oracle Free 23ai** | Oracle Database Free | Gratuito | Limites para desenvolvimento e small scale | Atual | Desenvolvimento moderno, aprendizado e protótipos |
| **Oracle 12c SE / SE2** | Standard Edition / Standard Edition 2 | Pago, licença + suporte | Menos recursos avançados que EE | Muito usado em legado corporativo | ERPs e sistemas médios |
| **Oracle 12c EE** | Enterprise Edition | Alto custo | Recursos enterprise; options pagas separadas | Ainda presente em legado | Grandes empresas e sistemas críticos antigos |
| **Oracle 18c SE2** | Standard Edition 2 | Pago | Moderado | Menos comum que 19c | Migrações e ambientes específicos |
| **Oracle 18c EE** | Enterprise Edition | Alto custo | Enterprise + options | Menos adotado | Casos específicos |
| **Oracle 19c SE2** | Standard Edition 2 | Pago | Moderado | LTS / muito forte | PMEs, ERP e produção estável |
| **Oracle 19c EE** | Enterprise Edition | Alto custo | Enterprise completo + add-ons | LTS / padrão corporativo | Produção crítica |
| **Oracle 21c SE2** | Standard Edition 2 | Pago | Moderado | Innovation Release | Projetos novos não-LTS e validações de recursos |
| **Oracle 21c EE** | Enterprise Edition | Alto custo | Recursos modernos | Innovation Release | Inovação e transição tecnológica |
| **Oracle 23ai SE2** | Nova geração / linha comercial aplicável | Pago | Modernizado | Emergente | Novos projetos com linha atual |
| **Oracle 23ai EE** | AI Database / Enterprise | Premium alto | Vector, AI, recursos enterprise e options | Atual | IA corporativa, modernização e workloads críticos |
| **Oracle RAC** | Real Application Clusters, add-on de EE | Muito alto / extra | Alta disponibilidade horizontal | Enterprise | Bancos, telecom, missão crítica e baixa tolerância a indisponibilidade |
| **Oracle Exadata** | Appliance + software Oracle | Muito alto | Infraestrutura + software premium | Top tier | Grandes corporações, performance extrema e consolidação |
| **Oracle Cloud Database Service** | OCI Base Database Service | Assinatura cloud, OCPU/ECPU + storage | Conforme plano | Cloud ativo | Lift-and-shift de Oracle tradicional para OCI |
| **Oracle Autonomous Transaction Processing (ATP)** | OCI Autonomous Database | Consumo cloud | Oracle gerencia tuning, patch e parte da operação | Cloud premium | Aplicações transacionais com operação automatizada |
| **Oracle Autonomous Data Warehouse (ADW)** | OCI Autonomous Database | Consumo cloud | Foco em analytics | Cloud premium | BI, Data Warehouse e workloads analíticos |
| **Oracle Always Free Autonomous DB** | OCI Free Tier | Gratuito, com limites | Recursos limitados | Cloud dev | Aprendizado, protótipo e testes sem custo |
| **Oracle Database@Azure** | Oracle + Microsoft Cloud | Consumo enterprise cloud | Conforme contrato e região | Corporativo | Integração Azure + Oracle com baixa latência |
| **Oracle Database@AWS** | Oracle em parceria/arquitetura multicloud | Variável | Depende da arquitetura e contrato | Corporativo | Migração híbrida e aproximação entre Oracle e ecossistema AWS |

### 9.3 Atalho mental para escolher

| Situação | Caminho provável | Por quê |
| :--- | :--- | :--- |
| Quero aprender Oracle localmente | **Oracle XE 21c** ou **Oracle Free 23ai** | Gratuito, simples e suficiente para laboratório. |
| Quero fazer laboratório com recursos mais atuais | **Oracle Free 23ai** | Aproxima o aluno da linha moderna do Oracle Database. |
| Tenho sistema legado Oracle | **11g / 12c / 19c** | São versões muito encontradas em empresas. |
| Quero produção estável tradicional | **Oracle 19c SE2 ou EE** | 19c é referência forte em ambientes corporativos. |
| Tenho pequena ou média carga previsível | **SE2** | Custo menor que EE e boa aderência a workloads mais simples. |
| Tenho missão crítica e requisitos avançados | **EE** | Mais recursos, options e flexibilidade arquitetural. |
| Preciso de alta disponibilidade horizontal | **EE + RAC** | RAC é opção enterprise para cenários críticos. |
| Quero cloud Oracle tradicional | **OCI Base Database Service** | Leva o modelo Oracle tradicional para nuvem. |
| Quero operação mais automatizada | **Autonomous ATP/ADW** | Oracle automatiza tuning, patch e parte da administração. |
| Quero estudar cloud sem custo | **Always Free Autonomous DB** | Bom para aprendizado e protótipos pequenos. |

### 9.4 Pontos importantes para lembrar

- **XE / Free**: grátis, bons para estudo, laboratório e desenvolvimento.
- **SE2**: pago, custo moderado, indicado para cargas menores e previsíveis.
- **EE**: caro, indicado para missão crítica e recursos enterprise.
- **EE + RAC / Exadata**: muito caro, usado quando disponibilidade, escala e performance justificam o investimento.
- **Cloud Autonomous**: assinatura recorrente, com menos esforço operacional.
- **12c** foi um marco por popularizar o modelo **multitenant** com `CDB` e `PDB`, além de iniciar uma orientação mais forte para cloud.
- **19c** continua muito relevante como base corporativa estável.
- **23ai / Free 23ai** aproximam o estudo da geração mais nova, com foco moderno e recursos ligados a IA.

Leitura complementar:
- [Guia de Licenciamento e Custos Oracle](./oracle-custo.md)

## 10. Panorama Atual dos Modelos de Banco

Hoje, falar de "banco de dados" significa lidar com famílias diferentes de tecnologias. O ponto principal é escolher o modelo pelo problema de negócio, não por moda.

| Modelo | Quando usar | Exemplos (links oficiais) |
| :--- | :--- | :--- |
| **Relacional (SQL)** | OLTP, ERP, financeiro, dados com integridade forte | [Oracle Database](https://www.oracle.com/database/), [PostgreSQL](https://www.postgresql.org/), [SQL Server](https://www.microsoft.com/sql-server) |
| **Documentos (NoSQL)** | Catálogos, perfis, conteúdo com schema flexível | [MongoDB](https://www.mongodb.com/), [Couchbase](https://www.couchbase.com/), [Firestore](https://firebase.google.com/docs/firestore) |
| **Chave-valor (NoSQL)** | Cache, sessão, leitura e escrita com latência baixa | [Redis](https://redis.io/), [Aerospike](https://aerospike.com/), [Valkey](https://valkey.io/) |
| **Colunar distribuído (NoSQL)** | Grandes volumes com escala horizontal e alta escrita | [Apache Cassandra](https://cassandra.apache.org/), [ScyllaDB](https://www.scylladb.com/), [Apache HBase](https://hbase.apache.org/) |
| **Séries temporais** | Observabilidade, IoT, métricas, telemetria | [InfluxDB](https://www.influxdata.com/), [Timescale](https://www.timescale.com/), [VictoriaMetrics](https://victoriametrics.com/) |
| **Grafos** | Fraude, recomendação por relacionamento, redes complexas | [Neo4j](https://neo4j.com/), [JanusGraph](https://janusgraph.org/), [TigerGraph](https://www.tigergraph.com/) |
| **Vetorial** | Busca semântica, RAG, similaridade de embeddings | [Qdrant](https://qdrant.tech/), [Milvus](https://milvus.io/), [Weaviate](https://weaviate.io/), [Pinecone](https://www.pinecone.io/) |
| **Analítico colunar (OLAP)** | BI, agregações pesadas, consultas de leitura massiva | [ClickHouse](https://clickhouse.com/), [DuckDB](https://duckdb.org/), [Snowflake](https://www.snowflake.com/) |
| **Data Warehouse cloud** | Camada analítica corporativa com governança central | [BigQuery](https://cloud.google.com/bigquery), [Amazon Redshift](https://aws.amazon.com/redshift/), [Azure Synapse](https://azure.microsoft.com/products/synapse-analytics/) |
| **NewSQL distribuído** | SQL com consistência forte e escala horizontal | [CockroachDB](https://www.cockroachlabs.com/), [YugabyteDB](https://www.yugabyte.com/), [TiDB](https://www.pingcap.com/tidb/) |
| **Busca e indexação** | Full text search, logs e observabilidade de busca | [Elasticsearch](https://www.elastic.co/elasticsearch), [OpenSearch](https://opensearch.org/), [Solr](https://solr.apache.org/) |
| **Ecossistema Big Data (armazenamento + processamento)** | Pipelines distribuídos, data lake, ETL/ELT em escala | [Apache Hadoop](https://hadoop.apache.org/), [Apache Spark](https://spark.apache.org/), [Databricks](https://www.databricks.com/) |

## 11. Linguagens e Perfil de Implementação
A linguagem de implementação não define sozinha a qualidade do banco, mas ajuda a entender escolhas de desempenho e ecossistema.

| Tecnologia | Linguagens principais (links oficiais) | Perfil técnico |
| :--- | :--- | :--- |
| **Oracle Database** | [C](https://en.cppreference.com/w/c), [C++](https://isocpp.org/) | Relacional robusto para workloads críticos e alta maturidade operacional. |
| **PostgreSQL** | [C](https://en.cppreference.com/w/c), [SQL](https://www.iso.org/standard/9075.html) | Relacional open source forte em extensibilidade e compliance SQL. |
| **MySQL** | [C](https://en.cppreference.com/w/c), [C++](https://isocpp.org/) | Relacional muito usado em aplicações web e sistemas de médio porte. |
| **MongoDB** | [C++](https://isocpp.org/), [JavaScript](https://developer.mozilla.org/docs/Web/JavaScript) | Banco de documentos com schema flexível e ciclo rápido de mudança. |
| **Redis** | [C](https://en.cppreference.com/w/c) | Chave-valor para cache, sessão e workloads de baixa latência. |
| **Apache Cassandra** | [Java](https://www.oracle.com/java/) | NoSQL distribuído orientado a alta escrita e disponibilidade. |
| **Neo4j** | [Java](https://www.oracle.com/java/) | Banco de grafos para relacionamento complexo e consultas por conexão. |
| **CockroachDB** | [Go](https://go.dev/) | NewSQL distribuído com foco em resiliência e escala geográfica. |
| **Qdrant** | [Rust](https://www.rust-lang.org/) | Vetorial otimizado para recuperação semântica por embeddings. |
| **ClickHouse** | [C++](https://isocpp.org/) | OLAP colunar para analytics de alta performance. |
| **DuckDB** | [C++](https://isocpp.org/) | Analítico embutido para exploração local de dados. |
| **Apache Spark** | [Scala](https://www.scala-lang.org/), [Java](https://www.oracle.com/java/), [Python](https://www.python.org/) | Engine distribuída para ETL, engenharia de dados e ML. |
| **Apache Hadoop** | [Java](https://www.oracle.com/java/) | Ecossistema de armazenamento e processamento distribuído em larga escala. |

## 12. Papel do DBA no Mercado Brasileiro
O DBA atual combina operação técnica com visão de negócio:
- Disponibilidade e recuperação: backup, restore, DR e continuidade.
- Segurança e conformidade: acesso, criptografia, trilha de auditoria e LGPD.
- Performance e custo: tuning, capacidade e governança de consumo.
- Arquitetura cloud: desenho de ambientes Oracle em OCI e modelos multicloud.

### 12.1 Faixa salarial mensal de DBA no Brasil
Referência de mercado com base em dados CAGED consolidados no Portal Salário.

| Nível | Média mensal (R$) | Fonte |
| :--- | :--- | :--- |
| **Júnior** | **7.604,04** | [Portal Salário - Administrador de Banco de Dados](https://www.salario.com.br/profissao/administrador-de-banco-de-dados-cbo-212305/) |
| **Pleno** | **10.196,91** | [Portal Salário - Administrador de Banco de Dados](https://www.salario.com.br/profissao/administrador-de-banco-de-dados-cbo-212305/) |
| **Sênior** | **13.196,49** | [Portal Salário - Administrador de Banco de Dados](https://www.salario.com.br/profissao/administrador-de-banco-de-dados-cbo-212305/) |

### 12.2 Faixas observadas em vagas Oracle e Oracle Cloud
Esses valores variam por cidade, regime de contratação (CLT ou PJ), escopo funcional e nível de especialização.

| Perfil | Faixa mensal observada (R$) | Fonte |
| :--- | :--- | :--- |
| **DBA Pleno com Oracle e OCI** | **8.000** | [Indeed - DBA Pleno (SP)](https://br.indeed.com/viewjob?jk=fb589a649937f681) |
| **DBA Oracle Sênior com OCI/AWS** | **12.000 a 14.000** | [Glassdoor Jobs - DBA Oracle Sênior](https://www.glassdoor.com.br/Vaga/exadata-oracle-vagas-SRCH_KE0%2C14.htm) |
| **Oracle Cloud ERP Financials Pleno** | **8.000 a 12.000** | [Indeed - Oracle Cloud ERP Financials Pleno](https://br.indeed.com/q-oracle-cloud-l-rio-de-janeiro%2C-rj-vagas.html) |
| **Consultor Funcional Oracle Fusion Cloud** | **15.000 a 20.000** | [Indeed - Consultor Funcional ERP Oracle Fusion](https://br.indeed.com/q-consultor-oracle-erp-vagas.html) |
| **Consultor Oracle Cloud (estimativa agregada)** | **3.000 a 16.000** | [Glassdoor - Consultor Oracle Cloud (Brasil)](https://www.glassdoor.com.br/Sal%C3%A1rios/consultor-oracle-cloud-sal%C3%A1rio-SRCH_KO0%2C22.htm) |

### 12.3 Por que ainda faz sentido estudar Oracle hoje
Mesmo com muitas opções no mercado, Oracle segue relevante por motivos objetivos:
- Base instalada grande em setores críticos como finanças, telecom, governo e varejo.
- Forte maturidade operacional em segurança, backup, recuperação e alta disponibilidade.
- Ecossistema amplo de recursos enterprise para missão crítica.
- Presença consistente em nuvem com OCI, Autonomous e estratégias multicloud.
- Alta demanda por profissionais capazes de equilibrar performance, risco e custo.

## 13. Perguntas de Revisão
1. Qual problema principal os SGBDs resolveram em relação a arquivos isolados?
2. Qual a diferença prática entre atomicidade e consistência no ACID?
3. Em que tipo de cenário consistência eventual pode ser aceitável?
4. Quando a edição XE é suficiente para um projeto?
5. O que muda no papel do DBA com a chegada da nuvem?
6. Por que licenciamento impacta decisão técnica?
7. Dê um caso onde banco vetorial é mais adequado que relacional.
8. Dê um caso onde relacional é mais adequado que NoSQL.
9. Qual é a relação entre LGPD e administração de banco?
10. Qual decisão errada no início do projeto mais costuma gerar retrabalho?

## 14. Gabarito Resumido
1. Integridade, consistência e concorrência segura dos dados.
2. Atomicidade é tudo ou nada na transação, consistência é manter regras válidas do modelo.
3. Ambientes distribuídos com foco em disponibilidade e escala.
4. Estudo, POC e pequenos ambientes sem exigência de alta escala.
5. Amplia para automação, custos, arquitetura multicloud e governança.
6. Porque define viabilidade financeira e limites de arquitetura.
7. Busca semântica, recomendação por similaridade e RAG.
8. Transações financeiras, pedidos e controle de estoque consistente.
9. Exige proteção de dados pessoais, auditoria e retenção adequada.
10. Escolher arquitetura sem considerar crescimento, custo e compliance.

## 15. Referências

### 15.1 Oracle e Oracle Cloud
- [Oracle AI Database 26ai - Licensing](https://docs.oracle.com/en/database/oracle/oracle-database/26/licensing.html)
- [Oracle AI Database 26ai - New Features](https://docs.oracle.com/en/database/oracle/oracle-database/26/nfcoa/index.html)
- [Oracle Cloud Infrastructure - Documentação](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Oracle Cloud Price List](https://www.oracle.com/cloud/price-list/)
- [Oracle Database Pricing](https://www.oracle.com/database/pricing/)
- [Oracle Base Database Service Pricing](https://www.oracle.com/br/database/base-database-service/pricing/)
- [Oracle Database Service for Azure](https://www.oracle.com/cloud/azure/oracle-database-for-azure/)
- [Oracle Database@Azure Pricing](https://www.oracle.com/cloud/azure/oracle-database-at-azure/pricing/)
- [Oracle Database@AWS GA Announcement (08/07/2025)](https://www.oracle.com/news/announcement/oracle-database-at-aws-now-generally-available-2025-07-08/)
- [Oracle Database@Google Cloud GA Announcement (09/09/2024)](https://blogs.oracle.com/cloud-infrastructure/post/general-availability-oracle-database-google-cloud)

### 15.2 Mercado de trabalho e salários
- [Portal Salário - Administrador de Banco de Dados (CBO 2123-05)](https://www.salario.com.br/profissao/administrador-de-banco-de-dados-cbo-212305/)
- [VAGAS - Mapa de Carreiras: Administrador de Banco de Dados](https://www.vagas.com.br/mapa-de-carreiras/cargos/administrador-de-banco-de-dados)
- [Glassdoor - Salário de Consultor Oracle Cloud (Brasil)](https://www.glassdoor.com.br/Sal%C3%A1rios/consultor-oracle-cloud-sal%C3%A1rio-SRCH_KO0%2C22.htm)
- [Indeed - DBA Pleno (SP)](https://br.indeed.com/viewjob?jk=fb589a649937f681)
- [Indeed - Oracle Cloud ERP Financials Pleno](https://br.indeed.com/q-oracle-cloud-l-rio-de-janeiro%2C-rj-vagas.html)
- [Indeed - Consultor Funcional ERP Oracle Fusion](https://br.indeed.com/q-consultor-oracle-erp-vagas.html)

### 15.3 Material do curso
- [Guia de Licenciamento e Custos Oracle](./oracle-custo.md)
- [Hub de referências do repositório](../README.md#referências-e-links-úteis)
