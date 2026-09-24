# Aula 3 - Módulo 2: Segurança e carga de dados no Oracle

Esta aula conecta segurança, controle de acesso, auditoria e movimentação de dados em volume. A linha de raciocínio é sair da identidade e chegar a uma operação de carga rastreável.

## O que será compreendido

Ao terminar a aula, deve ser possível:

- diferenciar autenticação de autorização;
- explicar a relação entre usuário e schema;
- diferenciar perfil, privilégio e role;
- aplicar o princípio do menor privilégio;
- separar conta de aplicação, leitura, carga e administração;
- entender por que a auditoria completa a segurança;
- escolher entre `SQL*Loader`, tabela externa e Data Pump;
- reconhecer quando usar `sqlplus`, `sqlldr`, `expdp` e `impdp`;
- executar uma carga e validar o resultado por SQL;
- explicar quem executou uma ação e como ela foi registrada.

## Resumo da aula

### Teoria principal

- autenticação, autorização e rastreabilidade;
- usuário, schema, perfil, privilégio e role;
- princípio do menor privilégio;
- separação entre aplicação, leitura, carga e administração;
- auditoria e trilha de ações;
- carga de dados em volume;
- diferença entre `SQL*Loader`, tabela externa, `expdp`, `impdp` e `sqlplus`.

### Prática principal

1. Subir o Oracle com Podman.
2. Validar a conexão e os binários nativos.
3. Criar perfil, usuários e roles.
4. Criar a tabela `APP_OWNER.PRODUTOS`.
5. Testar leitura e carga com usuários diferentes.
6. Criar auditoria e consultar evidências.
7. Carregar um CSV com `SQL*Loader`.
8. Consultar o mesmo arquivo usando tabela externa.
9. Exportar e importar um schema com Data Pump.
10. Validar e limpar o laboratório.

### Ferramentas utilizadas

```text
IDE                  -> SQL e consultas
Podman               -> ambiente Oracle
sqlplus              -> cliente nativo e administração pontual
sqlldr               -> carga de CSV ou TXT
expdp / impdp        -> exportação e importação lógica
```

### Resultado esperado

```text
identidade
  -> permissão
      -> objeto
          -> ação
              -> auditoria
                  -> carga validada
```

O material está organizado em dois arquivos:

```text
novos-modulos-enxutos/aula-3-modulo2/
├── README.md    -> teoria, orientação e comandos curtos
└── pratica.md   -> execução completa do laboratório
```

## Fluxo mental da aula

```text
usuário
  -> autenticação
      -> perfil
          -> role
              -> privilégio
                  -> schema e objeto
                      -> auditoria
                          -> carga ou movimentação de dados
```

A pergunta central é:

```text
Quem pode fazer o quê, em qual objeto, usando qual ferramenta, e como comprovar o resultado?
```

## 1. Segurança não é somente senha

Segurança no Oracle envolve camadas diferentes:

| Camada | Pergunta |
| :--- | :--- |
| Autenticação | Quem está tentando entrar? |
| Autorização | O que essa identidade pode fazer? |
| Perfil | Quais limites e políticas se aplicam? |
| Privilégio | Qual ação foi liberada? |
| Role | Como os privilégios foram agrupados? |
| Auditoria | O que aconteceu, quando e por quem? |

```text
Autenticação = validar identidade
Autorização = liberar ações
Auditoria = registrar evidências
```

Uma senha válida não significa que o usuário pode consultar ou alterar qualquer tabela.

## 2. Usuário e schema

No Oracle, um usuário representa a identidade que autentica. O schema representa o conjunto de objetos pertencentes a esse usuário.

```text
APP_OWNER
└── schema APP_OWNER
    ├── PRODUTOS
    ├── PRODUTOS_CARGA
    └── EXT_PRODUTOS
```

Por isso, uma tabela criada por `APP_OWNER` normalmente é referenciada como:

```sql
APP_OWNER.PRODUTOS
```

Consultas rápidas para entender a sessão:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

## 3. Perfil, privilégio e role

### Perfil

Um perfil concentra limites e políticas de senha ou sessão:

```sql
SELECT username,
       profile,
       account_status
FROM dba_users
ORDER BY username;
```

### Privilégio

Privilégio é uma permissão específica.

```text
CREATE SESSION -> conectar
CREATE TABLE   -> criar tabela no próprio schema
SELECT         -> consultar um objeto
INSERT         -> inserir em um objeto
```

