# Módulo 2 – Segurança, Controle de Acesso e Carga de Dados em Volume

## Visão geral

Este módulo deverá introduzir dois pilares centrais da administração de bancos Oracle:

- a **segurança do ambiente**, com foco em autenticação, autorização, usuários, perfis, privilégios, roles, auditoria e rastreabilidade;
- os **procedimentos de carga de dados em volume**, com foco em ferramentas e estratégias para entrada, movimentação e importação de dados em larga escala.

A lógica deste módulo é importante porque administrar banco de dados não significa apenas manter o ambiente em funcionamento. Também deveríamos garantir que o acesso aos dados esteja corretamente controlado e que grandes volumes de informação possam ser carregados com segurança, desempenho e rastreabilidade.

## Carga horária sugerida

4 horas

**Distribuição sugerida:**  
2 horas de teoria + 2 horas de prática

## Objetivos do módulo

Ao final deste módulo, deveríamos ter consolidado os seguintes entendimentos:

- compreender o papel da segurança em ambientes Oracle;
- distinguir autenticação de autorização;
- compreender a relação entre usuário, esquema, privilégios e roles;
- entender como perfis e políticas de senha ajudam a controlar o ambiente;
- compreender a diferença entre privilégios de sistema e privilégios de objeto;
- entender o papel da auditoria e da rastreabilidade;
- reconhecer as principais estratégias de carga de dados em volume;
- compreender quando usar SQL*Loader, tabelas externas e Data Pump;
- relacionar segurança, governança e movimentação de dados em ambientes corporativos.

## O que este módulo precisa entregar

Este módulo não deverá ser tratado apenas como um conjunto de comandos de `CREATE USER`, `GRANT` ou importação de dados. Ele precisa entregar uma visão administrativa e organizacional.

Ao final, deveríamos ter conseguido:

1. entender como o Oracle controla identidade e permissões;
2. diferenciar acesso ao banco de acesso aos objetos;
3. compreender como estruturar um ambiente com menor risco e mais governança;
4. entender como registrar e rastrear ações relevantes;
5. compreender como grandes volumes de dados entram ou saem do ambiente Oracle;
6. reconhecer a diferença entre carga operacional, carga externa e exportação/importação lógica.

# 1. Segurança no ambiente Oracle

Segurança em banco de dados não deve ser tratada apenas como “senha”. Em Oracle, segurança envolve controle de acesso, rastreabilidade, integridade dos dados e separação de responsabilidades.

De forma geral, a segurança do ambiente deveria considerar:

- quem pode acessar;
- como esse acesso será realizado;
- o que cada identidade pode fazer;
- quais ações devem ser registradas;
- como restringir excessos de privilégio;
- como reduzir risco operacional e risco de vazamento.

Em contexto corporativo, a administração de segurança do banco costuma apoiar princípios como:

- **menor privilégio possível**;
- **segregação de funções**;
- **rastreabilidade das ações**;
- **controle centralizado de acesso**;
- **padronização de perfis e permissões**.

Esse ponto é central porque, na prática, muitos problemas em banco não surgem apenas de falha técnica, mas de permissões mal concedidas, usuários excessivamente poderosos e ausência de governança.

# 2. Conceitos de autenticação e autorização

Esse tema é obrigatório porque muitas vezes esses conceitos aparecem misturados.

## 2.1. Autenticação

Autenticação responde à pergunta:

**“Quem está tentando acessar?”**

Em outras palavras, é o processo de validar a identidade do usuário, aplicação ou serviço que deseja entrar no banco.

Exemplos de autenticação:

- login por usuário e senha;
- autenticação integrada ao sistema operacional;
- autenticação externa;
- autenticação centralizada em diretórios ou serviços corporativos.

## 2.2. Autorização

Autorização responde à pergunta:

**“O que essa identidade pode fazer?”**

Depois que a identidade é reconhecida, o Oracle precisa determinar quais operações serão permitidas.

Exemplos:

- criar tabela;
- consultar uma view;
- alterar dados;
- criar usuário;
- executar procedimento;
- exportar dados;
- acessar objetos de outro esquema.

## 2.3. Diferença prática

A distinção é simples, mas fundamental:

- **autenticação** valida a identidade;
- **autorização** define os poderes dessa identidade.

