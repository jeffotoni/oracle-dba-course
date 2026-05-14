# Módulo 4 - Monitoramento, Tuning e Otimização de Desempenho

## Visão geral

Este módulo deverá consolidar um dos eixos mais sensíveis da administração de bancos de dados: a capacidade de observar o ambiente, identificar gargalos, interpretar sintomas de lentidão e aplicar ações de ajuste com base em evidências.

Em ambientes corporativos, desempenho não deve ser tratado apenas como velocidade percebida pelo usuário. Deveríamos entendê-lo como resultado da interação entre arquitetura, carga de trabalho, memória, CPU, I/O, concorrência, estatísticas, consultas SQL, parâmetros do banco e desenho dos objetos.

A administração de desempenho exige disciplina analítica. Antes de alterar qualquer configuração, deveríamos saber o que está acontecendo, por que está acontecendo e qual componente está impondo o principal custo operacional. Por isso, monitoramento e tuning devem caminhar juntos.

Este módulo organiza essa visão em uma estrutura teórica que prepara o terreno para a prática de diagnóstico, análise e otimização.

---

## Carga horária sugerida

5 horas

**Distribuição sugerida:**  
2 horas de teoria + 3 horas de prática

---

## Objetivos do módulo

Ao final deste módulo, deveríamos ter consolidado os seguintes entendimentos:

- compreender a importância do monitoramento contínuo do ambiente Oracle;
- reconhecer sintomas e sinais típicos de degradação de desempenho;
- entender o papel das visões dinâmicas de desempenho;
- compreender a relação entre sessões, processos, waits, locks e consumo de recursos;
- distinguir monitoramento preventivo de monitoramento corretivo;
- compreender fundamentos de tuning de instância, memória, I/O e SQL;
- entender o papel do otimizador baseado em custo;
- compreender a relevância das estatísticas para geração de planos de execução;
- reconhecer a função de ferramentas como Explain Plan, AWR, ADDM e SQL Tuning Advisor;
- relacionar desempenho, governança operacional e continuidade do serviço.

---

## O que este módulo precisa entregar

Este módulo não deverá ser tratado como um catálogo de parâmetros ou uma coleção de “dicas rápidas” de performance. Ele precisa estabelecer uma visão analítica e estruturada do desempenho do banco.

Ao final, deveríamos ter conseguido:

1. entender que lentidão é um sintoma, não um diagnóstico;
2. reconhecer que o banco precisa ser observado por métricas, sessões, eventos e planos;
3. distinguir causa raiz de efeito percebido;
4. compreender o papel do otimizador e das estatísticas;
5. reconhecer quando o problema está em SQL, quando está em concorrência, quando está em configuração e quando está em infraestrutura;
6. construir a base conceitual para uma prática de tuning orientada por evidências.

---

# 1. Monitoramento do ambiente Oracle

Monitorar um banco de dados significa observar continuamente seu comportamento operacional para identificar anomalias, tendências, gargalos e riscos de indisponibilidade ou lentidão.

Em Oracle, monitoramento não se resume a “olhar se o banco está no ar”. Deveríamos acompanhar:

- estado da instância;
- sessões e usuários conectados;
- consumo de CPU;
- uso de memória;
- leitura e escrita em disco;
- waits e eventos de espera;
- locks e deadlocks;
- crescimento de objetos;
- geração de redo;
- utilização de tablespaces;
- comportamento das consultas SQL.

## 1.1. Monitoramento preventivo

Monitoramento preventivo é aquele voltado a antecipar problemas.

Ele busca identificar sinais como:

- crescimento anormal de objetos;
- aumento do tempo médio de resposta;
- aumento persistente de waits;
- saturação de sessões;
- consumo exagerado de recursos;
- degradação progressiva de determinadas cargas.

A ideia do monitoramento preventivo é reduzir a necessidade de atuação apenas reativa.

## 1.2. Monitoramento corretivo

Monitoramento corretivo é aquele acionado quando já existe um incidente ou sintoma claro de lentidão, travamento ou indisponibilidade.

Exemplos típicos:

- usuários reclamando de lentidão;
- rotina batch demorando mais do que o normal;
- sessões travadas;
- crescimento anormal de fila de espera;
- consultas consumindo recursos em excesso.

## 1.3. Visão administrativa

Deveríamos sempre reforçar que monitoramento é parte da administração contínua do banco. Um ambiente só começa a ser bem gerenciado quando consegue produzir evidências confiáveis sobre seu próprio comportamento.

