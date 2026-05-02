# Módulo 5 – Oracle 12c Multitenant e Ambiente de Nuvem

## Visão geral

Este módulo deverá consolidar a visão mais moderna da administração Oracle, conectando a arquitetura clássica de banco de dados corporativo à evolução para ambientes multitenant e à operação em nuvem.

Ao longo da história dos bancos Oracle, a administração evoluiu de uma lógica mais centrada em instância única e banco único para modelos mais flexíveis, compartilhados e preparados para escala, consolidação e serviços em nuvem. Dentro desse movimento, a arquitetura **Multitenant**, introduzida como marco no Oracle 12c, tornou-se uma das mudanças mais importantes na forma de organizar e administrar bancos Oracle.

Além disso, a estratégia Oracle passou a incorporar fortemente o conceito de **Database as a Service (DBaaS)** e, posteriormente, serviços gerenciados e autônomos em nuvem, o que exige uma visão administrativa que ultrapassa o ambiente on-premises tradicional.

Este módulo deverá organizar essa transição conceitual e preparar a base para compreender como o Oracle se posiciona em ambientes modernos de banco de dados.

---

## Carga horária sugerida

4 horas

**Distribuição sugerida:**  
2 horas de teoria + 2 horas de prática

---

## Objetivos do módulo

Ao final deste módulo, deveríamos ter consolidado os seguintes entendimentos:

- compreender a importância da arquitetura multitenant no Oracle 12c;
- distinguir CDB e PDB;
- compreender a lógica de consolidação de ambientes em pluggable databases;
- reconhecer operações administrativas básicas em PDBs;
- compreender o papel de clone, plug e unplug no ciclo de vida administrativo;
- entender a relação entre Oracle e computação em nuvem;
- reconhecer os conceitos de Oracle Cloud Infrastructure (OCI), DBaaS e Autonomous Database;
- compreender diferenças entre administração on-premises, administração em nuvem e modelos híbridos;
- relacionar multitenant, nuvem, eficiência operacional e governança.

---

## O que este módulo precisa entregar

Este módulo não deverá ser tratado apenas como uma apresentação institucional sobre cloud. Ele precisa entregar uma visão administrativa concreta da evolução do Oracle.

Ao final, deveríamos ter conseguido:

1. entender por que a arquitetura multitenant foi importante;
2. compreender o papel de CDB e PDB na consolidação de ambientes;
3. reconhecer as principais operações administrativas em PDBs;
4. entender como o Oracle se posiciona em infraestrutura de nuvem;
5. distinguir claramente o que permanece igual e o que muda quando saímos do ambiente local para DBaaS ou serviço gerenciado;
6. construir a base conceitual para a prática introdutória de multitenant e cloud.

---

# 1. Contexto da evolução do Oracle

A administração de banco de dados Oracle sempre esteve ligada a ambientes corporativos críticos, com foco em transações, segurança, disponibilidade e recuperação. Ao longo do tempo, porém, o crescimento da demanda por consolidação, elasticidade e redução de custo operacional levou a mudanças arquiteturais importantes.

## 1.1. Cenário anterior ao Multitenant

Antes da consolidação do modelo multitenant, era comum administrar bancos de forma mais isolada, com uma relação mais direta entre instância, estrutura do banco e aplicação atendida.

Esse modelo funcionava, mas gerava desafios como:

- maior custo de administração;
- maior quantidade de bancos isolados;
- redundância de configuração;
- dificuldade de consolidação;
- uso menos eficiente de recursos;
- manutenção mais complexa em ambientes com muitos bancos.

## 1.2. Pressão por consolidação

Com o crescimento do número de sistemas corporativos, tornou-se importante encontrar formas de:

- consolidar ambientes;
- reduzir sobrecarga operacional;
- manter isolamento lógico;
- compartilhar melhor recursos;
- simplificar administração de múltiplos bancos.

É nesse contexto que a arquitetura multitenant ganha relevância.

## 1.3. Marco do Oracle 12c

O Oracle Database 12c, lançado originalmente em 2013, destacou-se justamente por introduzir de forma mais estruturada a arquitetura **Multitenant**, baseada em:

- **CDB** – Container Database;
- **PDB** – Pluggable Database.

Essa mudança foi estratégica porque aproximou o Oracle de modelos mais adequados à consolidação e à nuvem.

---

# 2. Arquitetura Multitenant

## 2.1. O que é Multitenant

A arquitetura multitenant é um modelo no qual múltiplos bancos lógicos podem coexistir dentro de uma estrutura maior compartilhada.

No Oracle, isso significa que um **Container Database (CDB)** pode conter uma ou mais **Pluggable Databases (PDBs)**.

## 2.2. Objetivo da arquitetura

