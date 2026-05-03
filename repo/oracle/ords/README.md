# ORDS com Podman

> Laboratório simples para subir `ORDS` em modo standalone e expor objetos Oracle como REST, usando o Oracle já rodando no host.

## Visão geral

Neste laboratório, a ideia é conectar:

```txt
Browser / curl
   ↓
ORDS
   ↓
Oracle Free / XE
   ↓
FREEPDB1
```

Leitura prática:

- `Oracle Database` continua sendo o banco;
- `ORDS` funciona como camada REST;
- a porta mais comum deste laboratório é `8181`;
- o banco do curso continua em `FREEPDB1`.

## O que é ORDS

`ORDS` significa `Oracle REST Data Services`.

Em linguagem direta:

- `Oracle` = plataforma e banco Oracle;
- `REST` = padrão de API via HTTP;
- `Data` = dados, SQL, PL/SQL, metadata e objetos;
- `Services` = serviços expostos externamente.

Tradução prática:

```txt
Serviços REST de dados da Oracle
```

Definição técnica:

- `ORDS` é a camada oficial da Oracle que transforma objetos e lógica do Oracle Database em serviços REST acessíveis por HTTP e JSON.

Regra mental:

```txt
ORDS = Oracle Database como API
```

## Contexto histórico

O `ORDS` surgiu da evolução do antigo `Oracle APEX Listener` e passou a se tornar uma plataforma REST mais ampla dentro do ecossistema Oracle.

Hoje ele é usado para aproximar o banco de dados de cenários como:

- web;
- mobile;
- cloud;
- microservices;
- `APEX`;
- `Database Actions`;
- APIs JSON;
- integrações com IA, vetores e workloads modernos.

## Quando usar

Este laboratório faz sentido quando a proposta for:

- expor tabela ou schema Oracle via HTTP;
- testar JSON sem escrever backend custom;
- demonstrar REST nativo no ecossistema Oracle;
- introduzir `Database Actions`, `SQL Developer Web` e integração com `ORDS`.

## Premissas do laboratório

Antes de subir o `ORDS`, este ambiente já deve estar pronto:

- Oracle rodando em `Podman`;
- porta do Oracle publicada no host;
- `Service Name` conhecido;
- usuário e objetos de teste já criados.

Exemplo usado neste curso:

```txt
Oracle container: oracle-free-full-23ai
Host DB: localhost
Porta DB: 1522
Service Name: FREEPDB1
Senha administrativa: OraclePwd123
Porta ORDS: 8181
```

## Mapa mental

```txt
Mac / Linux / Windows
 ├── Oracle Free (Podman)
 │    └── FREEPDB1
 └── ORDS (Podman)
      └── http://localhost:8181/ords/
```

## Fluxo recomendado

1. confirmar que o Oracle já está rodando;
2. autenticar no Oracle Container Registry;
3. baixar a imagem do `ORDS`;
4. subir o container em modo standalone;
5. configurar conexão com `FREEPDB1`;
6. habilitar schema e objetos REST;
7. testar no browser e com `curl`.

## Custo e leitura prática

Para laboratório, a leitura mais útil é esta:

- `ORDS` normalmente não é o centro do custo;
- o custo costuma estar no Oracle Database, na infraestrutura e no suporte;
- em laboratório local, `Oracle Free + ORDS` tende a ser custo zero.

Regra mental:

```txt
Oracle = dados
ORDS = API layer
```

## Comandos principais com Podman

### 1. Login no registry da Oracle

```bash
podman login container-registry.oracle.com
```

### 2. Pull da imagem do ORDS

```bash
podman pull container-registry.oracle.com/database/ords:latest
```

### 3. Criar volume de configuração

```bash
podman volume create ords-config
```

### 4. Subir o ORDS

```bash
podman run -d \
  --name ords \
  -p 8181:8080 \
  -e DBHOST=host.containers.internal \
  -e DBPORT=1522 \
  -e DBSERVICENAME=FREEPDB1 \
  -e ORACLE_PWD=OraclePwd123 \
  -v ords-config:/etc/ords/config:Z \
  container-registry.oracle.com/database/ords:latest
```

### 5. Ver logs

```bash
podman logs -f ords
```

### 6. Entrar no container

```bash
podman exec -it ords bash
```

## Configuração inicial

Dentro do container, o fluxo prático inicial é:

```bash
ords --config /etc/ords/config install
```

Na instalação, normalmente será necessário informar:

- host do banco;
- porta;
- `Service Name`;
- credenciais administrativas;
- metadados do `ORDS`.

Neste laboratório, a leitura mental é:

```txt
Host: host.containers.internal
Port: 1522
Service Name: FREEPDB1
```

Durante a instalação, a leitura prática esperada é:

```txt
Connection Type: Basic
Hostname: host.containers.internal
Port: 1522
Service Name: FREEPDB1
SYS Username: sys
SYS Password: OraclePwd123
SYS Role: SYSDBA
```

## Estrutura que o ORDS cria no Oracle

Após a instalação, o Oracle passa a ter componentes internos do `ORDS`, como:

- `ORDS_METADATA`
- `ORDS_PUBLIC_USER`

Leitura prática:

```txt
FREE
 └── FREEPDB1
      ├── JEFF
      ├── ORDS_METADATA
      └── ORDS_PUBLIC_USER
```

## Primeiro teste

No browser:

```txt
http://localhost:8181/ords/
```

Ou com `curl`:

```bash
curl http://localhost:8181/ords/
```

Também vale validar no Oracle:

```sql
SELECT username
FROM dba_users
WHERE username LIKE 'ORDS%';
```

Observação:

- esta consulta deve ser executada com um usuário administrativo, como `SYSTEM` ou `SYS`;
- conectando como `JEFF`, `DBA_USERS` não estará disponível por padrão.

## Preparando a tabela de exemplo

Neste laboratório, a tabela usada para os testes REST é `JEFF.LLM_MODEL`.

Exemplo de criação:

```sql
CREATE USER jeff IDENTIFIED BY StrongPass123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO jeff;
```

Conectar como `JEFF` e criar a tabela:

```sql
CREATE TABLE llm_model (
  id                NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  nome              VARCHAR2(100) NOT NULL,
  provider          VARCHAR2(100),
  input_token_limit NUMBER,
  output_token_limit NUMBER,
  ativo             CHAR(1) DEFAULT 'S'
);

INSERT INTO llm_model (nome, provider, input_token_limit, output_token_limit, ativo)
VALUES ('gpt-4.1', 'openai', 128000, 16384, 'S');

INSERT INTO llm_model (nome, provider, input_token_limit, output_token_limit, ativo)
VALUES ('gpt-4o', 'openai', 128000, 16384, 'S');

INSERT INTO llm_model (nome, provider, input_token_limit, output_token_limit, ativo)
VALUES ('claude-3.7-sonnet', 'anthropic', 200000, 8192, 'S');

INSERT INTO llm_model (nome, provider, input_token_limit, output_token_limit, ativo)
VALUES ('gemini-1.5-pro', 'google', 1000000, 8192, 'S');

COMMIT;
```

## Habilitando schema e objetos REST

Depois que o `ORDS` estiver instalado, o próximo passo é habilitar o schema e os objetos desejados.

Conectar como `JEFF` e executar primeiro a habilitação do schema:

```sql
BEGIN
  ORDS.ENABLE_SCHEMA(
    p_enabled             => TRUE,
    p_schema              => 'JEFF',
    p_url_mapping_type    => 'BASE_PATH',
    p_url_mapping_pattern => 'jeff',
    p_auto_rest_auth      => FALSE
  );
END;
/

COMMIT;
```

Depois, ainda como `JEFF`, habilitar a tabela `LLM_MODEL`:

```sql
BEGIN
  ORDS.ENABLE_OBJECT(
    p_enabled     => TRUE,
    p_schema      => 'JEFF',
    p_object      => 'LLM_MODEL',
    p_object_type => 'TABLE'
  );
END;
/

COMMIT;
```

Leitura prática:

- `ORDS.ENABLE_SCHEMA` libera o schema para publicação REST;
- `ORDS.ENABLE_OBJECT` libera o objeto específico;
- para a tabela aparecer em `/ords/jeff/llm_model/`, os dois passos fazem sentido no fluxo didático do laboratório.

Endpoint esperado:

```txt
http://localhost:8181/ords/jeff/llm_model/
```

## Testes com curl

### GET da coleção

```bash
curl http://localhost:8181/ords/jeff/llm_model/
```

### GET de um item específico

```bash
curl http://localhost:8181/ords/jeff/llm_model/1
```

### POST

```bash
curl -X POST http://localhost:8181/ords/jeff/llm_model/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "claude-3.7-sonnet",
    "provider": "anthropic",
    "input_token_limit": 200000,
    "output_token_limit": 8192,
    "ativo": "S"
  }'
```

### PUT

```bash
curl -X PUT http://localhost:8181/ords/jeff/llm_model/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "gpt-4.1-updated",
    "provider": "openai",
    "input_token_limit": 128000,
    "output_token_limit": 32768,
    "ativo": "S"
  }'
```

### DELETE

```bash
curl -X DELETE http://localhost:8181/ords/jeff/llm_model/1
```

## Resultado esperado

Depois da habilitação REST, o fluxo passa a ser:

```txt
Mac Host
 ├── Oracle Free Container
 │    └── localhost:1522
 │         └── FREEPDB1
 │              └── JEFF.LLM_MODEL
 │
 └── ORDS Container
      └── localhost:8181
           └── REST API
```

## O que este laboratório entrega

- Oracle local exposto por HTTP;
- JSON sem backend custom;
- introdução prática a `ORDS`;
- base para evoluir depois para `Database Actions`, REST e integração web.

## Limitações e observações

- o `ORDS` não substitui uma aplicação completa em Go, Java ou outra linguagem;
- a configuração inicial pode variar por versão;
- imagens oficiais Oracle podem exigir autenticação no registry;
- o `latest` pode mudar com o tempo;
- se `host.containers.internal` falhar, pode ser necessário usar IP do host ou outra estratégia de rede.

## Leitura complementar

- [Manual rápido de comandos](./manual/comandos.md)
- [Catálogo de versões Oracle](../versoes/README.md)
- [Podman no curso](../../../podman/README.md)
