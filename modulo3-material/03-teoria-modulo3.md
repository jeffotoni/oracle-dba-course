# Módulo 3 - Rotinas de Backup e Recuperação

## Visão geral

Este módulo deverá consolidar um dos pilares mais críticos da administração de bancos de dados: a capacidade de proteger informações e restaurar a operação diante de falhas.

Em ambientes corporativos, não basta manter o banco disponível em condições normais. Deveríamos também planejar como preservar os dados, como recuperar o ambiente após incidentes e como reduzir o tempo de indisponibilidade em situações de falha.

A administração de backup e recuperação envolve técnica, planejamento e disciplina operacional. Este módulo organiza esses elementos em uma visão teórica estruturada, preparando o caminho para a prática com rotinas de backup, restauração e recuperação.

---

## Carga horária sugerida

5 horas

**Distribuição sugerida:**  
2 horas de teoria + 3 horas de prática

---

## Objetivos do módulo

Ao final deste módulo, deveríamos ter consolidado os seguintes entendimentos:

- compreender a importância estratégica de backup e recuperação;
- distinguir backup de recuperação;
- diferenciar backup lógico de backup físico;
- distinguir backup frio de backup quente;
- compreender a diferença entre backup completo, incremental e archivelogs;
- entender o papel do modo ARCHIVELOG;
- compreender a arquitetura e o funcionamento do RMAN;
- reconhecer a função do control file e do recovery catalog;
- compreender políticas de retenção e gerenciamento do ciclo de vida dos backups;
- entender cenários de recuperação de instância, datafiles, tablespaces e blocos corrompidos;
- relacionar disponibilidade, risco operacional e continuidade de negócio.

---

## O que este módulo precisa entregar

Este módulo não deverá ser tratado apenas como uma coleção de comandos de backup. Ele precisa estabelecer uma visão administrativa clara sobre proteção de dados.

Ao final, deveríamos ter conseguido:

1. entender por que backup não é sinônimo de recuperação;
2. compreender que diferentes tipos de falha exigem diferentes estratégias;
3. distinguir claramente os principais tipos de backup;
4. entender por que logs e archivelogs são decisivos em recuperação;
5. reconhecer o RMAN como ferramenta central de administração de backup físico Oracle;
6. compreender o papel de retenção, catálogo e metadados na governança de backup;
7. preparar a base conceitual para a prática de restore e recovery.

---

# 1. Fundamentos de backup e recuperação

Backup e recuperação formam uma disciplina central na administração de banco de dados. Deveríamos tratá-los como parte da continuidade operacional do ambiente.

## 1.1. O que é backup

Backup é a cópia organizada e controlada dos dados e metadados necessários para restaurar o ambiente ou parte dele em caso de falha.

Em termos administrativos, backup existe para permitir:

- restauração após perda de arquivos;
- recuperação após erro operacional;
- proteção contra corrupção;
- migração e clonagem de ambientes;
- apoio à continuidade de negócio;
- preservação histórica em determinados cenários.

## 1.2. O que é recuperação

Recuperação é o processo de restaurar o banco ou seus componentes para um estado consistente e utilizável após um problema.

Em outras palavras:

- **backup** é a preparação;
- **recuperação** é a resposta diante da falha.

## 1.3. Por que esse tema é crítico

Em ambientes reais, falhas podem ocorrer por diversos motivos:

- erro humano;
- perda de disco;
- corrupção de bloco;
- falha de sistema operacional;
- falha de instância;
- falha lógica de aplicação;
- exclusão indevida;
- problemas de armazenamento;
- incidentes de segurança.

A administração de backup e recuperação existe justamente para reduzir impacto, tempo de parada e perda de dados.

## 1.4. Conceitos relacionados

Ao tratar desse tema, deveríamos relacioná-lo a outros conceitos administrativos:

- disponibilidade;
- durabilidade;
- integridade;
- janela de backup;
- janela de recuperação;
- retenção;
- RTO;
- RPO;
- continuidade de negócio.

