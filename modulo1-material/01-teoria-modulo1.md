# Módulo 1 - Teoria
## Arquitetura, Ferramentas Administrativas e Configuração do Ambiente

**Carga horária sugerida:** 4h  
**Distribuição sugerida:** 2h teoria + 2h prática

---

## 1. Objetivo do módulo

Ao final deste módulo, deveremos ser capazes de:

- compreender a estrutura básica do ambiente Oracle;
- diferenciar instância e banco de dados;
- reconhecer os principais componentes de memória, processos e arquivos;
- utilizar ferramentas administrativas básicas;
- conectar-se ao banco e consultar informações administrativas;
- compreender a lógica de parametrização inicial do ambiente.

---

## 2. Visão geral do módulo

Este módulo é a porta de entrada do curso. O objetivo não é cobrir todos os recursos do Oracle, e sim estabelecer base conceitual e operacional para os módulos seguintes.

Ao final desta unidade, precisaremos sair com cinco percepções claras:

1. o Oracle é um ambiente administrável, composto por estruturas, processos, arquivos e parâmetros;
2. administrar banco de dados não é apenas escrever SQL, mas observar, configurar, manter e recuperar o ambiente;
3. a arquitetura interna pode ser analisada por ferramentas e visões de sistema;
4. existe diferença entre memória, processos e estruturas em disco;
5. a configuração do banco influencia disponibilidade, desempenho e operação.

---

## 3. Papel do administrador Oracle

O DBA é o profissional responsável por manter o ambiente de banco de dados com segurança, estabilidade e desempenho adequado.

### Principais responsabilidades

- garantir disponibilidade para usuários e aplicações;
- controlar autenticação, privilégios e segurança;
- monitorar sessões, processos, recursos e alertas;
- acompanhar crescimento do banco e uso de armazenamento;
- administrar parâmetros, estruturas e objetos;
- executar rotinas operacionais, inclusive backup e recuperação;
- diagnosticar falhas, lentidão e gargalos;
- preparar o ambiente para escalabilidade e continuidade operacional.

---

## 4. Ferramentas administrativas e de apoio

A administração Oracle pode ser feita por múltiplas interfaces.

### 4.1. Cliente gráfico de consulta

Ferramentas como CloudBeaver permitem:

- abrir conexões;
- executar comandos SQL;
- consultar objetos do schema;
- visualizar tabelas, colunas e índices.

### 4.2. Ferramenta administrativa visual

Ferramentas como SQL Developer ajudam a visualizar:

- usuários;
- parâmetros;
- tablespaces;
- metadados e estrutura administrativa.

### 4.3. Linha de comando

Ferramentas de linha de comando e utilitários nativos do Oracle seguem essenciais para:

- administração remota;
- contingência;
- automação por script;
- manutenção operacional.

### 4.4. Visões administrativas

Além das interfaces, o Oracle fornece visões que tornam observáveis, por SQL, os componentes de arquitetura, operação e configuração.

---

## 5. Arquitetura do Oracle

No Módulo 1, a arquitetura deve ser entendida como integração entre memória, processos e arquivos.

### 5.1. Instância

A instância é o conjunto de memória e processos em execução que torna o banco operacional.

### 5.2. Banco de dados

O banco de dados é o conjunto de arquivos físicos persistidos em disco, incluindo:

- datafiles;
- redo log files;
- control files.

### 5.3. Diferença entre instância e banco de dados

- **Instância**: memória + processos em execução.
- **Banco de dados**: arquivos físicos armazenados em disco.

Quando o Oracle inicia, a instância é carregada e passa a abrir e administrar os arquivos do banco.

### 5.4. Modelo multitenant: definição básica

**Multitenant** é o modelo em que um banco contêiner hospeda bancos conectáveis.

- **CDB (Container Database)**: contêiner principal com estrutura administrativa comum;
- **PDB (Pluggable Database)**: banco conectável dentro do CDB, com isolamento lógico de dados e objetos.

Forma simples de explicar em aula:

- o CDB é o "prédio" administrativo;
- cada PDB é um "apartamento" com seus próprios objetos de aplicação.

Pontos didáticos essenciais:

1. um CDB pode conter uma ou mais PDBs;
2. a conexão da aplicação normalmente ocorre na PDB;
3. em laboratório, é comum usar o service name `FREEPDB1`.

Exemplo conceitual:

- comando `SELECT * FROM v$pdbs;` mostra as PDBs abertas no CDB;
- ao conectar em `FREEPDB1`, as operações do sistema/aplicação ocorrem nessa PDB.

---

## 6. Estruturas de memória

A memória influencia concorrência, tempo de resposta e consumo de recursos.

### 6.1. SGA

A **System Global Area (SGA)** é a memória compartilhada da instância, usada por múltiplos processos e sessões.

Exemplo didático:

- quando diferentes sessões executam consultas, o cache compartilhado da SGA pode reaproveitar blocos e SQL já processados.

### 6.2. PGA

A **Program Global Area (PGA)** é a memória privada de cada processo servidor.

Exemplo objetivo de processo:

- ao executar um `SELECT` com `ORDER BY`, o processo servidor da sessão pode usar PGA para ordenação;
- ao executar `CREATE INDEX`, o processo usa PGA para operações internas de construção do índice;
- em cargas com muitas sessões simultâneas, cada processo consome sua própria PGA.

### 6.3. Síntese didática

- SGA: memória compartilhada da instância;
- PGA: memória individual por processo;
- configuração de memória impacta desempenho e estabilidade.

---

## 7. Processos de background

O Oracle utiliza processos internos para operação contínua do ambiente.