Em termos administrativos, deveríamos sempre lembrar que um usuário autenticado não deve automaticamente possuir permissões amplas. A boa administração depende justamente de separar bem essas duas dimensões.

# 3. Usuários e administração de identidades

No Oracle, o conceito de usuário tem papel central porque ele se relaciona diretamente com acesso, posse de objetos e organização do ambiente.

## 3.1. O que é um usuário

Um usuário no Oracle representa uma identidade de acesso ao banco. Essa identidade pode ser usada por:

- pessoas;
- aplicações;
- integrações;
- processos automatizados;
- rotinas administrativas.

## 3.2. Usuário e esquema

Em Oracle, um ponto importante é a relação entre **usuário** e **schema**.

Na prática, quando um usuário é criado, normalmente existe um esquema associado ao seu nome. Esse esquema funciona como o espaço lógico onde os objetos pertencentes àquele usuário são armazenados.

Isso é importante porque muitas vezes não deveríamos pensar apenas em “quem entra”, mas também em:

- quem é dono dos objetos;
- onde as tabelas e views ficam organizadas;
- como separar objetos administrativos, operacionais e de aplicação.

## 3.3. Administração de usuários

A administração de usuários envolve tarefas como:

- criação de contas;
- bloqueio e desbloqueio;
- expiração de senha;
- definição de tablespaces padrão;
- controle de cota de armazenamento;
- concessão e revogação de privilégios;
- vinculação a perfis e roles.

## 3.4. Organização recomendada

Em ambientes bem administrados, não deveríamos conceder tudo diretamente a todos os usuários. O ideal costuma ser:

- criar identidades com propósito definido;
- separar usuários administrativos de usuários de aplicação;
- restringir privilégios diretos;
- padronizar permissões por roles;
- usar perfis para padronizar políticas.

# 4. Perfis e políticas de senha

Perfis são um recurso importante porque permitem aplicar regras de segurança e governança de forma padronizada.

## 4.1. O que é um perfil

Um perfil é um conjunto de limites e regras aplicado a usuários.

Por meio de perfis, podemos controlar aspectos como:

- tentativas inválidas de login;
- tempo de bloqueio;
- tempo de vida da senha;
- políticas de reutilização;
- limites de sessão;
- limites de recursos.

## 4.2. Por que perfis são importantes

Sem perfil, o ambiente tende a crescer de forma desorganizada. Cada usuário acaba ficando com configurações isoladas, o que dificulta controle, auditoria e manutenção.

Com perfis, conseguimos:

- padronizar regras;
- reduzir risco;
- aplicar políticas corporativas;
- facilitar administração em escala.

## 4.3. Políticas de senha

Políticas de senha ajudam a impor regras mínimas de segurança, como:

- complexidade;
- expiração;
- histórico;
- bloqueio após várias falhas;
- tempo de reutilização.

Essas políticas são relevantes especialmente em ambientes onde o banco é acessado diretamente por pessoas ou por múltiplos times.

## 4.4. Relação com governança

Perfis e políticas de senha não são apenas detalhes técnicos. Eles ajudam a transformar um ambiente “artesanal” em um ambiente com controle administrativo consistente.

# 5. Privilégios de sistema e privilégios de objeto

Esse é um dos tópicos mais importantes do módulo.

## 5.1. Privilégios de sistema

Privilégios de sistema permitem executar ações administrativas ou estruturais no banco.

Exemplos típicos:

- criar sessão;
- criar tabela;
- criar usuário;
- criar procedure;
- alterar estrutura;
- administrar determinados recursos.

Esses privilégios não dizem respeito a um objeto específico. Eles definem capacidades mais amplas dentro do ambiente.

## 5.2. Privilégios de objeto

Privilégios de objeto permitem agir sobre um objeto específico, como:

- selecionar dados de uma tabela;
- inserir registros;
- atualizar dados;
- excluir dados;
- executar uma procedure;
- referenciar uma tabela.

Aqui o controle é mais granular.

## 5.3. Diferença administrativa

A diferença prática é:

- **privilégio de sistema** controla ações amplas no banco;
- **privilégio de objeto** controla ações sobre objetos específicos.

## 5.4. Implicação de segurança

Esse ponto é essencial porque muitos ambientes se tornam inseguros quando privilégios de sistema são concedidos em excesso. Em geral, deveríamos preferir:

- menos privilégios amplos;
- mais controle específico;
- uso de roles padronizadas;
- menos concessão direta desnecessária.

# 6. Roles e organização do acesso

Roles existem para facilitar administração, padronização e governança.

## 6.1. O que é uma role

Uma role é um agrupamento lógico de privilégios.

Em vez de conceder dezenas de permissões diretamente a cada usuário, podemos organizar esses privilégios dentro de uma role e depois atribuir a role aos usuários adequados.

## 6.2. Vantagens do uso de roles

O uso de roles ajuda a:

- simplificar administração;
- padronizar permissões;
- reduzir erros manuais;
- facilitar revogação e revisão de acesso;
- apoiar segregação de funções.

## 6.3. Exemplo conceitual

Poderíamos ter, por exemplo:

- uma role de leitura;
- uma role de operador;
- uma role de integração;
- uma role administrativa restrita;
- uma role específica para carga de dados.

Assim, o ambiente fica menos dependente de concessões individuais desorganizadas.

## 6.4. Governança e menor privilégio

Roles ajudam muito a aplicar o princípio do menor privilégio. Em vez de “dar tudo” para facilitar, deveríamos montar conjuntos coerentes e rastreáveis de permissões.

# 7. Auditoria e rastreabilidade

Em ambientes corporativos, segurança sem rastreabilidade é incompleta.

## 7.1. O que é auditoria

Auditoria é o registro controlado de ações relevantes realizadas no banco.

Esse registro pode incluir, por exemplo:

- tentativas de login;
- acessos a objetos críticos;
- operações administrativas;
- criação e remoção de usuários;
- concessão de privilégios;
- alterações em estruturas;
- execuções relevantes.

## 7.2. O que é rastreabilidade

Rastreabilidade é a capacidade de reconstruir o histórico do que aconteceu:

- quem fez;
- quando fez;
- em que objeto fez;
- de qual origem;
- com qual resultado.

## 7.3. Por que isso importa

Auditoria e rastreabilidade são importantes para:

- investigação de incidentes;
- conformidade;
- governança;
- segurança;
- revisão de acessos;
- identificação de uso indevido.

## 7.4. Visão administrativa

Deveríamos tratar auditoria não como “peso extra”, mas como mecanismo de proteção do próprio ambiente. Em contextos reais, muitas vezes o problema não é apenas impedir uma ação, mas conseguir provar que ela ocorreu, por quem foi executada e em qual momento.

# 8. Procedimentos de carga de dados em volume

A segunda metade do módulo trata da entrada e movimentação de grandes volumes de dados.

## 8.1. O que é carga de dados em volume

Carga em volume é o processo de inserir, importar ou disponibilizar grandes quantidades de dados no banco de forma planejada, eficiente e controlada.

Ela aparece em vários cenários, como:

- migração de sistemas;
- carga inicial de ambiente;
- integração entre plataformas;
- recebimento de arquivos externos;
- reprocessamento;
- atualização massiva;
- importação/exportação de estruturas e dados.

## 8.2. Desafios típicos

Grandes cargas costumam exigir atenção a:

- desempenho;
- consistência;
- formato dos arquivos;
- tratamento de erros;
- controle transacional;
- impacto em produção;
- segurança de acesso aos dados;
- rastreabilidade da operação.

## 8.3. Relação com administração

Carga em volume não é apenas tema de desenvolvimento. É tema de administração porque mexe com:

- performance;
- armazenamento;
- permissões;
- planejamento operacional;
- janelas de execução;
- controle de falhas.

# 9. SQL*Loader

SQL*Loader é uma das ferramentas clássicas do Oracle para carga de dados.

## 9.1. O que é

SQL*Loader é um utilitário voltado para carregar dados de arquivos externos para tabelas Oracle.

## 9.2. Quando faz sentido usar

Deveríamos considerar SQL*Loader em cenários como:

- carga de arquivos texto;
- importação de CSV ou arquivos delimitados;
- entrada controlada de dados estruturados;
- cargas repetitivas com layout conhecido.

## 9.3. Como funciona conceitualmente

Ele normalmente trabalha com:

- um arquivo de dados;
- um arquivo de controle;
- definição de layout;
- regras de mapeamento;
- tratamento de erros e rejeições.