---

# 2. Fontes de observação no Oracle

O Oracle oferece múltiplas formas de observação do ambiente. Para administração e tuning, as mais importantes incluem:

- **alert log**;
- **visões dinâmicas de desempenho (V$ Views)**;
- **AWR**;
- **ADDM**;
- **planos de execução**;
- **estatísticas do dicionário e do otimizador**;
- **ferramentas gráficas ou utilitários administrativos**.

## 2.1. Alert log

O alert log registra eventos importantes do banco, como:

- inicialização e desligamento;
- erros críticos;
- problemas de I/O;
- mensagens relacionadas a recuperação;
- eventos estruturais relevantes.

Ele não é uma ferramenta completa de tuning, mas é essencial no diagnóstico operacional.

## 2.2. V$ Views

As visões dinâmicas de desempenho são centrais para administração Oracle. Elas permitem observar sessões, memória, redo, waits, locks, arquivos, estatísticas e diversos componentes internos do banco.

Exemplos de famílias relevantes:

- `V$INSTANCE`
- `V$DATABASE`
- `V$SESSION`
- `V$PROCESS`
- `V$SYSSTAT`
- `V$SYSTEM_EVENT`
- `V$SESSION_EVENT`
- `V$SQL`
- `V$SQLAREA`
- `V$LOCK`
- `V$DATAFILE`
- `V$UNDOSTAT`
- `V$ACTIVE_SESSION_HISTORY` (quando disponível)

## 2.3. Instrumentação e leitura crítica

Ter acesso às visões não resolve o problema por si só. Deveríamos saber fazer perguntas corretas, como:

- o banco está lento para todos ou apenas para um grupo de sessões?
- existe espera dominante?
- há bloqueios?
- o plano de execução mudou?
- as estatísticas estão atualizadas?
- o consumo está concentrado em uma consulta ou distribuído?

---

# 3. Sessões, processos e consumo de recursos

Para analisar desempenho, deveríamos entender a relação entre sessão, processo e carga.

## 3.1. Sessão

Uma sessão representa a interação lógica de um usuário ou aplicação com o banco.

A análise de sessões ajuda a responder:

- quem está conectado;
- o que está executando;
- há sessões inativas demais;
- há sessões presas;
- há sessões em espera prolongada;
- quais sessões estão consumindo mais recursos.

## 3.2. Processo

Os processos no Oracle dão suporte à execução do ambiente e das sessões. Em contexto de monitoramento, interessa compreender:

- quais processos estão ativos;
- como a instância está se comportando;
- como sessões e processos se relacionam;
- onde há pressão operacional.

## 3.3. Consumo de recursos

O monitoramento de recursos costuma observar:

- CPU;
- memória;
- I/O;
- tempo de execução;
- geração de redo;
- concorrência;
- atividade por sessão;
- carga por SQL.

Esse ponto é importante porque muitos problemas percebidos como “problema do banco” podem estar ligados a poucas sessões, poucas consultas ou recursos específicos.

---

# 4. Waits e eventos de espera

Um dos conceitos mais importantes em tuning Oracle é a ideia de **espera**.

## 4.1. O que são waits

Waits representam o tempo em que uma sessão ou processo está aguardando algo para continuar sua execução.

Essa espera pode estar relacionada a:

- leitura em disco;
- disputa por lock;
- contenção em latch;
- eventos de log;
- rede;
- commit;
- recursos internos.

## 4.2. Por que waits são importantes

Em vez de olhar apenas para “está lento”, deveríamos observar **onde o tempo está sendo gasto**. Muitas vezes, a principal pista está justamente no evento de espera dominante.

## 4.3. Interpretação prática

Se grande parte do tempo está sendo consumida em espera, o problema pode não ser CPU pura, mas:

- I/O lento;
- contenção;
- bloqueio;
- concorrência;
- problema de desenho de consulta;
- pressão sobre redo;
- infraestrutura insuficiente.

## 4.4. Espera dominante e causa raiz

Uma prática importante de administração de desempenho é identificar a espera dominante, mas sem confundir isso com causa final. O evento aponta um sintoma de baixo nível. A análise precisa ir além para descobrir por que aquilo está acontecendo.

---

# 5. Locks e deadlocks

Concorrência faz parte da vida de qualquer banco transacional. Por isso, monitorar locks e deadlocks é essencial.

