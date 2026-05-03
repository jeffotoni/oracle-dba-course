# Exemplos Oracle com Podman

Este arquivo consolida os exemplos Oracle do workspace usando Podman.

O foco aqui e usar:

- `podman run`
- `podman build`
- `podman compose`

sem depender de `script/up.sh` e `script/down.sh`.

O catalogo completo de versoes esta em:

```txt
repo/oracle/versoes/README.md
```

Para o curso, a sequência mais útil e:

1. `podman run`
2. conexão em Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente
3. queries de validação
4. depois `Containerfile`
5. por fim `podman compose`

## 1. Versao Mais Completa

A versao mais completa hoje e:

```txt
repo/oracle/versoes/free-full-23ai
```

Ela concentra tres formas didaticas de uso:

- `podman run`
- `Containerfile`
- `podman compose`

## 2. Oracle Free Full 23ai com `podman run`

Imagem:

```txt
container-registry.oracle.com/database/free:latest
```

Subir:

```bash
podman run -d \
  --name oracle-free-full-23ai \
  -p 1522:1521 \
  --cap-add SYS_NICE \
  -e ORACLE_PWD=OraclePwd123 \
  -e ORACLE_PDB=FREEPDB1 \
  -v oracle-free-full-23ai-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/free:latest
```

Ver logs:

```bash
podman logs -f oracle-free-full-23ai
```

Ver status:

```bash
podman ps --filter name=oracle-free-full-23ai
```

Remover container:

```bash
podman rm -f oracle-free-full-23ai
```

Remover volume de dados:

```bash
podman volume rm oracle-free-full-23ai-data
```

## 3. Oracle Free Full 23ai com `Containerfile`

Arquivo:

```txt
repo/oracle/versoes/free-full-23ai/containerfile/Containerfile
```

Build:

```bash
cd repo/oracle/versoes/free-full-23ai
podman build -t oracle-free-full-23ai:23ai -f containerfile/Containerfile .
```

Run da imagem local:

```bash
podman run -d \
  --name oracle-free-full-23ai \
  -p 1522:1521 \
  --cap-add SYS_NICE \
  -e ORACLE_PWD=OraclePwd123 \
  -e ORACLE_PDB=FREEPDB1 \
  -v oracle-free-full-23ai-data:/opt/oracle/oradata:Z \
  oracle-free-full-23ai:23ai
```

## 4. Oracle Free Full 23ai com `podman compose`

Arquivo:

```txt
repo/oracle/versoes/free-full-23ai/compose/compose.yaml
```

Subir:

```bash
cd repo/oracle/versoes/free-full-23ai/compose
podman compose build
podman compose up -d
```

Ver status:

```bash
podman compose ps
```

Ver logs:

```bash
podman compose logs -f oracle-free-full-23ai
```

Derrubar:

```bash
podman compose down
```

Derrubar apagando volume:

```bash
podman compose down -v
```

### Observacao importante sobre compose

Se aparecer erro de nome de container ja em uso:

```bash
podman rm -f oracle-free-full-23ai
```

Se o volume ja existir e o compose reclamar que ele nao foi criado por compose, trate o volume como externo no `compose.yaml` ou remova o volume manualmente.

## 5. Credenciais de Conexao

### Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente no host

```txt
Host: localhost
Port: 1522
Connection type: Service Name
Service Name: FREEPDB1
User: system
Password: OraclePwd123
```

### Cliente SQL em container

```txt
Host: host.containers.internal
Port: 1522
Connection type: Service Name
Service Name: FREEPDB1
User: system
Password: OraclePwd123
```

## 6. Outras Versoes Oracle com `podman run`

### Oracle Free Lite 23ai

```bash
podman run -d \
  --name oracle-free-lite-23ai \
  -p 1521:1521 \
  -e ORACLE_PWD=OraclePwd123 \
  -e ORACLE_PDB=FREEPDB1 \
  -v oracle-free-lite-23ai-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/free:latest-lite
```

### Oracle XE 21 Slim

```bash
podman run -d \
  --name oracle-xe-21-slim \
  -p 1523:1521 \
  -e ORACLE_PASSWORD=OraclePwd123 \
  -v oracle-xe-21-slim-data:/opt/oracle/oradata:Z \
  gvenzl/oracle-xe:21-slim
```

Conexao esperada:

```txt
Host: localhost
Port: 1523
Service Name: XEPDB1
User: system
Password: OraclePwd123
```

### Oracle XE 21 Full

```bash
podman run -d \
  --name oracle-xe-21-full \
  -p 1524:1521 \
  -e ORACLE_PASSWORD=OraclePwd123 \
  -v oracle-xe-21-full-data:/opt/oracle/oradata:Z \
  gvenzl/oracle-xe:21-full
```

### Oracle Free 23 Slim

```bash
podman run -d \
  --name oracle-free-23-slim \
  -p 1525:1521 \
  -e ORACLE_PASSWORD=OraclePwd123 \
  -v oracle-free-23-slim-data:/opt/oracle/oradata:Z \
  gvenzl/oracle-free:23-slim
```

### Oracle Free 23 Full

```bash
podman run -d \
  --name oracle-free-23-full \
  -p 1526:1521 \
  --cap-add SYS_NICE \
  -e ORACLE_PASSWORD=OraclePwd123 \
  -v oracle-free-23-full-data:/opt/oracle/oradata:Z \
  gvenzl/oracle-free:23-full
```

### Oracle XE Official

```bash
podman run -d \
  --name oracle-xe-official \
  -p 1527:1521 \
  -e ORACLE_PWD=OraclePwd123 \
  -v oracle-xe-official-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/express:21.3.0-xe
```

### Oracle Enterprise 12c

Comando base informado para laboratorio:

```bash
podman run -d \
  --name oracle-12c \
  -p 1528:1521 \
  -p 5508:5500 \
  -e ORACLE_PWD=Oracle123 \
  container-registry.oracle.com/database/enterprise:12.2.0.1
```

No catalogo `repo/oracle/versoes`, essa versao foi organizada como `oracle-12c` usando a porta `1529` para evitar conflito com `oracle-xe-11g`, que ja ocupa `1528`.

### Oracle XE 11g Legacy

```bash
podman run -d \
  --name oracle-xe-11g \
  -p 1528:1521 \
  wnameless/oracle-xe-11g-r2
```

Conexao esperada:

```txt
Host: localhost
Port: 1528
SID/Service: XE
User: system
Password: oracle
```

## 7. Validacao Rapida

Ver versao do banco:

```sql
SELECT banner FROM v$version;
```

Ver usuario atual e container:

```sql
SELECT
  USER AS current_user,
  SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name,
  SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

Criar tabela de teste:

```sql
CREATE TABLE teste_chatgpt (
  id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  nome VARCHAR2(100),
  criado_em DATE DEFAULT SYSDATE
);

INSERT INTO teste_chatgpt (nome) VALUES ('Jefferson Oracle Test');
COMMIT;

SELECT * FROM teste_chatgpt;
```

## 8. Regras Praticas Deste Laboratorio

- Oracle moderno: prefira conexao por `Service Name`.
- Volumes Oracle com Podman: prefira `:Z`.
- Imagens full podem exigir `--cap-add SYS_NICE`.
- Se o nome do container ja existir, remova antes com `podman rm -f nome`.
- Se a porta estiver ocupada, altere o mapeamento no host.
- Se uma nova versao conflitar com uma porta antiga, ajuste a porta do host e mantenha a porta interna Oracle.
- Para comparacao entre versoes, o catalogo principal continua em `repo/oracle/versoes/README.md`.
