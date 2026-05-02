# Curso Oracle Database Administration (DBA)

## ✦ Sobre o autor

Desenvolvido por **Jefferson Otoni Lima (Jeffotoni)**, **Engenheiro de Software Sênior**, **Arquiteto de Soluções** e **instrutor técnico**, com mais de **22 anos de experiência** na construção de sistemas distribuídos de alta performance.

Atua com foco em **arquitetura de software**, **design de APIs**, **backend em escala**, **cloud-native**, **Go**, **containers**, **DevOps**, **observabilidade** e **infraestrutura moderna para aplicações críticas**.

Também possui forte atuação em **bancos de dados** e **administração de dados** em diferentes modelos, incluindo:

- **relacionais**
- **NoSQL**
- **vetoriais**
- **temporais**
- **graph**
- **cache**
- **motores especializados para alta escala e baixa latência**

É criador do **Quick Framework**, autor do **Go Bootcamp** e contribuidor ativo da comunidade **Go** no Brasil e no exterior.

## ✦ Sobre este curso

Este repositorio concentra o material do curso de Oracle Database Administration, do `Modulo 0` ao `Modulo 5`, com apoio pratico em Oracle Free / XE, Podman, CloudBeaver e exemplos de aplicacao em Go.

O objetivo nao e apenas apresentar teoria de Oracle. O curso foi organizado para que seja possivel:

- entender a arquitetura basica do Oracle;
- subir o ambiente local;
- conectar corretamente na instancia e na PDB;
- criar usuario, schema, tabela e consultas;
- evoluir depois para administracao, seguranca, backup, tuning e multitenant.

## ✦ Público-alvo

Este curso foi pensado para:

- iniciantes em Oracle;
- desenvolvedores que precisam entender melhor banco de dados;
- analistas e administradores que querem consolidar base em Oracle DBA;
- pessoas que preferem aprender com laboratório real.

## ✦ Abordagem do curso

A abordagem do curso e direta e progressiva:

- primeiro entender a base conceitual;
- depois subir o ambiente;
- em seguida conectar, consultar e criar objetos;
- so entao avancar para administracao, seguranca, backup, tuning e multitenant.

## Regra central do curso

Se esta sequencia nao estiver clara:

```txt
conexao -> PDB -> user/schema -> tabela -> query -> Oracle rodando
```

o resto perde valor.

Por isso, o curso precisa comecar por duas bases ao mesmo tempo:

- base operacional;
- base conceitual.

Na pratica, isso significa que a entrada real do curso e:

- `modulo0-material`
- `modulo0-guia-pratico`
- `podman`
- `repositorio/oracle`
- `repositorio/go.oracle/v1`

antes de entrar forte em `modulo1-material`.

## Por onde comecar

A trilha inicial recomendada e esta:

1. ler `modulo0-material/README.md`;
2. ler `modulo0-guia-pratico/README.md`;
3. aprofundar a duvida sobre `CDB`, `PDB`, `SID`, `Service Name` e `CREATE DATABASE` em `modulo0-guia-pratico/oracle_create_database_guide-v2.md`;
4. preparar ambiente com `podman/README.md`;
5. subir Oracle com `repositorio/oracle/versoes/README.md`;
6. validar conexao e operacoes basicas na IDE;
7. testar exemplo de aplicacao com `repositorio/go.oracle/v1/README.md`;
8. entrar depois em `modulo1-material`.

## Mapa do repositorio

### Base conceitual inicial

- `modulo0-material/README.md`
  - fundamentos de banco de dados;
  - contexto Oracle;
  - edicoes, custo, decisao tecnica e panorama atual.

- `modulo0-guia-pratico/README.md`
  - leitura da IDE;
  - conexao;
  - schemas;
  - tablespaces;
  - roles;
  - sequencia correta de trabalho no Oracle Free / XE.

- `modulo0-guia-pratico/oracle_create_database_guide-v2.md`
  - explicacao robusta do ponto onde mais ha confusao no inicio:
  - `FREE`, `FREEPDB1`, `CDB`, `PDB`, `SID`, `Service Name`;
  - quando usar `CREATE DATABASE`;
  - quando criar apenas usuario, schema e tabela.

### Base operacional inicial

- `podman/README.md`
  - uso de Podman no curso;
  - comandos base;
  - build, run, volumes e compose;
  - ponte para exemplos reais.

- `podman/go-exemplos.md`
  - exemplos praticos com projetos Go.

- `podman/oracle-exemplos.md`
  - exemplos de Oracle rodando com Podman.

- `repositorio/oracle/versoes/README.md`
  - catalogo das versoes Oracle usadas no laboratorio;
  - visao macro das diferentes formas de subir Oracle.

- `repositorio/oracle/versoes/free-full-23ai/README.md`
  - versao mais completa e didatica do laboratorio Oracle;
  - referencia principal para demonstracao.

- `repositorio/go.oracle/v1/README.md`
  - exemplo simples de API em Go conectando ao Oracle;
  - CRUD HTTP para mostrar Oracle em uso real.

### Modulos do curso

- `modulo1-material`
  - arquitetura e configuracao do ambiente Oracle.
- `modulo2-material`
  - seguranca, controle de acesso e carga.
- `modulo3-material`
  - backup e recuperacao.
- `modulo4-material`
  - monitoramento, tuning e otimizacao.
- `modulo5-material`
  - multitenant e nuvem.

### Primeiro bloco: vamos rodar e entender

Este bloco vem antes do aprofundamento administrativo:

- subir o Oracle;
- conectar pela IDE;
- entender `PDB` e `Service Name`;
- criar usuario;
- entender que usuario e schema caminham juntos;
- criar tabela;
- executar `INSERT`, `SELECT`, `UPDATE` e `DELETE`;
- validar queries de ambiente;
- entender a diferenca entre o que e comando de cliente e o que e SQL Oracle.

### Segundo bloco: entrar em arquitetura e administracao

So depois disso entra com mais forca:

- `modulo1-material`;
- parametros;
- instancia;
- memoria;
- processos;
- arquivos fisicos e logicos;
- visoes dinamicas;
- multitenant com mais profundidade.

## Estrutura do curso por modulo

### Modulo 0: Fundamentos de Banco de Dados e Contextualizacao

Evolucao do armazenamento de dados, surgimento dos SGBDs, modelo relacional, panorama atual e base de decisao tecnica para Oracle.

- [Modulo 0 - Material principal](./modulo0-material/README.md)
- [Modulo 0 - Guia pratico](./modulo0-guia-pratico/README.md)
- [Modulo 0 - Create Database, CDB, PDB e Service Name](./modulo0-guia-pratico/oracle_create_database_guide-v2.md)

### Modulo 1: Arquitetura e Configuracao do Ambiente

Instancia vs banco de dados, estruturas de memoria, processos de background, arquivos fisicos e logicos.

- [Modulo 1 - Conteudo teorico](./modulo1-material/01-teoria-modulo1.md)
- [Modulo 1 - Guia pratico](./modulo1-material/02-pratica-modulo1.md)
- [Modulo 1 - Scripts SQL](./modulo1-material/scripts/)

### Modulo 2: Seguranca, Controle de Acesso e Carga de Dados

Autenticacao, autorizacao, usuarios, perfis, privilegios, roles e ferramentas de carga.

- [Modulo 2 - Conteudo teorico](./modulo2-material/02-teoria-modulo2.md)
- [Modulo 2 - Guia pratico](./modulo2-material/02-pratica-modulo2.md)
- [Modulo 2 - Laboratorio de carga](./modulo2-material/modulo2-seguranca-carga/)

### Modulo 3: Rotinas de Backup e Recuperacao

Fundamentos de RMAN, backup fisico e logico, completo e incremental, e cenarios de recuperacao.

- [Modulo 3 - Conteudo teorico](./modulo3-material/03-teoria-modulo3.md)
- [Modulo 3 - Guia pratico](./modulo3-material/03-pratica-modulo3.md)

### Modulo 4: Monitoramento, Tuning e Otimizacao

Visoes dinamicas, identificacao de gargalos, locks, waits, Explain Plan e otimizacao de consultas.

- [Modulo 4 - Conteudo teorico](./modulo4-material/04-teoria-modulo4.md)
- [Modulo 4 - Guia pratico](./modulo4-material/04-pratica-modulo4.md)

### Modulo 5: Multitenant e Nuvem

Arquitetura `CDB/PDB`, administracao de PDBs e visao geral de Oracle Cloud.

- [Modulo 5 - Conteudo teorico](./modulo5-material/05-teoria-modulo5.md)
- [Modulo 5 - Guia pratico](./modulo5-material/05-pratica-modulo5.md)

## Ambiente necessario

Para acompanhar as praticas, e recomendavel ter pelo menos:

### Software essencial

- `Podman`
- `DBeaver Community` ou outra IDE SQL equivalente
- `Git`
- `Visual Studio Code`
- `Go`, quando a aula entrar no exemplo de aplicacao

### Hardware recomendado

- sistema operacional: Windows 10/11 64 bits, macOS ou Linux;
- memoria RAM: minimo `8 GB`, ideal `16 GB`;
- espaco em disco: pelo menos `20 GB` livres;
- virtualizacao habilitada, quando exigida pelo ambiente local.

## Quick start de laboratorio

Fluxo minimo recomendado para a primeira pratica:

1. abrir `podman/README.md`;
2. escolher uma versao em `repositorio/oracle/versoes/README.md`;
3. subir preferencialmente `repositorio/oracle/versoes/free-full-23ai/README.md`;
4. conectar na IDE usando `Service Name`;
5. validar ambiente com `SELECT` em `v$instance`, `v$database`, `v$pdbs` e `SYS_CONTEXT`;
6. criar usuario;
7. criar tabela;
8. inserir e consultar dados;
9. opcionalmente testar a API em `repositorio/go.oracle/v1/README.md`.

## Referencias uteis

### Oracle

- [Oracle Help Center](https://docs.oracle.com/en/)
- [Database 23ai New Features](https://docs.oracle.com/en/database/oracle/oracle-database/23/nfjac/index.html)
- [Oracle Architecture Center](https://docs.oracle.com/en/solutions/)
- [Ask TOM](https://asktom.oracle.com/)
- [Oracle Base](https://oracle-base.com/)

### Ferramentas

- [DBeaver Community](https://dbeaver.io/)
- [Oracle SQL Developer](https://www.oracle.com/database/sqldeveloper/)
- [Oracle Container Registry](https://container-registry.oracle.com/)

## Uso do repositorio

- teoria: arquivos dos modulos;
- pratica Oracle: `modulo0-guia-pratico`, `podman` e `repositorio/oracle`;
- pratica de aplicacao: `repositorio/go.oracle/v1`;
- aprofundamento administrativo: `modulo1` ao `modulo5`.