## 5.1. Locks

Locks são mecanismos de controle usados para proteger consistência durante operações concorrentes.

Em princípio, locks não são sempre um problema. Eles fazem parte do funcionamento normal do banco.

## 5.2. Quando locks viram problema

Eles passam a ser um problema quando:

- ficam retidos por tempo excessivo;
- bloqueiam transações críticas;
- provocam fila de espera grande;
- se associam a desenho ruim de aplicação;
- surgem em massa em horário de pico.

## 5.3. Deadlocks

Deadlock é uma situação em que duas ou mais transações entram em espera circular, impedindo a continuidade normal.

## 5.4. Perspectiva administrativa

Deveríamos tratar locks e deadlocks não apenas como fenômeno do banco, mas também como sinal de:

- desenho de transação inadequado;
- tempo de retenção excessivo;
- baixa coordenação entre processos;
- concorrência mal distribuída;
- SQL ou aplicação mal desenhados.

---

# 6. Fundamentos de tuning

Tuning é o processo de ajustar o ambiente para obter melhor desempenho com base em observação e evidência.

## 6.1. O que tuning não deveria ser

Tuning não deveria ser:

- alteração aleatória de parâmetros;
- troca de índices por tentativa e erro;
- ajuste baseado apenas em “receita pronta”;
- repetição mecânica de checklists sem diagnóstico.

## 6.2. O que tuning deveria ser

Tuning deveria ser:

- análise;
- formulação de hipótese;
- intervenção controlada;
- validação do resultado;
- documentação da mudança.

## 6.3. Dimensões do tuning

No Oracle, tuning costuma envolver:

- tuning de instância;
- tuning de memória;
- tuning de I/O;
- tuning de SQL;
- tuning de concorrência;
- tuning de modelo físico e índices;
- tuning de estatísticas e planos.

---

# 7. Tuning de instância

Tuning de instância observa o comportamento global do banco.

## 7.1. O que envolve

Pode envolver análise de:

- sessões ativas;
- pressão de memória;
- carga geral;
- waits predominantes;
- geração de redo;
- configuração de parâmetros;
- número de processos e sessões;
- comportamento de background processes.

## 7.2. Visão prática

Esse tipo de tuning busca responder se o ambiente está configurado de forma coerente com a carga que está recebendo.

## 7.3. Cuidado metodológico

Deveríamos evitar tratar parâmetros como solução mágica. Muitas vezes, o problema não está na instância em si, mas em SQL ruim, desenho físico inadequado ou concorrência mal controlada.

---

# 8. Tuning de memória

Memória é um dos pontos mais sensíveis em Oracle.

## 8.1. Componentes importantes

De forma geral, deveríamos relacionar memória a:

- SGA;
- PGA;
- buffer cache;
- shared pool;
- áreas de execução de sessão e processo.

## 8.2. Sintomas de problema de memória

Podem incluir:

- excesso de leitura física;
- queda de eficiência do cache;
- parsing excessivo;
- pressão sobre shared pool;
- crescimento de spills para disco;
- degradação em operações de ordenação e hash.

## 8.3. Ajuste de memória

Ajustes de memória precisam ser avaliados com cuidado, porque alterar memória sem entender a carga pode deslocar o problema para outro componente.

---

# 9. Tuning de I/O

I/O continua sendo um ponto crítico de desempenho em muitos ambientes.

## 9.1. O que observar

Deveríamos considerar:

- leituras físicas;
- escritas físicas;
- latência;
- distribuição de carga sobre armazenamento;
- checkpoints;
- geração de redo;
- impacto de full scans;
- pressão de archivelogs e backup.

## 9.2. Relação com SQL

Problemas de I/O muitas vezes não nascem apenas do disco em si. Eles podem ser consequência de:

- plano de execução ruim;
- ausência de índice adequado;
- estatísticas desatualizadas;
- consulta que lê mais dados do que deveria;
- desenho físico inadequado.

## 9.3. Visão administrativa

Tuning de I/O exige olhar tanto o banco quanto a infraestrutura que o suporta.

---

# 10. Tuning de SQL

Tuning de SQL costuma gerar os maiores ganhos práticos em muitos ambientes.

## 10.1. Por que SQL é tão importante

Mesmo um banco bem configurado pode ficar lento se as consultas forem ruins. Em muitos casos, poucas instruções SQL concentram grande parte do consumo de recursos.