## 9.4. Vantagens

- ferramenta tradicional e consolidada;
- boa para cargas estruturadas;
- controle detalhado do layout;
- integração com rotinas operacionais.

## 9.5. Limitações

- exige preparação de controle;
- menos amigável para exploração ad hoc;
- depende de um fluxo mais operacional do que analítico.

# 10. Tabelas externas

Tabelas externas oferecem uma abordagem bastante interessante para leitura de dados externos.

## 10.1. O que são

Tabelas externas permitem que arquivos externos sejam lidos como se fossem tabelas do banco, sem que os dados precisem ser carregados imediatamente para dentro de uma tabela interna tradicional.

## 10.2. Ideia central

O Oracle cria uma definição lógica sobre um arquivo externo. Assim, o arquivo pode ser consultado com SQL, respeitando layout e metadados definidos.

## 10.3. Quando são úteis

Deveríamos considerar tabelas externas quando quisermos:

- consultar um arquivo antes de carregá-lo;
- validar dados de entrada;
- integrar processos ETL;
- separar leitura externa de carga definitiva;
- explorar dados com SQL sem ingestão imediata.

## 10.4. Vantagens

- flexibilidade;
- integração com SQL;
- boa para inspeção e validação;
- útil em pipelines de ingestão.

## 10.5. Limitação conceitual

Elas não substituem toda forma de carga. Em muitos casos, funcionam melhor como etapa intermediária de leitura, validação e transformação.

# 11. Oracle Data Pump

Data Pump é a ferramenta lógica moderna de exportação e importação do Oracle.

## 11.1. O que é

Oracle Data Pump é o conjunto de utilitários usado para exportar e importar dados e metadados do banco.

Em termos conceituais, ele é usado para:

- movimentar schemas;
- exportar tabelas;
- transferir metadados;
- migrar ambientes;
- copiar estruturas;
- apoiar refresh ou migração lógica.

## 11.2. Principais usos

- exportação lógica;
- importação lógica;
- migração entre ambientes;
- clonagem de conteúdo;
- transporte seletivo de objetos.

## 11.3. Diferença em relação ao SQL*Loader

A diferença principal é que o Data Pump trabalha mais com a lógica interna do banco, exportando e importando objetos e dados Oracle, enquanto o SQL*Loader foca na carga de arquivos externos para tabelas.

## 11.4. Relevância administrativa

O Data Pump é extremamente importante porque aparece em:

- manutenção;
- migração;
- refresh de ambientes;
- backup lógico;
- integração entre bancos.

# 12. Comparação conceitual entre SQL*Loader, tabelas externas e Data Pump

Esse comparativo é importante porque ajuda a organizar o raciocínio do módulo.

## 12.1. SQL*Loader

Deveríamos associar a:

- carga de arquivos externos estruturados;
- ingestão de dados em tabela;
- rotinas repetitivas de carga.

## 12.2. Tabelas externas

Deveríamos associar a:

- leitura de arquivos como tabela;
- validação;
- exploração;
- integração SQL sobre arquivo externo.

## 12.3. Data Pump

Deveríamos associar a:

- exportação e importação lógica;
- movimentação entre ambientes Oracle;
- migração de objetos e dados internos do ecossistema Oracle.

## 12.4. Regra prática de escolha

De forma resumida:

- se o dado vem de **arquivo externo estruturado**, tende a fazer sentido pensar em **SQL*Loader**;
- se quisermos **consultar ou validar o arquivo com SQL**, tende a fazer sentido pensar em **tabela externa**;
- se quisermos **exportar/importar objetos e dados Oracle**, tende a fazer sentido pensar em **Data Pump**.

# 13. Relação entre segurança e carga de dados

Este módulo fica mais forte quando mostramos que segurança e carga não são assuntos separados.

Toda carga relevante deveria levantar perguntas como:

- quem pode executar a carga;
- em qual esquema os dados entrarão;
- quais objetos serão afetados;
- como limitar privilégios da rotina;
- como registrar a operação;
- como validar origem e integridade do arquivo;
- como tratar erros e rejeições;
- como evitar exposição indevida de dados.

Em outras palavras, carga de dados também é tema de governança.

# 14. Encaminhamento para a prática

Na parte prática deste módulo, deveríamos transformar esses conceitos em operações concretas, incluindo:

- criação e administração de usuários;
- aplicação de perfis;
- concessão de privilégios e roles;
- observação de metadados e visões relacionadas à segurança;
- simulação de carga com ferramentas Oracle;
- comparação entre abordagens de ingestão e importação.

# 15. Resumo executivo do módulo

## O que este módulo deverá consolidar

- segurança como disciplina administrativa do banco;
- diferença entre autenticação e autorização;
- importância de usuários, perfis, privilégios e roles;
- necessidade de auditoria e rastreabilidade;
- fundamentos das cargas em volume;
- distinção entre SQL*Loader, tabelas externas e Data Pump.

## O que não deveríamos fazer

- reduzir segurança a “senha”;
- tratar privilégios de forma desorganizada;
- misturar exportação lógica com carga externa sem diferenciar;
- apresentar ferramentas sem explicar quando usar cada uma.

## Resultado esperado

Ao final da parte teórica, deveríamos ter um mapa claro de como o Oracle organiza identidades, permissões, rastreamento e entrada de dados em volume. Isso criará base suficiente para construir a parte prática do módulo com consistência.

# 16. Refinamentos essenciais para ambiente corporativo

## 16.1. Multitenant: usuário comum x usuário local

No Oracle multitenant, deveríamos diferenciar:

- **usuário comum (CDB)**: válido em todos os containers, normalmente com prefixo `C##`;
- **usuário local (PDB)**: válido apenas na PDB onde foi criado.

Para este módulo, o fluxo didático tende a funcionar melhor com **usuários locais em `FREEPDB1`**, pois isso reduz risco e evita confusão operacional.

## 16.2. Princípio operacional de menor privilégio

Em práticas de segurança, deveríamos adotar como padrão:

- conceder apenas o necessário;
- preferir role em vez de concessão direta em excesso;
- separar contas administrativas de contas de aplicação;
- revisar privilégios periodicamente.

## 16.3. Separação por responsabilidade

Uma organização mínima recomendada:

- conta de aplicação (dona de objetos);
- conta de leitura (consulta);
- conta de carga (ingestão);
- conta administrativa (somente operações de administração).

Essa separação reduz impacto de erro humano e melhora rastreabilidade.

# 17. Decisão rápida de ferramenta (carga em volume)

## 17.1. Matriz resumida

| Cenário | Ferramenta mais adequada |
|---|---|
| Arquivo CSV/TXT para tabela Oracle | SQL*Loader |
| Validar/consultar arquivo sem carga imediata | Tabela externa |
| Exportar/importar objetos e dados Oracle | Data Pump |
| Replicação/CDC entre ambientes | GoldenGate (quando aplicável) |

## 17.2. Regra prática de escolha

- Se o dado entra por arquivo estruturado: começar pensando em **SQL*Loader**.
- Se a necessidade é inspeção/validação com SQL sobre arquivo: usar **tabela externa**.
- Se a necessidade é migração lógica Oracle-Oracle: usar **Data Pump**.

# 18. Riscos comuns e prevenção

## 18.1. Segurança

Riscos recorrentes:

- privilégios amplos demais;
- uso excessivo de contas administrativas;
- ausência de trilha de auditoria;
- falta de padrão em perfis e roles.

Prevenção recomendada:

- role por função;
- auditoria habilitada para ações críticas;
- revisão periódica de concessões;
- política de senha e bloqueio de contas inativas.

## 18.2. Carga de dados

Riscos recorrentes:

- carga sem validação de layout;
- execução sem isolamento de permissões;
- ausência de registro de erro/rejeição;
- impacto em janela de produção.

Prevenção recomendada:

- validar arquivo antes da carga final;
- usar conta de carga dedicada;
- registrar logs técnicos da operação;
- testar volume e tempo em ambiente controlado.

# 19. Checklist de fechamento da teoria

Ao concluir a teoria do módulo 2, deveríamos conseguir responder com segurança:

- qual é a diferença entre autenticação e autorização;
- como usuários, perfis, privilégios e roles se relacionam;
- quando usar privilégio de sistema versus privilégio de objeto;
- por que auditoria e rastreabilidade são obrigatórias em governança;
- quando escolher SQL*Loader, tabela externa ou Data Pump;
- como conectar carga em volume com segurança e controle de acesso.