### RTO
**Recovery Time Objective** representa o tempo máximo aceitável para restaurar o serviço.

### RPO
**Recovery Point Objective** representa a quantidade máxima aceitável de perda de dados em termos de tempo.

Esses conceitos ajudam a conectar administração técnica com necessidade de negócio.

---

# 2. Tipos de falha que motivam estratégias de recuperação

Nem toda falha é igual. Por isso, não existe uma única estratégia universal de recuperação.

## 2.1. Falha de instância

Acontece quando a instância para de forma inesperada, por exemplo:

- queda do processo do banco;
- falha do servidor;
- encerramento abrupto;
- reinício inesperado do sistema.

Nesses casos, os arquivos do banco podem continuar existindo, mas a instância precisará passar por recuperação para garantir consistência.

## 2.2. Falha de mídia

Acontece quando há perda ou dano em arquivos físicos, como:

- datafiles;
- control files;
- redo logs;
- dispositivos de armazenamento.

Esse tipo de incidente costuma exigir restauração a partir de backup e aplicação de logs.

## 2.3. Corrupção lógica ou física

Pode ocorrer corrupção em:

- blocos;
- estruturas específicas;
- dados carregados incorretamente;
- objetos afetados por falha de aplicação.

## 2.4. Erro humano

Um dos cenários mais comuns envolve ações como:

- exclusão indevida de objetos;
- atualização errada em massa;
- sobrescrita de dados;
- comandos administrativos incorretos.

## 2.5. Falha parcial x falha total

Também deveríamos distinguir:

- falha parcial, quando apenas parte do banco é afetada;
- falha total, quando toda a instância ou ambiente fica indisponível.

Essa distinção é importante para entender por que alguns cenários exigem recuperação de instância, outros de datafile, outros de tablespace e outros apenas de blocos específicos.

---

# 3. Backup lógico e backup físico

Essa é uma das primeiras classificações que deveríamos consolidar.

## 3.1. Backup lógico

Backup lógico é realizado em nível de estrutura lógica do banco, normalmente extraindo objetos e dados em formato lógico.

Exemplos de uso:

- exportação de schema;
- exportação de tabelas;
- cópia lógica de objetos e dados;
- apoio a migração;
- clonagem seletiva.

### Características
- trabalha com objetos lógicos;
- é útil para movimentação entre ambientes;
- não substitui integralmente a estratégia de recuperação física do banco;
- é muito valioso em cenários de migração e restauração seletiva.

### 3.1.1. A comparação mental com outros bancos

Para quem já trabalhou com outros bancos, a forma mais prática de entender o backup lógico em Oracle é esta:

- PostgreSQL: `pg_dump`
- MySQL / MariaDB: `mysqldump`
- MongoDB: `mongodump`
- Oracle: `expdp`

Em Oracle, a ferramenta principal para esse tipo de operação é o **Oracle Data Pump**, com:

- `expdp` para exportação lógica;
- `impdp` para importação lógica.

Essa comparação é útil porque aproxima o raciocínio inicial:

- exportar schema;
- exportar tabela;
- mover objetos e dados entre ambientes;
- reconstruir parte do banco sem restaurar toda a infraestrutura física.

### 3.1.2. O que o Data Pump exporta

O Data Pump trabalha com camada lógica do banco, incluindo:

- metadados;
- tabelas;
- índices;
- constraints;
- dados;
- objetos de schema, conforme o escopo do comando.

Em termos práticos, isso significa que ele não exporta o banco como conjunto de datafiles prontos para restore físico. Ele exporta a representação lógica dos objetos Oracle.

### 3.1.3. O que o Data Pump não substitui

Mesmo sendo extremamente útil, o Data Pump não substitui:

- backup físico com RMAN;
- estratégia de archivelogs;
- restore de datafiles;
- recuperação estrutural do ambiente após perda de mídia.

