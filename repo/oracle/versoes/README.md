# Oracle em Containers - Catálogo de Versões

Este diretório organiza várias formas de executar Oracle em ambiente local usando **Podman**.

O objetivo é oferecer uma visão macro e didática para entender:

- quais imagens Oracle existem para estudo e laboratório;
- como cada versão expõe porta, service name, usuário e volume;
- como subir Oracle com script simples;
- como evoluir de `podman run` para `Containerfile` e `podman compose`;
- quais diferenças práticas existem entre Oracle XE, Oracle Free, imagens oficiais e imagens da comunidade.

A ideia não é dizer que existe uma única forma correta. O laboratório mostra diferentes caminhos para subir Oracle localmente e comparar as abordagens.

## Estrutura Geral

```txt
versoes/
├── README.md
├── clean-volumes.sh
├── free-full-23ai/
│   ├── README.md
│   ├── compose/
│   │   └── compose.yaml
│   ├── containerfile/
│   │   └── Containerfile
│   ├── manual/
│   │   └── comandos.md
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-12c/
│   ├── README.md
│   ├── compose/
│   │   └── compose.yaml
│   ├── containerfile/
│   │   └── Containerfile
│   ├── manual/
│   │   └── comandos.md
│   └── script/
│       ├── down.sh
│       └── up.sh
├── free-lite-23ai/
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-free-23-full/
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-free-23-slim/
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-xe-11g/
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-xe-21-full/
│   └── script/
│       ├── down.sh
│       └── up.sh
├── oracle-xe-21-slim/
│   └── script/
│       ├── down.sh
│       └── up.sh
└── oracle-xe-official/
    └── script/
        ├── down.sh
        └── up.sh
```

## O Que Foi Padronizado

Cada versão possui, no mínimo, uma pasta `script/` com:

- `up.sh`: sobe o container com nome, porta, senha e volume definidos;
- `down.sh`: remove o container;
- `REMOVE_VOLUME=true ./down.sh`: remove também o volume, quando suportado pelo script.

Isso permite testar cada versão de forma isolada sem decorar comandos longos.

## Versão Piloto Completa

A versão `free-full-23ai` recebeu uma organização mais completa para mostrar diferentes formas de trabalhar com containers:

```txt
free-full-23ai/
├── README.md
├── compose/          # exemplo com podman compose
├── containerfile/    # exemplo de build com Containerfile
├── manual/           # comando podman run direto
└── script/           # automação simples com up/down
```

Nela aparecem quatro abordagens didáticas:

1. **Script:** caminho mais simples para executar.
2. **Manual:** comando `podman run` explícito para entender cada parâmetro.
3. **Containerfile:** criação de uma imagem local baseada na imagem oficial.
4. **Compose:** organização declarativa para subir o serviço.

As demais versões foram mantidas com `script/` por enquanto, para não duplicar complexidade antes de validar o padrão completo.

## Catálogo De Versões

| Pasta | Imagem | Porta | Service | Usuário | Senha | Observação |
|---|---|---:|---|---|---|---|
| `free-lite-23ai` | `container-registry.oracle.com/database/free:latest-lite` | `1521` | `FREEPDB1` | `system` | `OraclePwd123` | Oracle Free oficial lite |
| `free-full-23ai` | `container-registry.oracle.com/database/free:latest` | `1522` | `FREEPDB1` | `system` | `OraclePwd123` | Versão piloto completa |
| `oracle-xe-21-slim` | `gvenzl/oracle-xe:21-slim` | `1523` | `XEPDB1` | `system` | `OraclePwd123` | XE 21 slim comunidade |
| `oracle-xe-21-full` | `gvenzl/oracle-xe:21-full` | `1524` | `XEPDB1` | `system` | `OraclePwd123` | XE 21 full comunidade |
| `oracle-free-23-slim` | `gvenzl/oracle-free:23-slim` | `1525` | `FREEPDB1` | `system` | `OraclePwd123` | Free 23 slim comunidade |
| `oracle-free-23-full` | `gvenzl/oracle-free:23-full` | `1526` | `FREEPDB1` | `system` | `OraclePwd123` | Free 23 full comunidade |
| `oracle-xe-official` | `container-registry.oracle.com/database/express:21.3.0-xe` | `1527` | `XEPDB1` | `system` | `OraclePwd123` | XE 21 imagem oficial |
| `oracle-xe-11g` | `wnameless/oracle-xe-11g-r2` | `1528` | `XE` | `system` | `oracle` | XE 11g legado |
| `oracle-12c` | `container-registry.oracle.com/database/enterprise:12.2.0.1` | `1529` | `ORCL` ou service configurado na imagem | `system` | `Oracle123` | Enterprise 12c oficial para laboratorio |