O objetivo da arquitetura multitenant é combinar:

- compartilhamento de infraestrutura;
- isolamento lógico;
- simplificação administrativa;
- maior eficiência operacional;
- facilidade de clonagem e movimentação.

## 2.3. Mudança de paradigma

Esse modelo altera a forma de pensar administração. Em vez de tratar cada banco como um universo totalmente isolado, passamos a pensar em:

- uma camada container;
- múltiplos bancos plugáveis;
- operações locais e globais;
- administração compartilhada e segmentada ao mesmo tempo.

---

# 3. CDB – Container Database

## 3.1. O que é

O **Container Database (CDB)** é a estrutura principal que abriga o ambiente multitenant.

## 3.2. Papel administrativo

O CDB centraliza elementos compartilhados de administração e serve como contêiner lógico da arquitetura.

Em termos conceituais, ele concentra:

- a camada estrutural do ambiente;
- componentes compartilhados;
- metadados e mecanismos que sustentam as PDBs;
- ponto central de administração global.

## 3.3. Visão administrativa

Ao administrar o CDB, deveríamos pensar em:

- estrutura global do ambiente;
- visão consolidada das PDBs;
- parâmetros e operações de nível container;
- governança do conjunto.

---

# 4. PDB – Pluggable Database

## 4.1. O que é

A **Pluggable Database (PDB)** é um banco lógico plugado dentro do CDB.

## 4.2. Papel administrativo

A PDB permite isolar aplicações, dados e objetos de forma lógica, mantendo um nível importante de separação entre ambientes.

## 4.3. Benefícios

O uso de PDBs ajuda a:

- consolidar vários bancos em uma estrutura comum;
- reduzir overhead administrativo;
- facilitar provisionamento;
- separar aplicações ou clientes;
- tornar cópia e movimentação mais simples;
- melhorar uso de recursos.

## 4.4. Visão prática

Na administração do dia a dia, deveríamos enxergar a PDB como o espaço lógico mais próximo da aplicação, enquanto o CDB representa a camada superior de controle e consolidação.

---

# 5. Relação entre CDB e PDB

Essa distinção é obrigatória porque, sem ela, a administração multitenant fica confusa.

## 5.1. CDB

O CDB representa a estrutura container, a camada superior do ambiente.

## 5.2. PDB

A PDB representa o banco lógico plugável, onde a aplicação ou conjunto de dados efetivamente vive.

## 5.3. Implicação administrativa

Deveríamos sempre saber em qual contexto estamos operando:

- nível CDB;
- nível PDB.

Essa distinção afeta:

- visões administrativas;
- criação de usuários;
- parametrização;
- gerenciamento de objetos;
- escopo de determinadas operações.

---

# 6. Vantagens da arquitetura Multitenant

A adoção de multitenant não aconteceu apenas por elegância arquitetural. Ela resolve problemas reais de administração.

## 6.1. Consolidação

Permite reunir múltiplos bancos em uma estrutura comum.

## 6.2. Padronização

Facilita administração padronizada de ambientes antes dispersos.

## 6.3. Eficiência de recursos

Ajuda a compartilhar melhor componentes estruturais e operacionais.

## 6.4. Agilidade operacional

Favorece criação, clone, abertura, fechamento e movimentação de PDBs.

## 6.5. Aproximação com nuvem

A arquitetura multitenant conversa muito bem com modelos de serviço e provisionamento sob demanda.

---

# 7. Operações administrativas básicas em PDBs

Um dos pontos mais importantes deste módulo é mostrar que a administração multitenant não é puramente conceitual. Ela envolve operações concretas.

## 7.1. Abertura e fechamento

PDBs podem ser abertas e fechadas conforme a necessidade operacional.

Isso é importante para:

- manutenção;
- disponibilidade controlada;
- preparação de ambiente;
- administração do ciclo de vida.

## 7.2. Criação

PDBs podem ser criadas como parte da expansão ou organização do ambiente.

## 7.3. Clone

O clone de PDB permite criar uma cópia lógica de uma base existente, recurso muito útil para:

- homologação;
- testes;
- provisionamento rápido;
- replicação controlada de ambiente.

## 7.4. Plug e unplug

Essas operações permitem mover PDBs entre ambientes ou reorganizar a estrutura administrativa de forma flexível.

## 7.5. Administração do ciclo de vida

No contexto multitenant, deveríamos pensar no ciclo de vida da PDB como:

1. criação;
2. abertura;
3. uso;
4. clone ou movimentação;
5. fechamento;
6. remoção, quando necessário.

---

# 8. Usuários e administração em ambiente multitenant

A arquitetura multitenant traz reflexos importantes para a administração de usuários.

## 8.1. Escopo administrativo