Regra prática:

- para dev, laboratório, migração seletiva e cópia de schema, comece pensando em `expdp` e `impdp`;
- para proteção operacional do banco, continuidade e disaster recovery, pense em `RMAN`.

## 3.2. Backup físico

Backup físico é a cópia dos arquivos físicos do banco.

Exemplos de elementos envolvidos:

- datafiles;
- control files;
- archived redo logs;
- SPFILE;
- backupsets e image copies gerados pelo RMAN.

### Características
- é o núcleo da proteção operacional do banco Oracle;
- é o tipo de backup mais diretamente associado a restore e recovery do ambiente;
- trabalha em nível de infraestrutura e arquivos reais do banco.

## 3.3. Diferença prática

De forma resumida:

- **backup lógico** ajuda a exportar e reconstruir objetos e dados;
- **backup físico** ajuda a restaurar o próprio banco como estrutura operacional.

Deveríamos evitar tratar um como substituto completo do outro. Eles se complementam, mas atendem necessidades diferentes.

### 3.3.1. Analogia útil

Uma analogia simples ajuda a fixar:

- `expdp` / `impdp`: exportam e reconstroem objetos;
- `RMAN`: restaura a infraestrutura física do banco.

Em linguagem direta:

- o Data Pump é o caminho mais próximo de um "dump lógico";
- o RMAN é o caminho central para restore e recovery físico em Oracle.

---

# 4. Backup frio e backup quente

Essa classificação é clássica e ajuda a entender estratégias operacionais.

## 4.1. Backup frio

Backup frio é realizado quando o banco está desligado ou sem atividade de escrita relevante.

### Características
- o banco não está aberto para operação normal;
- a consistência tende a ser mais simples de garantir;
- normalmente implica indisponibilidade durante a janela de backup.

### Vantagens
- simplicidade conceitual;
- menor complexidade operacional;
- consistência mais direta em determinados cenários.

### Limitações
- exige parada;
- pouco adequado para ambientes que precisam de alta disponibilidade.

## 4.2. Backup quente

Backup quente é realizado com o banco em operação.

### Características
- o ambiente continua ativo;
- permite continuidade do serviço;
- depende fortemente de controle transacional e, em muitos cenários, do uso adequado de archivelogs e ferramentas de backup.

### Vantagens
- menor impacto de indisponibilidade;
- mais adequado para ambientes corporativos contínuos.

### Limitações
- maior complexidade;
- requer planejamento e controle mais rigorosos.

## 4.3. Perspectiva moderna

Em administração Oracle, quando usamos RMAN e ambiente adequadamente configurado, a ideia de backup quente se torna parte natural da operação corporativa. Ainda assim, a distinção conceitual continua importante.

---

# 5. Backup completo, incremental e archivelogs

Essa classificação é essencial para entender estratégia e retenção.

## 5.1. Backup completo

Backup completo captura toda a base ou todo o conjunto de arquivos definidos na política de backup.

### Características
- serve como base principal de restauração;
- tende a exigir mais tempo e espaço;
- costuma ser o ponto de referência para vários planos de retenção.

## 5.2. Backup incremental

Backup incremental copia apenas os blocos alterados desde um ponto de referência anterior.

### Características
- reduz volume de dados copiados;
- pode tornar a rotina diária mais eficiente;
- depende de estratégia coerente para recuperação posterior.

### Benefícios
- economia de tempo;
- redução de espaço;
- melhor aderência a janelas de backup restritas.

## 5.3. Archivelogs

Archivelogs são cópias persistidas dos redo logs preenchidos, preservando o histórico necessário para recuperação.

### Importância
Sem archivelogs, a capacidade de recuperação fica muito mais limitada.

### O que os archivelogs permitem
- recuperação até ponto consistente mais próximo;
- aplicação de alterações ocorridas após o último backup físico;
- recuperação mais precisa em cenários de falha de mídia.

## 5.4. Estratégia combinada