## 10.2. O que observar em SQL

Deveríamos avaliar:

- volume de leitura;
- seletividade;
- filtros;
- joins;
- agregações;
- ordenações;
- uso de índices;
- cardinalidade estimada;
- custo do plano;
- estabilidade do plano.

## 10.3. Perspectiva de tuning

Tuning de SQL não significa apenas “colocar índice”. Às vezes o problema está em:

- lógica da consulta;
- função aplicada em coluna indexada;
- junção mal distribuída;
- estatísticas ruins;
- falta de filtro;
- projeção excessiva;
- modelo inadequado.

---

# 11. O otimizador baseado em custo (CBO)

O CBO é um dos elementos centrais do desempenho em Oracle.

## 11.1. O que é

O **Cost-Based Optimizer** é o mecanismo que escolhe o plano de execução com base em estimativas de custo.

## 11.2. O que o CBO considera

Em linhas gerais, o CBO utiliza:

- estatísticas de tabelas;
- estatísticas de índices;
- cardinalidade estimada;
- seletividade;
- distribuição de dados;
- custos de operações;
- alternativas de acesso e junção.

## 11.3. Importância administrativa

Sem entender o CBO, fica muito difícil compreender por que o banco escolheu determinado plano e por que uma consulta executou bem ontem e mal hoje.

---

# 12. Estatísticas

Estatísticas são fundamentais para que o otimizador estime corretamente o custo de execução.

## 12.1. O que são

São metadados sobre distribuição e volume dos dados armazenados.

## 12.2. Por que importam

Sem estatísticas adequadas, o CBO pode:

- estimar cardinalidade errada;
- escolher junção inadequada;
- ignorar índice útil;
- fazer acesso excessivo a dados;
- selecionar plano instável.

## 12.3. Problemas típicos

Estatísticas podem causar problema quando:

- estão desatualizadas;
- foram coletadas em momento inadequado;
- não representam bem a distribuição real;
- não existem para objetos relevantes.

## 12.4. Relação com governança

Coleta e manutenção de estatísticas devem ser tratadas como parte da rotina administrativa do banco.

---

# 13. Planos de execução

O plano de execução é um dos instrumentos mais importantes para entender o comportamento de uma consulta.

## 13.1. O que é

É a representação das operações que o banco pretende executar para responder uma instrução SQL.

## 13.2. O que ele mostra

De forma geral, o plano pode mostrar:

- acesso por índice;
- full table scan;
- métodos de join;
- ordenação;
- filtros;
- operações intermediárias;
- estimativas de linhas;
- custo relativo.

## 13.3. Por que é importante

Sem olhar o plano, muitas análises de desempenho ficam superficiais. O plano ajuda a conectar:

- SQL escrito;
- escolha do otimizador;
- uso de objetos físicos;
- custo esperado;
- possíveis gargalos.

## 13.4. Limitação importante

Plano estimado não é a mesma coisa que tempo real observado. Por isso, deveríamos combinar plano de execução com métricas reais e comportamento do banco.

---

# 14. Explain Plan

## 14.1. O que é

Explain Plan é um recurso usado para visualizar o plano estimado de execução de uma instrução SQL.

## 14.2. Utilidade

Ele ajuda a:

- entender a estratégia escolhida pelo otimizador;
- comparar alternativas;
- identificar full scans inesperados;
- observar métodos de join;
- apoiar revisões de SQL.

## 14.3. Limitação

Explain Plan mostra plano estimado. Em análise mais avançada, deveríamos também considerar execução real e estatísticas observadas.

---

# 15. AWR

## 15.1. O que é

AWR, **Automatic Workload Repository**, é um repositório de informações de desempenho do banco.

## 15.2. O que ele ajuda a observar

Ele consolida dados como:

- carga do sistema;
- eventos de espera;
- SQL mais custosos;
- consumo de recursos;
- atividade por snapshots;
- tendências de comportamento.

## 15.3. Relevância administrativa

AWR é valioso porque ajuda a olhar desempenho de forma histórica e comparativa, não apenas instantânea.

## 15.4. Limitação prática

Em laboratório simples, nem sempre conseguiremos explorar toda a profundidade do AWR. Mesmo assim, é importante compreender sua função conceitual.

---

# 16. ADDM

## 16.1. O que é

ADDM, **Automatic Database Diagnostic Monitor**, é um mecanismo de diagnóstico que usa dados do AWR para identificar problemas e sugerir ações.

