# Grupo 1 — Dashboard Simples de Estatísticas Oracle

## Tema

Construir uma ferramenta simples de monitoramento mostrando estatísticas atuais do Oracle.

## Objetivo

O grupo deve montar uma solução pequena que siga esta linha:

```txt
Oracle -> consulta de métricas -> API ou leitura direta -> atualização periódica -> dashboard simples
```

## Ideia do projeto

A proposta é criar um painel básico para mostrar que o Oracle pode ser observado em tempo real.

O foco não é fazer uma plataforma completa de observabilidade. O foco é demonstrar:

- leitura do banco em tempo real;
- atualização simples;
- interpretação mínima do que está sendo exibido.

## O que o trabalho deve demonstrar

- como consultar views administrativas do Oracle;
- como organizar os dados de monitoramento;
- como mostrar atualização periódica;
- como explicar o significado das métricas escolhidas.

## O que pode entrar no dashboard

O grupo pode escolher um conjunto pequeno de indicadores, por exemplo:

- nome da instância;
- status da instância;
- container atual;
- quantidade de sessões;
- waits principais;
- SQLs mais custosos;
- uso de tablespaces;
- estatísticas gerais do sistema.

## Escopo mínimo

### 1. Banco Oracle

O projeto deve consultar o Oracle já rodando no laboratório.

Exemplos de views úteis:

- `v$instance`
- `v$database`
- `v$session`
- `v$system_event`
- `v$sql`
- `dba_tablespaces`

> Observação: algumas views administrativas, como `v$system_event`, `v$sql` e `dba_tablespaces`, podem exigir privilégios mais altos. Se o grupo optar por essas consultas, deve validar antes com qual usuário irá apresentar.

## 2. API ou backend simples

O grupo pode escolher:

- API simples em Go, Node, Python, Java ou outra tecnologia;
- ou leitura direta do banco em uma aplicação web pequena.

Exemplos de endpoints:

- `GET /health`
- `GET /stats/instance`
- `GET /stats/sessions`
- `GET /stats/waits`
- `GET /stats/sql`

## 3. Interface

Uma tela simples já resolve bem.

Exemplo:

- cards com instância e banco;
- tabela com sessões;
- tabela com waits principais;
- atualização automática a cada 5 ou 10 segundos.

## Queries que podem servir de base

### Instância

```sql
SELECT instance_name,
       status,
       database_status
FROM v$instance;
```

### Banco

```sql
SELECT name,
       open_mode,
       log_mode
FROM v$database;
```

### Sessões

```sql
SELECT username,
       status,
       COUNT(*) AS total_sessions
FROM v$session
WHERE username IS NOT NULL
GROUP BY username, status
ORDER BY username, status;
```

### Waits

```sql
SELECT event,
       total_waits,
       time_waited
FROM v$system_event
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC
FETCH FIRST 10 ROWS ONLY;
```

### SQL custoso

```sql
SELECT sql_id,
       executions,
       elapsed_time,
       cpu_time,
       buffer_gets
FROM v$sqlarea
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;
```

> Observação: se a leitura de `v$sqlarea` não estiver liberada para o usuário da apresentação, o grupo pode reduzir o escopo e focar em instância, banco e sessões.

## Fluxo sugerido do sistema

1. conectar no Oracle;
2. criar consultas de monitoramento;
3. expor essas consultas em endpoints ou diretamente na tela;
4. atualizar os dados periodicamente;
5. apresentar o painel em sala.

## Interface

O grupo pode escolher uma destas opções:

### Opção A — Dashboard web simples

Uma tela com:

- cards de status;
- tabelas simples;
- refresh automático.

### Opção B — API + cliente

- backend expondo JSON;
- frontend simples consumindo a API.

### Opção C — Script + visualização simples

- script de coleta;
- exibição em terminal ou página simples;
- foco mais forte na explicação.

## O que eu sugiro como recorte ideal

Para apresentação em sala, o melhor equilíbrio costuma ser:

- backend pequeno;
- 3 ou 4 endpoints;
- frontend HTML simples;
- atualização automática.

## Estrutura mínima sugerida

```txt
grupo1/
├── README.md
├── app/
│   ├── main.(go|py|js)
│   └── ...
├── sql/
│   └── consultas.sql
└── docs/
```

## O que apresentar em sala

- quais métricas foram escolhidas;
- de quais views elas vieram;
- como a atualização foi feita;
- como interpretar a tela;
- demonstração ao vivo.

## O que avaliar no trabalho

- simplicidade;
- clareza;
- leitura correta das métricas;
- funcionamento;
- apresentação.

## Referências úteis

- `aula5-revisao-modulo4/README.md`
- `modulo4-material/04-teoria-modulo4.md`
- `modulo4-material/04-pratica-modulo4.md`
- `repo/go.oracle/v1/README.md`

## Observação final

O grupo não precisa tentar construir um “Grafana do Oracle”.

A meta é fazer algo pequeno, claro e funcional.

Um painel simples, bem explicado e demonstrável vale mais do que uma solução grande e confusa.