Na prática, a estratégia costuma combinar:

- backup completo;
- backup incremental;
- backup de archivelogs;
- retenção adequada;
- testes periódicos de recuperação.

---

# 6. Modo ARCHIVELOG e NOARCHIVELOG

Esse é um ponto conceitual que não pode faltar.

## 6.1. NOARCHIVELOG

No modo NOARCHIVELOG, os redo logs reutilizados não são preservados como archivelogs.

### Consequência
A recuperação fica limitada ao ponto do último backup disponível, sem capacidade de reaplicar todas as alterações posteriores.

## 6.2. ARCHIVELOG

No modo ARCHIVELOG, os redo logs preenchidos são arquivados antes de serem reutilizados.

### Consequência
Ganha-se capacidade de recuperação muito mais robusta, pois os logs podem ser reaplicados após a restauração de arquivos de backup.

## 6.3. Importância administrativa

Em ambientes corporativos relevantes, o modo ARCHIVELOG é geralmente indispensável para objetivos de continuidade mais exigentes.

---

# 7. Arquitetura e funcionamento do RMAN

O RMAN, Recovery Manager, é a principal ferramenta Oracle para backup físico e recuperação.

## 7.1. O que é o RMAN

RMAN é o utilitário nativo do Oracle para:

- backup físico;
- restore;
- recovery;
- gerenciamento de metadados de backup;
- validação de backups;
- controle de retenção;
- automação de tarefas de proteção.

## 7.2. Por que o RMAN é central

Ele é central porque conhece a estrutura do banco Oracle e trabalha de forma integrada com:

- datafiles;
- control files;
- archived redo logs;
- SPFILE;
- blocos utilizados;
- catálogo de backup;
- políticas de retenção.

## 7.3. Componentes lógicos envolvidos

Ao estudar RMAN, deveríamos compreender pelo menos estes elementos:

- **target database**: banco que será protegido;
- **control file**: armazena metadados de backup quando não há recovery catalog externo;
- **recovery catalog**: base opcional separada para armazenar metadados RMAN;
- **backup pieces**: arquivos gerados em formato de backupset;
- **image copies**: cópias físicas de arquivos;
- **channels**: caminhos lógicos pelos quais RMAN lê e grava dados.

## 7.4. Vantagens do RMAN

- integração nativa com o Oracle;
- noção de blocos usados;
- suporte a backups incrementais;
- validação de blocos e backups;
- restore e recovery coordenados;
- automação e padronização operacional.

---

# 8. Control file, recovery catalog e controle de metadados

Esse ponto merece destaque porque backup não depende apenas do arquivo copiado. Depende também do conhecimento sobre esse backup.

## 8.1. Control file

O control file é um arquivo crítico do banco que armazena metadados essenciais, inclusive informações sobre estrutura e, em muitos cenários, metadados RMAN.

### Por que é importante
Sem control file íntegro, a administração e recuperação do ambiente ficam severamente comprometidas.

## 8.2. Recovery catalog

O recovery catalog é uma base separada, opcional, usada para armazenar metadados de backup e recuperação de forma centralizada.

### Vantagens do recovery catalog
- histórico mais amplo;
- separação dos metadados em relação ao target database;
- apoio a ambientes mais complexos;
- melhor governança em múltiplos bancos.

## 8.3. Quando usar

Em laboratório e ambientes simples, muitas vezes o control file já basta. Em contextos corporativos mais amplos, o recovery catalog pode fazer bastante sentido.

---

# 9. Políticas de retenção e ciclo de vida dos backups

Uma estratégia de backup sem retenção bem definida tende a se tornar cara, confusa e arriscada.

## 9.1. O que é retenção

Retenção é a política que define por quanto tempo backups e logs deverão ser mantidos antes de se tornarem obsoletos ou descartáveis.

## 9.2. Por que isso é importante

Sem política de retenção, podemos ter problemas como:

- consumo descontrolado de espaço;
- dificuldade de localizar o backup correto;
- descarte prematuro de arquivos essenciais;
- excesso de cópias sem governança.

## 9.3. Critérios possíveis de retenção

A retenção pode ser pensada com base em:

- número de cópias;
- janela de recuperação;
- período regulatório;
- criticidade do sistema;
- custo de armazenamento;
- RPO e RTO desejados.

## 9.4. Governança do ciclo de vida

Deveríamos tratar backup como ciclo de vida:

1. gerar;
2. validar;
3. registrar;
4. reter;
5. testar recuperação;
6. tornar obsoleto;
7. remover com segurança.

---

# 10. Restore e recovery

Esses dois termos são próximos, mas não são idênticos.

## 10.1. Restore

Restore é o processo de restaurar arquivos de backup para o ambiente.

Exemplos:
- restaurar um datafile perdido;
- restaurar um control file;
- restaurar uma cópia do banco.

## 10.2. Recovery

Recovery é o processo de aplicar logs e outras informações necessárias para devolver consistência ao banco ou ao componente restaurado.

## 10.3. Diferença prática

- **restore** recoloca o arquivo;
- **recovery** reaplica o que falta para torná-lo consistente.

Essa distinção é central para não reduzir recuperação a mera cópia de arquivos.

---

# 11. Recuperação de instância

## 11.1. O que é

A recuperação de instância acontece quando a instância falha, mas os arquivos do banco ainda estão disponíveis.

## 11.2. Como funciona conceitualmente

O Oracle usa informações de redo e mecanismos internos para reaplicar e desfazer operações conforme necessário, levando o banco de volta a um estado consistente.

## 11.3. Importância

Esse tipo de recuperação mostra que o Oracle não depende sempre de restauração manual de arquivos para se recuperar. Em muitos casos, o próprio banco executa processos internos de recuperação ao reiniciar.

---

# 12. Recuperação de datafiles

## 12.1. O que é

Esse cenário ocorre quando um ou mais datafiles são perdidos, danificados ou inacessíveis.

## 12.2. Estratégia geral

Em linhas gerais, deveríamos pensar em:

- restaurar o datafile a partir de backup;
- aplicar archivelogs e redo necessários;
- devolver consistência ao componente afetado.

## 12.3. Contexto administrativo

Esse é um dos cenários clássicos de falha de mídia. Com boa estratégia de backup físico e archivelogs, a recuperação tende a ser viável de maneira controlada.

---

# 13. Recuperação de tablespaces

## 13.1. O que é

A recuperação de tablespace é uma abordagem focada em uma unidade lógica do banco, em vez de todo o ambiente.

## 13.2. Quando faz sentido

Faz sentido quando o problema está restrito a objetos ou arquivos associados a uma tablespace específica.

## 13.3. Benefícios

- recuperação mais direcionada;
- menor impacto sobre outras partes do banco;
- melhor aderência a falhas parciais.

---

# 14. Recuperação de blocos corrompidos

## 14.1. O que é

Esse cenário ocorre quando apenas alguns blocos apresentam corrupção, sem necessidade de restaurar arquivos inteiros.

## 14.2. Importância

Esse tipo de abordagem é importante porque evita operações mais pesadas quando o problema é localizado.

## 14.3. Valor administrativo

A possibilidade de tratar corrupção localizada reforça a ideia de recuperação granular e de manutenção mais eficiente do ambiente.

---

# 15. SPFILE, control file e arquivos críticos associados

Ao pensar em backup e recuperação, não deveríamos restringir a atenção apenas aos datafiles.

Também são críticos:

- **SPFILE** ou PFILE, que guardam parâmetros do ambiente;
- **control files**, essenciais para metadados e estrutura do banco;
- **archived redo logs**, decisivos para recuperação;
- em certos contextos, arquivos de senha e outros componentes administrativos.

Isso reforça que o banco é um conjunto articulado de arquivos e metadados, não apenas um repositório de tabelas.