## Sequência Recomendada

Para o curso, a ordem mais útil costuma ser:

1. começar por `free-full-23ai`;
2. usar primeiro o comando manual com `podman run`;
3. validar conexão no CloudBeaver;
4. só depois comparar outras versões;
5. por fim explorar `Containerfile` e `podman compose`.

## Como Usar Uma Versão Com Script

Entre na pasta da versão desejada e execute o `up.sh`:

```bash
cd repo/oracle/versoes/free-lite-23ai/script
./up.sh
```

Ver logs:

```bash
podman logs -f oracle-free-lite-23ai
```

Remover container:

```bash
./down.sh
```

Remover container e volume, quando quiser resetar tudo:

```bash
REMOVE_VOLUME=true ./down.sh
```

## Como Usar A Versão Completa `free-full-23ai`

Leia o guia específico:

```txt
repo/oracle/versoes/free-full-23ai/README.md
```

Subir via script:

```bash
cd repo/oracle/versoes/free-full-23ai/script
./up.sh
```

Subir via compose:

```bash
cd repo/oracle/versoes/free-full-23ai/compose
podman compose up -d
```

Comando manual direto:

```txt
repo/oracle/versoes/free-full-23ai/manual/comandos.md
```

## CloudBeaver E Clientes SQL

Para CloudBeaver local, normalmente use:

```txt
Host: localhost
Port: porta da versão
Connection type: Service Name
Service Name: FREEPDB1 ou XEPDB1
Database: FREEPDB1
User: system
Password: senha da versão
```

Para CloudBeaver em container, normalmente use:

```txt
Host: host.containers.internal
Port: porta da versão
Connection type: Service Name
Service Name: FREEPDB1 ou XEPDB1
Database: FREEPDB1
User: system
Password: senha da versão
```

## Observações Técnicas

- Oracle moderno usa arquitetura multitenant; por isso, para laboratório, priorize conexão via **Service Name** da PDB.
- Oracle Free geralmente usa `FREEPDB1`.
- Oracle XE 21 geralmente usa `XEPDB1`.
- Oracle XE 11g legado usa `XE`.
- O volume com sufixo `:Z` ajuda o Podman a ajustar label SELinux/MCS e evita `Permission denied` em `/opt/oracle/oradata`.
- Algumas imagens full precisam de `--cap-add SYS_NICE` para evitar erro de prioridade de processo durante o startup.
- Se uma porta estiver ocupada, altere `HOST_PORT` antes de executar o script ou ajuste o mapeamento no compose.
- Se um container com o mesmo nome já existir, remova com `podman rm -f nome-do-container`.

## Limpeza Geral De Volumes

O arquivo `clean-volumes.sh` remove os volumes das versões de laboratório.

Use com cuidado, pois isso apaga os dados persistidos dos bancos:

```bash
cd repo/oracle/versoes
./clean-volumes.sh
```

## Vamos testar nosso ORACLE
```bash
-- 1) Ver versão do Oracle
SELECT banner FROM v$version;

-- 2) Ver usuário atual e container/PDB
SELECT 
    USER AS current_user,
    SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name,
    SYS_CONTEXT('USERENV', 'CON_NAME') AS pdb_name
FROM dual;

-- 3) Criar tabela + inserir + consultar
CREATE TABLE teste_chatgpt (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100),
    criado_em DATE DEFAULT SYSDATE
);

INSERT INTO teste_chatgpt (nome) VALUES ('Jefferson Oracle Test');

COMMIT;

**SELECT * FROM teste_chatgpt;
```
