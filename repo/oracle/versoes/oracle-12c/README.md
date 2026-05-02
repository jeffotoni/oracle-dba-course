# Oracle 12c Enterprise

Ambiente de laboratorio para subir o **Oracle Enterprise 12c** com Podman.

Esta versao usa a imagem oficial:

```txt
container-registry.oracle.com/database/enterprise:12.2.0.1
```

## Estrutura

```txt
oracle-12c/
├── README.md
├── compose/
│   └── compose.yaml
├── containerfile/
│   └── Containerfile
├── manual/
│   └── comandos.md
└── script/
    ├── down.sh
    └── up.sh
```

## Configuracao Padrao

| Item | Valor |
| :--- | :--- |
| Container | `oracle-12c` |
| Imagem oficial | `container-registry.oracle.com/database/enterprise:12.2.0.1` |
| Imagem local buildada | `oracle-12c:12c` |
| Porta host SQL | `1529` |
| Porta container SQL | `1521` |
| Porta host web/admin | `5508` |
| Porta container web/admin | `5500` |
| Volume | `oracle-12c-data` |
| Senha | `Oracle123` |

## Observacoes

- O comando base enviado para laboratorio usava `1528:1521`, mas no catalogo esta versao foi ajustada para `1529:1521`.
- O motivo e simples: `1528` ja esta ocupada pela versao `oracle-xe-11g`.
- A imagem 12c pode expor service ou SID de forma diferente conforme o bootstrap da imagem. Em laboratorio, valide no primeiro acesso qual nome a instancia registrou.

## Credenciais Para DBeaver

- **Host:** `localhost`
- **Port:** `1529`
- **User:** `system`
- **Password:** `Oracle123`

No primeiro acesso, valide se a conexao deve usar:

- **SID:** `ORCL`
- ou **Service Name:** o nome registrado pela imagem

## Subir Com Script

```bash
cd repo/oracle/versoes/oracle-12c/script
./up.sh
```

Ver logs:

```bash
podman logs -f oracle-12c
```

Derrubar sem apagar dados:

```bash
cd repo/oracle/versoes/oracle-12c/script
./down.sh
```

Derrubar apagando o volume:

```bash
cd repo/oracle/versoes/oracle-12c/script
REMOVE_VOLUME=true ./down.sh
```

## Subir Manualmente Com `podman run`

O arquivo `manual/comandos.md` mantem o comando manual principal.

```bash
podman run -d \
  --name oracle-12c \
  -p 1529:1521 \
  -p 5508:5500 \
  -e ORACLE_PWD=Oracle123 \
  -v oracle-12c-data:/opt/oracle/oradata:Z \
  container-registry.oracle.com/database/enterprise:12.2.0.1
```

## Build Com Containerfile

```bash
cd repo/oracle/versoes/oracle-12c
podman build -t oracle-12c:12c -f containerfile/Containerfile .
```

Rodar a imagem local criada:

```bash
podman run -d \
  --name oracle-12c \
  -p 1529:1521 \
  -p 5508:5500 \
  -e ORACLE_PWD=Oracle123 \
  -v oracle-12c-data:/opt/oracle/oradata:Z \
  oracle-12c:12c
```

## Subir Com Podman Compose

```bash
cd repo/oracle/versoes/oracle-12c/compose
podman compose up -d
```

Ver status:

```bash
podman compose ps
```

Ver logs:

```bash
podman compose logs -f oracle-12c
```

Derrubar:

```bash
podman compose down
```

Derrubar apagando volume:

```bash
podman compose down -v
```
