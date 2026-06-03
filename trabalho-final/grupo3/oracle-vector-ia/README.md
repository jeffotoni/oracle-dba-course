# Oracle AI Assistant — Busca Semântica com Vetores
Camilla - Cleo - Nicole - Pablo

Assistente de perguntas e respostas com busca semântica usando **Oracle Database 23c** (suporte nativo a vetores) e **sentence-transformers**.

## Como funciona

1. Documentos sobre governança de dados são armazenados no banco Oracle com a coluna `embedding` do tipo `VECTOR(384, FLOAT32)`.
2. O script `gerar_embedding.py` gera embeddings para cada documento usando o modelo `all-MiniLM-L6-v2` e os salva no banco.
3. O script `buscar.py` recebe perguntas do usuário, gera o embedding da pergunta e usa `VECTOR_DISTANCE` (distância de cosseno) para encontrar os documentos mais relevantes.

## Pré-requisitos

- Oracle Database 23c Free (`localhost:1526/FREEPDB1`)
- Python 3.x
- Dependências Python:

```bash
pip install oracledb sentence-transformers
```

## Configuração do banco

Execute o script SQL para criar a tabela e inserir os documentos:

```bash
sqlplus camilla/Admin@123@localhost:1526/FREEPDB1 @scritp.sql
```

## Uso

**1. Gerar os embeddings** (executar uma vez após inserir documentos):

```bash
python gerar_embedding.py
```

**2. Iniciar o assistente:**

```bash
python buscar.py
```

Exemplo de interação:

```
Oi, como posso ajudar? O que é LGPD?

Resposta do Assistente:
-------------------
Encontrei um conteúdo relacionado: LGPD

A LGPD é a Lei Geral de Proteção de Dados...

Nível de similaridade: 0.91
```

Digite `sair` para encerrar.

## Estrutura

```
oracle/
├── scritp.sql          # Criação da tabela e carga dos documentos
├── gerar_embedding.py  # Geração e persistência dos embeddings
└── buscar.py           # Assistente interativo de busca semântica
```

## Base de conhecimento

Os documentos cobrem os seguintes temas de gestão de dados:

- Governança de Dados
- Qualidade de Dados
- Master Data Management (MDM)
- Data Warehouse
- LGPD
- ETL
- Metadados
- Catálogo de Dados