## 16.2. O que ele faz

Ele busca identificar:

- gargalos relevantes;
- consumo desproporcional;
- SQL problemáticos;
- waits dominantes;
- oportunidades de melhoria.

## 16.3. Visão crítica

ADDM ajuda bastante, mas não substitui o julgamento do administrador. Sugestão automática não deve ser aplicada sem análise contextual.

---

# 17. SQL Tuning Advisor

## 17.1. O que é

É uma ferramenta voltada a análise de instruções SQL para sugerir melhorias.

## 17.2. O que pode sugerir

Pode sugerir, por exemplo:

- criação de perfis SQL;
- coleta de estatísticas;
- reescrita da consulta;
- ajustes relacionados ao plano.

## 17.3. Visão administrativa

Deveríamos vê-lo como apoio à análise, e não como substituto do entendimento do problema.

---

# 18. Relação entre desempenho, desenho de dados e aplicação

Um erro comum é atribuir toda lentidão ao banco de dados. Em muitos cenários, o problema nasce da interação entre várias camadas.

Deveríamos sempre considerar:

- SQL mal escrito;
- modelo físico inadequado;
- índice ausente ou excessivo;
- coleta ruim de estatísticas;
- concorrência excessiva;
- transações longas;
- desenho inadequado da aplicação;
- infraestrutura subdimensionada.

Isso reforça que tuning não é apenas “mexer no banco”, mas compreender o ecossistema.

---

# 19. Estratégia analítica de tuning

Uma abordagem mais madura de tuning deveria seguir uma sequência lógica.

## 19.1. Observar o sintoma
Exemplo:
- lentidão;
- travamento;
- fila;
- consumo alto;
- tempo excessivo de execução.

## 19.2. Coletar evidências
Exemplo:
- sessões;
- waits;
- SQL;
- plano;
- estatísticas;
- locks;
- eventos.

## 19.3. Formular hipótese
Exemplo:
- problema de join;
- estatística desatualizada;
- índice inadequado;
- concorrência;
- pressão de I/O.

## 19.4. Intervir de forma controlada
Exemplo:
- revisar SQL;
- atualizar estatísticas;
- ajustar índice;
- alterar parâmetro com cautela;
- redistribuir carga.

## 19.5. Medir o efeito
Sem medir antes e depois, não há tuning de verdade.

---

# 20. Boas práticas de monitoramento e tuning

Deveríamos enfatizar algumas boas práticas:

- medir antes de alterar;
- registrar intervenções;
- evitar mudanças simultâneas em excesso;
- revisar SQL de maior impacto;
- manter estatísticas coerentes;
- monitorar crescimento e tendência;
- tratar locks longos como sinal de investigação;
- observar waits dominantes;
- usar ferramentas automáticas com senso crítico;
- diferenciar ajuste emergencial de melhoria estrutural.

---

# 21. Encaminhamento para a prática

Na parte prática deste módulo, deveríamos transformar esses conceitos em operações concretas, incluindo:

- leitura do alert log;
- consultas em `V$SESSION`, `V$LOCK`, `V$SQL`, `V$SYSSTAT` e `V$SYSTEM_EVENT`;
- observação de sessões e waits;
- simulação de locks;
- leitura de planos de execução;
- uso de `EXPLAIN PLAN`;
- análise de estatísticas;
- identificação de consultas custosas;
- comparação entre execução antes e depois de ajustes simples.

---

# 22. Resumo executivo do módulo

## O que este módulo deverá consolidar

- monitoramento como prática contínua de administração;
- lentidão como sintoma, não como diagnóstico;
- importância das visões de desempenho;
- relevância de sessões, waits, locks e consumo de recursos;
- fundamentos de tuning de instância, memória, I/O e SQL;
- papel central do CBO e das estatísticas;
- valor de planos de execução e ferramentas analíticas como AWR, ADDM e SQL Tuning Advisor.

## O que não deveríamos fazer

- ajustar parâmetros sem diagnóstico;
- tratar índice como solução universal;
- confundir sintoma com causa raiz;
- confiar apenas em impressão subjetiva de lentidão;
- aplicar sugestões automáticas sem análise.

## Resultado esperado

Ao final da parte teórica, deveríamos ter um mapa claro de monitoramento, diagnóstico e tuning no Oracle, com base suficiente para construir uma prática consistente e orientada por evidências.