---

# 16. Estratégias e boas práticas de backup

Do ponto de vista administrativo, algumas boas práticas deveriam sempre ser enfatizadas.

## 16.1. Não basta gerar backup; deveríamos validar

Um backup que nunca foi validado ou testado pode falhar no momento mais crítico.

## 16.2. Backup sem teste de recuperação é risco oculto

A confiança real em backup vem da capacidade de restaurar e recuperar com sucesso.

## 16.3. Política de retenção precisa ser explícita

Sem retenção clara, o ambiente fica desorganizado.

## 16.4. Logs e monitoramento são essenciais

Toda rotina de backup deveria deixar evidências verificáveis de execução.

## 16.5. Documentação operacional importa

Runbooks, horários, destinos, retenção e responsáveis devem estar claramente definidos.

## 16.6. Planejamento por criticidade

Nem todo banco exige a mesma janela, a mesma frequência ou a mesma profundidade de retenção. A estratégia deve considerar o valor do sistema para o negócio.

---

# 17. Relação entre backup, recuperação e continuidade de negócio

Este módulo fica mais forte quando associamos a técnica ao contexto maior de continuidade.

Backup e recuperação sustentam:

- disponibilidade do serviço;
- redução de perdas;
- conformidade;
- governança;
- recuperação de incidentes;
- resposta a falhas operacionais;
- retomada do ambiente após interrupções.

Em outras palavras, backup não é apenas uma rotina noturna. É parte da proteção do negócio.

---

# 18. Encaminhamento para a prática

Na parte prática deste módulo, deveríamos transformar esses conceitos em operações concretas, incluindo:

- configuração básica de ambiente para backup;
- observação do modo ARCHIVELOG;
- uso do RMAN;
- execução de backup completo;
- execução de backup incremental;
- backup de archivelogs;
- validação de backups;
- restore e recovery em cenários controlados;
- simulações de recuperação de instância, datafile e tablespace.

---

# 19. Resumo executivo do módulo

## O que este módulo deverá consolidar

- backup como preparação e recuperação como resposta;
- diferença entre backup lógico e físico;
- distinção entre backup frio e quente;
- importância de backup completo, incremental e archivelogs;
- papel central do RMAN;
- relevância do control file e do recovery catalog;
- necessidade de retenção e governança;
- compreensão de cenários de recuperação de instância, datafiles, tablespaces e blocos.

## O que não deveríamos fazer

- tratar backup como simples cópia de arquivo sem contexto;
- confundir restore com recovery;
- ignorar logs e archivelogs;
- confiar em backup nunca testado;
- reduzir o tema a comandos sem estratégia.

## Resultado esperado

Ao final da parte teórica, deveríamos ter um mapa claro da disciplina de backup e recuperação em Oracle, com base suficiente para construir uma prática consistente usando RMAN, restore e recovery em ambiente controlado.

---

# 20. Exemplos de referência RMAN

Este bloco resume comandos recorrentes que aparecem na operação de backup e recuperação.

## 20.1. Backup com formato de arquivo definido

```rman
BACKUP DATABASE
FORMAT '/opt/oracle/backup/db_%U.bkp';
```

Esse formato ajuda a padronizar destino e naming dos arquivos de backup.

## 20.2. Restore e recover completos

```rman
RESTORE DATABASE;
RECOVER DATABASE;
```

Essa sequência representa o fluxo base de restauração e recuperação quando o cenário exige recuperação completa do banco.

## 20.3. Exemplo de Point-in-Time Recovery

```rman
RUN {
  SET UNTIL TIME "TO_DATE('2026-04-14 10:00:00','YYYY-MM-DD HH24:MI:SS')";
  RESTORE DATABASE;
  RECOVER DATABASE;
}
```

Após PITR, a abertura do banco pode exigir `RESETLOGS`, conforme o estado do ambiente e a estratégia adotada.