Em termos conceituais, deveríamos distinguir entre:

- administração no escopo do container;
- administração no escopo da PDB.

## 8.2. Implicação prática

Isso afeta:

- criação de usuários;
- privilégio;
- administração de objetos;
- leitura de determinadas visões;
- governança do ambiente.

## 8.3. Visão de segurança

A segurança em multitenant exige mais atenção ao escopo, porque o administrador precisa saber se está atuando no nível global da estrutura ou no nível específico de uma base plugável.

---

# 9. Parâmetros, administração e monitoramento em Multitenant

Multitenant não elimina os conceitos clássicos de administração Oracle. Ele os reorganiza em um contexto mais amplo.

## 9.1. O que permanece

Continuamos precisando de:

- usuários;
- privilégios;
- monitoramento;
- backup;
- recuperação;
- tuning;
- controle de sessões;
- observação de desempenho.

## 9.2. O que muda

A diferença está no escopo da administração e na forma de organizar ambientes múltiplos dentro de uma mesma estrutura container.

## 9.3. Implicação para monitoramento e tuning

Deveríamos interpretar desempenho também considerando:

- distribuição entre PDBs;
- impacto compartilhado no container;
- governança de múltiplos bancos lógicos;
- consolidação de recursos.

---

# 10. Oracle e computação em nuvem

O segundo eixo deste módulo é a relação entre Oracle e cloud.

## 10.1. O que significa levar banco para nuvem

Levar banco de dados para nuvem não significa apenas “mudar de lugar”. Significa alterar o modelo de provisão, operação e consumo de infraestrutura.

## 10.2. Principais mudanças conceituais

Em nuvem, a administração tende a se relacionar com:

- elasticidade;
- provisionamento sob demanda;
- automação;
- abstração de infraestrutura;
- cobrança por consumo;
- serviço gerenciado;
- integração com rede, segurança e observabilidade da plataforma.

## 10.3. Perspectiva administrativa

Deveríamos entender cloud como mudança operacional e não apenas tecnológica. Em nuvem, várias atividades permanecem, mas o grau de responsabilidade do administrador pode mudar conforme o tipo de serviço.

---

# 11. Oracle Cloud Infrastructure (OCI)

## 11.1. O que é

A **Oracle Cloud Infrastructure (OCI)** é a plataforma de nuvem da Oracle.

## 11.2. Papel da OCI no contexto de banco de dados

A OCI oferece serviços e infraestrutura para hospedar bancos Oracle em diferentes modelos, com diferentes níveis de abstração.

## 11.3. Visão administrativa

Ao falar de OCI, deveríamos pensar em:

- infraestrutura;
- rede;
- armazenamento;
- segurança;
- serviços gerenciados;
- provisionamento de banco;
- integração com workloads corporativos.

---

# 12. Database as a Service (DBaaS)

## 12.1. O que é

**DBaaS** é o modelo em que o banco é oferecido como serviço.

## 12.2. O que isso muda

Em vez de administrar tudo manualmente em nível de servidor, passamos a receber parte da infraestrutura e da operação já preparada.

## 12.3. Benefícios

- provisionamento mais rápido;
- redução de esforço operacional;
- padronização;
- melhor integração com automação;
- maior agilidade para criação e expansão de ambientes.

## 12.4. O que não desaparece

Mesmo em DBaaS, ainda deveríamos nos preocupar com:

- usuários;
- privilégios;
- segurança lógica;
- backup;
- monitoramento;
- tuning;
- governança dos dados;
- desenho das consultas e objetos.

---

# 13. Autonomous Database

## 13.1. O que é

O **Autonomous Database** é a proposta da Oracle de um banco com alto grau de automação operacional.

## 13.2. Ideia central

A plataforma assume automaticamente parte de atividades como:

- provisionamento;
- ajustes automáticos;
- algumas rotinas de atualização;
- automação de parte do ciclo operacional;
- administração de baixo nível em determinadas camadas.

## 13.3. Visão crítica

Deveríamos evitar tratar “autônomo” como ausência total de administração. O que muda é o nível e o foco da administração.

## 13.4. O que continua importante

Mesmo em banco autônomo, continuam relevantes:

- segurança;
- governança;
- desenho de dados;
- controle de acesso;
- observabilidade;
- custo;
- integração com aplicações;
- qualidade de SQL.

---

# 14. Administração on-premises x administração em nuvem

Esse comparativo é importante para dar maturidade ao módulo.

## 14.1. On-premises

No modelo on-premises, a organização costuma ter maior controle direto sobre:

- servidor;
- sistema operacional;
- armazenamento;
- instalação;
- configuração de baixo nível;
- políticas locais.

## 14.2. Nuvem