Neste módulo, devemos fixar que:

- há processos responsáveis por escrita em disco, recuperação e manutenção;
- a instância não depende apenas da sessão do usuário;
- processos de background são parte estrutural da confiabilidade do banco.

Exemplos introdutórios úteis:

- **DBWn**: grava blocos alterados da memória para datafiles;
- **LGWR**: grava registros de redo em redo logs;
- **SMON/PMON**: apoio em recuperação e limpeza operacional.

---

## 8. Arquivos físicos e estruturas lógicas

### 8.1. Arquivos físicos

- **Datafiles**: armazenam dados persistidos;
- **Redo log files**: registram alterações para recuperação;
- **Control files**: armazenam metadados estruturais do banco.

### 8.2. Estruturas lógicas

- **Tablespaces**: agrupamento lógico de armazenamento;
- **Segmentos**: estruturas associadas a objetos, como tabelas e índices;
- **Extents**: conjuntos de blocos alocados para segmentos;
- **Blocks**: menor unidade de armazenamento e I/O.

### 8.3. Relação físico x lógico

A administração ocorre no plano lógico, mas a persistência e recuperação ocorrem no plano físico.

Exemplo de associação:

- uma tabela pertence a um segmento;
- o segmento ocupa extents;
- os extents estão em datafiles de um tablespace.

---

## 9. Parametrização e configuração

Parâmetros controlam comportamento, capacidade e operação da instância.

### 9.1. O que são parâmetros

Controlam, por exemplo:

- memória;
- processos;
- sessões;
- comportamento de execução;
- uso de recursos.

### 9.2. PFILE e SPFILE

- **PFILE**: arquivo texto, editável manualmente;
- **SPFILE**: arquivo de parâmetros persistente, gerenciado pelo Oracle.

Exemplo didático de PFILE (texto):

```ini
*.memory_target=1G
*.processes=300
*.open_cursors=500
```

Interpretação rápida:

- `*.memory_target=1G`: define meta geral de memória;
- `*.processes=300`: limite aproximado de processos;
- `*.open_cursors=500`: quantidade de cursores por sessão.

Exemplo didático de uso de SPFILE:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'spfile';

ALTER SYSTEM SET open_cursors = 500 SCOPE=BOTH;
```

Interpretação rápida:

- `SELECT ... FROM v$parameter WHERE name = 'spfile'` indica o arquivo SPFILE em uso;
- com `SCOPE=BOTH`, a alteração vale em memória agora e persiste no SPFILE para próximo restart.

### 9.3. O que devemos explicar

- parâmetros definem como a instância inicia e opera;
- parte dos parâmetros é dinâmica;
- parte das alterações exige reinicialização.

Exemplo prático:

- `open_cursors` pode ser ajustado para ampliar cursores por sessão;
- `processes` e `sessions` afetam capacidade concorrente do ambiente.

---

## 10. Dicionário de dados e visões de sistema

A consulta administrativa deve ser feita por dicionário de dados e visões dinâmicas de desempenho.

### 10.1. Famílias do dicionário de dados

- **USER_***: objetos do usuário conectado;
- **ALL_***: objetos acessíveis ao usuário;
- **DBA_***: visão administrativa ampla, com privilégios elevados.

### 10.2. Visões dinâmicas (`V$`)

Exemplos centrais do módulo:

- `V$INSTANCE`
- `V$DATABASE`
- `V$VERSION`
- `V$SGA`
- `V$PARAMETER`
- `V$PROCESS`
- `V$BGPROCESS`
- `V$SESSION`
- `V$DATAFILE`
- `V$LOGFILE`
- `V$CONTROLFILE`
- `V$PDBS`

### 10.3. Como ler essas visões em sala

- usar `V$` para estado operacional atual;
- usar `DBA_*` para visão administrativa ampla;
- usar `USER_*`/`ALL_*` para demonstrar escopo de acesso por privilégio.

---

## 11. Privilégios úteis para o Módulo 1

Devemos introduzir privilégios de forma objetiva, sem aprofundar segurança avançada.

### Conceitos básicos

- privilégio de sistema;
- privilégio de objeto;
- role (agrupamento de privilégios).

### Exemplos para demonstração

- `CREATE SESSION`
- `CREATE TABLE`
- `SELECT_CATALOG_ROLE`
- `DBA` (somente demonstração controlada)

Exemplo didático:

- um usuário com apenas `CREATE SESSION` conecta, mas não administra;
- com `SELECT_CATALOG_ROLE`, passa a consultar mais visões de catálogo.

---

## 12. Ponte entre teoria e prática

A transição didática deve seguir a lógica **conceito -> evidência técnica -> operação**.

- conceito: instância, banco, memória, processos, arquivos, parâmetros e privilégios;
- evidência técnica: consultas em `V$`, `DBA_*`, `ALL_*` e `USER_*`;
- operação: conexão por service name da PDB (ex.: `FREEPDB1`) e validação por SQL.

---

## 13. Fechamento conceitual do módulo

Ao final do módulo, o entendimento esperado é:

- distinção clara entre instância e banco de dados;
- noção objetiva de SGA e PGA;
- noção objetiva de multitenant, CDB e PDB;
- entendimento da relação entre estruturas lógicas e arquivos físicos;
- uso inicial de dicionário de dados, visões `V$` e parâmetros como base de administração.

---

## 14. Trilha de aprofundamento (material extra)

Para evolução após este módulo introdutório, usar como referência complementar:

- [Oracle - Guia Full](./oracle_guia_full.md)

Este guia amplia tópicos como engenharia de dados, eventos, integração, segurança avançada, alta disponibilidade e recursos multimodelo.
