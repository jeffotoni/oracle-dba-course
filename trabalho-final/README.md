# Trabalho Final

Este diretório organiza os temas do trabalho final por grupo.

## Objetivo

Cada grupo deve construir uma ferramenta simples usando Oracle, com foco em demonstração prática em sala.

A ideia do trabalho não é fazer algo grande. A ideia é mostrar:

- entendimento do problema;
- modelagem mínima;
- uso do Oracle;
- uma interface ou fluxo de uso simples;
- uma apresentação curta e clara.

## Linha geral do trabalho

Os trabalhos foram pensados para manter a mesma lógica do curso:

```txt
Oracle como banco
Oracle como plataforma observável
Oracle como suporte de aplicação
Oracle como base para API e busca moderna
```

Ou seja, os grupos não precisam construir sistemas grandes. Precisam construir **ferramentas pequenas, entendíveis e demonstráveis**.

## Regra prática

```txt
Ferramenta simples > sistema grande incompleto
Demonstração prática > excesso de teoria
```

## Grupos

### Grupo 1

Tema sugerido:

- dashboard simples de estatísticas Oracle

Ideia:

- ler views do Oracle;
- expor por API ou ler direto;
- atualizar periodicamente;
- mostrar dados de instância, sessões ou estatísticas.

Detalhamento:

- `trabalho-final/grupo1/README.md`

### Grupo 2

Tema sugerido:

- cache simples key-value com Oracle

Ideia:

- tabela de chave e valor;
- `POST` para gravar;
- `GET` para buscar;
- `DELETE` para remover;
- opcionalmente expiração simples.

Detalhamento:

- `trabalho-final/grupo2/README.md`

### Grupo 3

Tema sugerido:

- busca vetorial simples com Oracle

Ideia:

- texto;
- embedding local;
- armazenamento vetorial no Oracle;
- consulta por similaridade;
- resultado simples em tela ou API.

Detalhamento:

- `trabalho-final/grupo3/README.md`

## O que todos os grupos devem ter

Mesmo com tecnologias diferentes, todos os grupos devem buscar:

- problema simples e claro;
- modelagem mínima coerente;
- uso real do Oracle;
- demonstração prática;
- explicação objetiva do fluxo.

## O que vale como entrega mínima

Uma entrega boa já pode ser:

- banco Oracle funcionando;
- tabelas criadas;
- dados de exemplo;
- API simples ou interface simples;
- roteiro curto de uso;
- apresentação funcionando ao vivo.

## Entrega mínima por grupo

Independentemente da tecnologia escolhida, cada grupo deve entregar pelo menos:

- um `README.md` explicando a ideia, a arquitetura mínima e como executar;
- os scripts SQL principais de criação e carga inicial;
- o código da API, interface ou script usado na demonstração;
- um roteiro simples para apresentação em sala;
- uma demonstração prática funcionando.

## O que não é necessário

Não é necessário:

- autenticação complexa;
- frontend sofisticado;
- arquitetura distribuída;
- deploy em nuvem;
- sistema grande.

Se o grupo quiser evoluir, ótimo. Mas o mínimo bem feito vale mais do que um escopo ambicioso mal executado.

## Apresentação

Cada grupo deve apresentar:

- o problema escolhido;
- a modelagem mínima usada;
- a tecnologia escolhida;
- como a solução funciona;
- uma demonstração prática;
- principais decisões e limitações.

## Observação importante

Os temas e exemplos deste diretório servem como **inspiração e direção**, não como limitação rígida.

O objetivo é ajudar o grupo a começar melhor, com menos atrito.

## Leitura prática dos três temas

### Grupo 1

Mostra o Oracle como ambiente observável.

### Grupo 2

Mostra o Oracle como suporte simples para aplicação.

### Grupo 3

Mostra o Oracle como base moderna para busca vetorial e IA.

## Referência inicial

- `aula4-xespecial-apis/README.md`
- `aula5-xespecial-ords/README.md`
- `repo/go.oracle/v1/README.md`
- `repo/oracle/ords/README.md`