Na nuvem, parte dessas camadas passa a ser abstraída ou gerenciada pelo provedor, dependendo do serviço contratado.

## 14.3. O que tende a mudar

Pode mudar:

- o ponto de provisionamento;
- a forma de escalar;
- a responsabilidade por patching em algumas camadas;
- o modo de contratar infraestrutura;
- a integração com observabilidade e identidade da plataforma cloud.

## 14.4. O que permanece

Continuam importantes:

- segurança lógica;
- usuários;
- privilégios;
- monitoração;
- tuning;
- backup;
- recuperação;
- governança;
- desenho de dados.

---

# 15. Ambientes híbridos

## 15.1. O que são

Ambientes híbridos combinam recursos locais e em nuvem.

## 15.2. Por que são comuns

São comuns porque muitas organizações:

- não migram tudo de uma vez;
- mantêm sistemas críticos locais;
- usam nuvem para expansão, contingência ou novos projetos;
- combinam legados com arquitetura moderna.

## 15.3. Desafios administrativos

Em ambientes híbridos, deveríamos lidar com:

- integração de dados;
- consistência de identidade e acesso;
- governança distribuída;
- sincronização de ambientes;
- observabilidade em múltiplas camadas;
- estratégia de backup e recuperação em contextos distintos.

---

# 16. Multitenant e cloud como parte da mesma tendência

Esses dois temas se conectam diretamente.

## 16.1. Relação conceitual

A arquitetura multitenant favorece:

- consolidação;
- isolamento lógico;
- provisionamento mais ágil;
- melhor aproveitamento de infraestrutura.

Esses elementos são altamente compatíveis com a lógica de nuvem.

## 16.2. Visão estratégica

Deveríamos entender que o movimento para multitenant não é isolado. Ele faz parte de uma transição maior do Oracle para ambientes mais compartilhados, automatizados e orientados a serviço.

---

# 17. Governança, segurança e custo em nuvem

Ao falar de cloud, não deveríamos ficar apenas na camada técnica. Administração também envolve governança.

## 17.1. Segurança

Deveríamos continuar observando:

- identidade;
- privilégio;
- segmentação;
- rastreabilidade;
- proteção de dados.

## 17.2. Governança

A nuvem exige disciplina de:

- padronização;
- naming;
- organização de ambientes;
- acompanhamento de uso;
- controle de permissões;
- documentação operacional.

## 17.3. Custo

Em cloud, consumo de recursos tem impacto direto no custo operacional. Por isso, desempenho, sizing e governança passam a ter reflexo ainda mais claro em orçamento.

---

# 18. Relação com os módulos anteriores

Este módulo fecha a disciplina conectando administração tradicional com evolução arquitetural.

## 18.1. Relação com o Módulo 1

A distinção entre instância, banco, arquitetura e parâmetros prepara a compreensão do modelo multitenant.

## 18.2. Relação com o Módulo 2

Segurança, usuários e privilégios continuam existindo em ambiente multitenant e em nuvem, mas com novos contextos de escopo e governança.

## 18.3. Relação com o Módulo 3

Backup e recuperação continuam centrais, inclusive em ambientes consolidados e cloud.

## 18.4. Relação com o Módulo 4

Monitoramento, tuning e desempenho continuam relevantes, agora em cenário com múltiplas PDBs e possível abstração de infraestrutura.

---

# 19. Encaminhamento para a prática

Na parte prática deste módulo, deveríamos transformar esses conceitos em operações introdutórias como:

- identificação do CDB e das PDBs existentes;
- abertura e fechamento de PDB;
- criação ou clone de PDB, quando o ambiente permitir;
- observação de escopo administrativo;
- consultas em visões relacionadas a multitenant;
- contextualização de OCI, DBaaS e Autonomous Database;
- análise de cenários on-premises, cloud e híbridos.

---

# 20. Resumo executivo do módulo

## O que este módulo deverá consolidar

- multitenant como marco arquitetural do Oracle 12c;
- distinção entre CDB e PDB;
- operações administrativas básicas em PDBs;
- importância de clone, plug e unplug;
- OCI como plataforma de nuvem da Oracle;
- DBaaS e Autonomous Database como modelos de serviço;
- diferenças entre administração local, em nuvem e híbrida.

## O que não deveríamos fazer

- tratar multitenant como mera mudança de nomenclatura;
- reduzir cloud a discurso institucional;
- imaginar que banco em nuvem elimina a necessidade de administração;
- ignorar governança, segurança e custo em ambiente cloud.

## Resultado esperado

Ao final da parte teórica, deveríamos ter um mapa claro da arquitetura multitenant e da posição do Oracle em ambientes de nuvem, com base suficiente para construir uma prática introdutória coerente e alinhada à evolução da administração de bancos Oracle.