Privilégios de sistema têm alcance amplo. Privilégios de objeto atuam sobre uma tabela, view, procedure ou outro objeto específico.

### Role

Role é um pacote de privilégios que pode ser concedido a vários usuários.

```text
role_leitura_m2
  -> CREATE SESSION
  -> SELECT em APP_OWNER.PRODUTOS
```

Roles facilitam revisão, concessão e revogação de acesso.

## 4. Menor privilégio e segregação

O laboratório separa responsabilidades:

| Conta | Responsabilidade |
| :--- | :--- |
| `APP_OWNER` | Dono da tabela e da aplicação |
| `ANALISTA` | Consulta controlada |
| `OPERADOR_CARGA` | Carga de dados |
| `APP_CLONE` | Destino de uma cópia lógica |
| `SYSTEM` ou `SYSDBA` | Administração do ambiente |

O objetivo não é criar muitos usuários sem motivo. É demonstrar que cada operação pode receber somente o acesso necessário.

## 5. Auditoria e rastreabilidade

Auditoria registra ações relevantes e permite responder:

```text
Quem executou?
Quando executou?
Em qual objeto?
Qual ação ocorreu?
Houve erro ou sucesso?
```

A trilha unificada pode ser consultada com:

```sql
SELECT event_timestamp,
       dbusername,
       action_name,
       object_schema,
       object_name,
       return_code
FROM unified_audit_trail
ORDER BY event_timestamp DESC
FETCH FIRST 20 ROWS ONLY;
```

Auditoria não substitui privilégio. Ela registra a ação; o controle de acesso decide se a ação pode ocorrer.

## 6. Carga de dados em volume

Carga em volume aparece em migrações, integrações, cargas iniciais, refresh de ambientes, recebimento de arquivos e cópia de schemas.

Antes de carregar dados, confirme:

- origem do arquivo ou dump;
- usuário executor;
- schema de destino;
- tabela de destino;
- privilégios necessários;
- logs e validações;
- estratégia de rollback ou limpeza.

## 7. Ferramentas Oracle utilizadas

| Ferramenta | Função principal | Onde será executada |
| :--- | :--- | :--- |
| `sqlplus` | SQL e administração por linha de comando | Container, quando necessário |
| `sqlldr` | Carregar CSV ou TXT em tabela | Container Oracle |
| `expdp` | Exportar dados e metadados Oracle | Container Oracle |
| `impdp` | Importar dump lógico Oracle | Container Oracle |
| Tabela externa | Ler arquivo usando SQL | Banco, com arquivo no container |

```text
Arquivo externo para tabela definitiva -> SQL*Loader
Arquivo externo para validação com SQL -> tabela externa
Oracle para Oracle                 -> expdp / impdp
Administração e consultas           -> IDE ou sqlplus
```

O cliente gráfico continua sendo adequado para SQL e consultas. Os binários nativos do Oracle são usados dentro do container porque dependem da instalação Oracle e dos diretórios internos do ambiente.

## 8. Comandos básicos do ambiente

Subir a versão usada na prática:

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

Validar o container:

```bash
podman ps
podman logs --tail 30 oracle-free-full-23ai
```

Entrar no container e verificar os binários:

```bash
podman exec -it oracle-free-full-23ai bash
command -v sqlplus
command -v sqlldr
command -v expdp
command -v impdp
```

Conexão principal na IDE:

```text
Host: localhost
Port: 1522
Service Name: FREEPDB1
User: SYSTEM
Password: OraclePwd123
Role: Normal
```

Validação inicial:

```sql
SELECT USER AS current_user,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema,
       SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;
```

## 9. Como executar esta aula

O [laboratório prático](./pratica.md) contém os comandos na ordem executável:

1. subir e validar o Oracle;
2. criar perfis, usuários e roles;
3. criar a tabela e testar acessos;
4. habilitar auditoria e gerar evidências;
5. carregar um CSV com SQL*Loader;
6. consultar o mesmo arquivo como tabela externa;
7. exportar e importar um schema com Data Pump;
8. validar e limpar o laboratório.

## Resultado esperado

Ao finalizar, a sequência deve estar clara:

```text
identidade
  -> acesso
      -> objeto
          -> ação
              -> evidência
                  -> carga validada
```

Consulte também o [material completo do Módulo 2](../../modulo2-material/02-teoria-modulo2.md), a [prática original](../../modulo2-material/02-pratica-modulo2.md) e a [revisão atual](../../aula3-revisao-modulo2/README.md).
