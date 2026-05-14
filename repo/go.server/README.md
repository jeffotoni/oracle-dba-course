# Go Server

> API HTTP mínima em Go para demonstração de rota, método, JSON, build local e execução com `Podman`.

## Objetivo

Este projeto existe para demonstrar o ciclo mais simples possível de uma API em Go:

- escrever uma rota;
- subir a aplicação;
- enviar requisição HTTP;
- receber JSON de volta;
- compilar;
- empacotar em container.

## Estrutura do projeto

- `repo/go.server/main.go`
  - servidor HTTP simples;
- `repo/go.server/go.mod`
  - módulo Go;
- `repo/go.server/Containerfile`
  - imagem simples com `go run`;
- `repo/go.server/Containerfile.build`
  - imagem com binário compilado;
- `repo/go.server/Containerfile.alpine`
  - imagem final baseada em `alpine`;
- `repo/go.server/Containerfile.distroless`
  - imagem final `distroless`;
- `repo/go.server/Containerfile.scratch`
  - imagem final mínima `scratch`.

## O que a aplicação faz

A aplicação expõe uma única rota:

```txt
POST /api/v1/user
```

### Comportamento

- aceita apenas `POST`;
- lê o corpo da requisição;
- registra no log o JSON recebido;
- responde com o mesmo JSON;
- retorna `405` se o método não for permitido.

## Quick start

## 1. Rodar localmente com Go

```bash
cd repo/go.server
go run main.go
```

Saída esperada:

```txt
server running on :8080
```

## 2. Compilar localmente

```bash
cd repo/go.server
go build -o go-server .
```

## 3. Executar binário compilado

```bash
cd repo/go.server
./go-server
```

## 4. Testar a API

### GET na rota principal

Esse teste é útil para mostrar que a rota existe, mas o método está errado.

```bash
curl -i http://localhost:8080/api/v1/user
```

Resposta esperada:

- `405 Method Not Allowed`

### GET em rota inexistente

```bash
curl -i http://localhost:8080/api/v1/not-found
```

Resposta esperada:

- `404 Not Found`

### POST com JSON simples

```bash
curl -i \
  -X POST http://localhost:8080/api/v1/user \
  -H 'Content-Type: application/json' \
  -d '{"name":"Jefferson","email":"jeff@email.com"}'
```

### POST com outro JSON

```bash
curl -i \
  -X POST http://localhost:8080/api/v1/user \
  -H 'Content-Type: application/json' \
  -d '{"name":"Maria","role":"admin","active":true}'
```

### POST com payload mais próximo de cadastro

```bash
curl -i \
  -X POST http://localhost:8080/api/v1/user \
  -H 'Content-Type: application/json' \
  -d '{"id":10,"name":"Arthur","email":"arthur@email.com","city":"Sao Paulo"}'
```

## Outras ferramentas para teste

### Linha de comando

- `curl`
- `HTTPie`
- `wget`

### Interface gráfica

- `Insomnia`
- `Postman`
- `Bruno`

## Rodando com Podman

## 1. Imagem simples com `go run`

Arquivo:

- `repo/go.server/Containerfile`

### Build

```bash
cd repo/go.server
podman build -t go-server:dev -f Containerfile .
```

### Run

```bash
podman run --rm -p 8080:8080 --name go-server go-server:dev
```

### Quando usar

- demonstração rápida;
- laboratório;
- ambiente didático.

## 2. Imagem com binário compilado

Arquivo:

- `repo/go.server/Containerfile.build`

### Build

```bash
cd repo/go.server
podman build -t go-server:build -f Containerfile.build .
```

### Run

```bash
podman run --rm -p 8080:8080 --name go-server-build go-server:build
```

### Quando usar

- mostrar diferença entre `go run` e binário compilado;
- laboratório de build simples.

## 3. Imagem final em Alpine

Arquivo:

- `repo/go.server/Containerfile.alpine`

### Build

```bash
cd repo/go.server
podman build -t go-server:alpine -f Containerfile.alpine .
```

### Run

```bash
podman run --rm -p 8080:8080 --name go-server-alpine go-server:alpine
```

### Quando usar

- mostrar imagem menor;
- introduzir multi-stage build;
- manter ambiente ainda fácil de entender.

## 4. Imagem final Distroless

Arquivo:

- `repo/go.server/Containerfile.distroless`

### Build

```bash
cd repo/go.server
podman build -t go-server:distroless -f Containerfile.distroless .
```

### Run

```bash
podman run --rm -p 8080:8080 --name go-server-distroless go-server:distroless
```

### Quando usar

- mostrar imagem mais enxuta;
- falar de redução de superfície do container;
- discutir execução sem shell.

## 5. Imagem Scratch

Arquivo:

- `repo/go.server/Containerfile.scratch`

### Build

```bash
cd repo/go.server
podman build -t go-server:scratch -f Containerfile.scratch .
```

### Run

```bash
podman run --rm -p 8080:8080 --name go-server-scratch go-server:scratch
```

### Quando usar

- mostrar imagem mínima;
- falar de binário estático;
- discutir limitações de debugging.

## Sugestão para a aula

Se a aula for curta, a melhor sequência é:

1. `go run main.go`
2. testar com `curl`
3. `go build -o go-server .`
4. `podman build -t go-server:dev -f Containerfile .`
5. `podman run --rm -p 8080:8080 --name go-server go-server:dev`

## O que explicar ao vivo

### Método HTTP

Esta API aceita apenas `POST` na rota principal.

### Corpo da requisição

O servidor lê o JSON enviado no body.

### Resposta

O mesmo conteúdo recebido é devolvido para facilitar a visualização do fluxo.

### Logs

O log no terminal mostra o que a aplicação recebeu.

## Relação com o restante do curso

Este projeto ajuda a criar a ponte entre:

- aplicação;
- HTTP;
- JSON;
- cliente de API;
- container;
- Oracle exposto por `ORDS`.

### Regra prática

```txt
Go = API construída na aplicação
ORDS = API exposta pelo Oracle
```

## Encerramento

Este projeto não tenta ser um backend completo. Ele existe para ser pequeno o suficiente para explicar:

- rota;
- método;
- request body;
- response body;
- build;
- container.

Essa simplicidade ajuda a preparar o terreno para integração com Oracle e para a comparação com `ORDS`.
