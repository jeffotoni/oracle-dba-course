# Podman no Curso

Este diretório concentra o uso de Podman no curso e organiza os exemplos reais do workspace.

O objetivo aqui nao e apenas mostrar comandos soltos. A ideia e documentar como usar Podman para:

- subir containers simples;
- buildar imagens locais;
- trabalhar com volumes, portas e logs;
- executar exemplos em Go;
- subir multiplas versoes Oracle para laboratorio;
- usar `podman compose` quando fizer sentido.

## O Que Existe Neste Workspace

| Area | Objetivo | Caminho |
| :--- | :--- | :--- |
| Guia principal de Podman | Conceitos, instalacao, comandos base e fluxo geral | `podman/README.md` |
| Exemplos Go com Podman | Subir APIs Go, buildar imagem e testar HTTP | `podman/go-exemplos.md` |
| Exemplos Oracle com Podman | Subir Oracle por `podman run`, `Containerfile` e `podman compose` | `podman/oracle-exemplos.md` |
| CRUD Go + Oracle | API HTTP em Go conectando no Oracle | `repo/go.oracle/v1` |
| Catalogo Oracle | Varias versoes Oracle para laboratorio | `repo/oracle/versoes` |
| ORDS com Podman | Expor Oracle via REST em `localhost:8181` | `repo/oracle/ords` |

## Visao Geral

Podman e uma engine de containers compativel com OCI. No laboratorio ele entra como alternativa pratica ao Docker, com boa aderencia a comandos conhecidos e um fluxo simples para desenvolvimento local.

Pontos relevantes para este curso:

- funciona bem para desenvolvimento local;
- tem boa compatibilidade com a sintaxe do Docker;
- permite trabalhar com `podman run`, `podman build`, `podman logs`, `podman exec` e `podman compose`;
- no macOS usa `podman machine`;
- em Linux, o sufixo `:Z` em volumes pode ser importante quando houver SELinux.

## Comandos Base

Ver versao:

```bash
podman --version
```

Ver containers ativos:

```bash
podman ps
```

Ver todos os containers:

```bash
podman ps -a
```

Ver imagens:

```bash
podman images
```

Ver volumes:

```bash
podman volume ls
```

Ver logs:

```bash
podman logs -f nome-do-container
```

Entrar no container:

```bash
podman exec -it nome-do-container bash
```

Parar container:

```bash
podman stop nome-do-container
```

Remover container:

```bash
podman rm -f nome-do-container
```

Remover volume:

```bash
podman volume rm nome-do-volume
```

## Instalacao Rapida

### macOS

```bash
brew install podman
podman machine init
podman machine start
```

Teste:

```bash
podman ps
podman run hello-world
```

### Linux

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install podman -y
```

Fedora:

```bash
sudo dnf install podman -y
```

Teste:

```bash
podman ps
```

## `podman run`, `podman build` e `podman compose`

No curso, essas tres formas aparecem com papeis diferentes:

| Forma | Quando usar | Melhor para |
| :--- | :--- | :--- |
| `podman run` | Rodar rapido e enxergar todos os parametros | Aula, laboratorio, entendimento do container |
| `podman build` | Criar imagem local a partir de `Containerfile` | Mostrar empacotamento da aplicacao |
| `podman compose` | Declarar servicos com build, porta, volume e ambiente | Ambientes repetiveis e organizados |

## `Containerfile` vs `Dockerfile`

- Em Docker, o nome mais comum e `Dockerfile`.
- Em Podman e Buildah, `Containerfile` e um nome natural e bem aceito.
- Podman aceita os dois.
- Neste workspace, os exemplos mais didaticos usam `Containerfile`.

## Volumes e SELinux

Quando o host usa SELinux, monte volumes com `:Z`:

```bash
podman run -d \
  -v meu-volume:/dados:Z \
  imagem
```

Isso ajuda a evitar erros como:

```txt
Permission denied
```

## `podman compose` no macOS

Em alguns ambientes, `podman compose` usa um provider externo. Exemplo:

```txt
Executing external compose provider "/opt/homebrew/bin/docker-compose"
```

Isso nao impede o uso, mas traz duas implicacoes praticas:

- se o volume ja existir e nao tiver sido criado pelo compose, pode ser necessario marcar como `external: true`;
- se um container com o mesmo nome ja existir, ele deve ser removido antes:

```bash
podman rm -f nome-do-container
```

## Fluxos Reais Deste Workspace

### Go

Exemplos documentados em [go-exemplos.md](go-exemplos.md).

Conteudo principal:

- subir API Go com `podman run`;
- buildar imagem local com `podman build`;
- testar endpoints com `curl`;
- conectar Go com Oracle no exemplo `repo/go.oracle/v1`.

### Oracle

Exemplos documentados em [oracle-exemplos.md](oracle-exemplos.md).

Conteudo principal:

- subir varias versoes Oracle com `podman run`;
- usar `Containerfile` na versao mais completa;
- usar `podman compose` no `free-full-23ai`;
- incluir o Oracle Enterprise 12c como exemplo adicional de imagem oficial;
- subir `ORDS` em modo standalone para expor REST sobre o Oracle local;
- entender portas, volumes, services e credenciais.

## Estrategia Didatica Usada Aqui

Para Oracle, o laboratorio foi organizado em camadas:

1. Primeiro, entender o `podman run` puro.
2. Depois, entender o `Containerfile`.
3. Por fim, entender `podman compose`.

Isso torna o aprendizado progressivo:

- primeiro fica claro o container;
- depois entende a imagem;
- depois entende a orquestracao basica.

No catalogo `repo/oracle/versoes`, a versao mais completa hoje e:

```txt
repo/oracle/versoes/free-full-23ai
```

Ela foi usada como modelo para:

- `podman run`;
- `Containerfile`;
- `podman compose`.

As outras versoes Oracle continuam uteis para comparacao, mas foram mantidas com foco no fluxo simples de laboratorio.

Uma versao adicional importante no catalogo agora e:

```txt
repo/oracle/versoes/oracle-12c
```

Ela ajuda a comparar:

- Oracle Free moderno versus Oracle Enterprise 12c;
- service name e comportamento de imagens oficiais diferentes;
- uso de porta SQL adicional e porta web/admin (`5500`);
- diferenca entre laboratorio com Free e laboratorio com linha Enterprise.

## Proximos

Depois deste guia principal, a leitura recomendada e:

1. [go-exemplos.md](go-exemplos.md)
2. [oracle-exemplos.md](oracle-exemplos.md)
3. [repo/oracle/versoes/README.md](../repo/oracle/versoes/README.md)
4. [repo/go.oracle/v1/README.md](../repo/go.oracle/v1/README.md)
