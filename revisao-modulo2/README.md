# Revisão do Módulo 2

> Resumo organizado do módulo 2: segurança, controle de acesso, auditoria e carga de dados em volume no Oracle.

## Ideia central do módulo

O módulo 2 junta dois temas que andam juntos no ambiente real:

1. controlar quem entra e o que pode fazer;
2. controlar como grandes volumes de dados entram, saem ou são movimentados.

Em outras palavras:

```txt
Segurança = identidade + permissão + rastreabilidade
Carga em volume = entrada e movimentação controlada de dados
```

## O que precisa ficar claro

- autenticação não é a mesma coisa que autorização;
- usuário não é apenas login, também se relaciona com schema e posse de objetos;
- privilégios amplos demais aumentam risco;
- roles ajudam a organizar permissões;
- perfis ajudam a padronizar política;
- auditoria ajuda a provar o que aconteceu;
- SQL*Loader, tabela externa e Data Pump não são a mesma coisa.

## 1. Segurança no Oracle

Segurança em Oracle não deve ser reduzida a senha. Ela envolve:

- identidade;
- acesso;
- permissão;
- segregação de funções;
- rastreabilidade;
- governança.

### Regra prática

```txt
Não basta saber quem entrou.
É preciso saber o que pode fazer e o que ficou registrado.
```

## 2. Autenticação x autorização

### Autenticação

Responde à pergunta:

```txt
Quem está tentando acessar?
```

### Autorização

Responde à pergunta:

```txt
O que essa identidade pode fazer?
```

### Diferença curta

```txt
Autenticação = validar identidade
Autorização = definir permissões
```

## 3. Usuário e schema

No Oracle, quando um usuário é criado, normalmente existe um schema associado ao mesmo nome.

Isso é importante porque o usuário não representa apenas acesso. Ele também se relaciona com:

- dono de objetos;
- organização lógica;
- separação entre aplicação, leitura, carga e administração.

### Regra prática

```txt
Usuário = identidade
Schema = espaço lógico dos objetos
```

## 4. Perfis

Perfis existem para aplicar regras de forma padronizada.

Eles podem controlar:

- tentativas de login;
- bloqueio;
- expiração de senha;
- reutilização;
- limite de sessão;
- tempo ocioso.

### Ideia central

Perfil ajuda a tirar o ambiente do improviso e levar para um padrão administrativo.

## 5. Privilégios e roles

### Privilégios de sistema

Controlam ações amplas no ambiente, como:

- criar sessão;
- criar tabela;
- criar usuário;
- criar procedure.

### Privilégios de objeto

Controlam ações sobre objetos específicos, como:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `EXECUTE`

### Roles

Roles agrupam privilégios. Isso simplifica:

- concessão;
- revisão;
- revogação;
- padronização.

### Regra prática

```txt
Privilégio de sistema = poder amplo
Privilégio de objeto = poder específico
Role = pacote organizado de permissões
```

## 6. Menor privilégio e segregação

O módulo 2 faz mais sentido quando fecha nesta lógica:

- conta de aplicação;
- conta de leitura;
- conta de carga;
- conta administrativa.

### Regra prática

```txt
Menos privilégio direto
Mais role coerente
Mais rastreabilidade
```

## 7. Auditoria e rastreabilidade

Auditoria registra ações relevantes no banco.

Rastreabilidade permite responder:

- quem fez;
- quando fez;
- em qual objeto;
- com qual resultado.

### O que auditar costuma fazer sentido

- logon;
- acesso a objetos sensíveis;
- operações administrativas;
- concessão de privilégios;
- alterações importantes.

### Regra prática

```txt
Segurança sem rastreabilidade é incompleta
```

## 8. Carga de dados em volume

Carga em volume é a entrada, leitura, importação ou movimentação de grande quantidade de dados de forma planejada.

Ela aparece em cenários como:

- migração;
- carga inicial;
- integração entre sistemas;
- recebimento de arquivo externo;
- refresh de ambiente;
- cópia de schema;
- importação lógica.

## 9. Ferramentas de carga e movimentação

## 9.1. SQL*Loader

Ferramenta clássica do Oracle para carregar arquivo externo estruturado em tabela Oracle.

### Quando pensar em SQL*Loader

- CSV ou TXT bem definido;
- carga repetitiva;
- arquivo com layout conhecido;
- rotina operacional.

## 9.2. Tabela externa

Permite ler arquivo como tabela sem carregar de imediato para tabela interna.

### Quando pensar em tabela externa

- validar arquivo antes da carga;
- consultar com SQL;
- inspecionar conteúdo;
- usar como etapa intermediária em ETL.

## 9.3. Data Pump

Ferramenta de exportação e importação lógica do ecossistema Oracle.

### Quando pensar em Data Pump

- exportar schema;
- importar schema;
- copiar objetos e dados;
- migrar ambiente Oracle para Oracle;
- fazer dump lógico.

## 9.4. Regra prática de escolha

```txt
Arquivo estruturado para tabela = SQL*Loader
Ler arquivo com SQL = tabela externa
Mover objetos e dados Oracle = Data Pump
```

## 10. Segurança e carga andam juntas

Carga de dados não é assunto separado de segurança.

Toda carga relevante deveria levantar perguntas como:

- quem pode executar;
- em qual schema entra;
- quais privilégios a rotina precisa;
- como registrar a operação;
- como validar origem e erro;
- como reduzir impacto operacional.

## 11. Queries essenciais de revisão

### Ver usuários

```sql
SELECT username,
       account_status,
       profile
FROM dba_users
ORDER BY username;
```

### Ver roles

```sql
SELECT role
FROM dba_roles
ORDER BY role;
```

### Ver privilégios de sistema

```sql
SELECT grantee,
       privilege
FROM dba_sys_privs
ORDER BY grantee, privilege;
```

### Ver privilégios de objeto

```sql
SELECT grantee,
       owner,
       table_name,
       privilege
FROM dba_tab_privs
ORDER BY grantee, owner, table_name, privilege;
```

### Ver roles concedidas

```sql
SELECT grantee,
       granted_role
FROM dba_role_privs
ORDER BY grantee, granted_role;
```

### Ver trilha de auditoria

```sql
SELECT event_timestamp,
       dbusername,
       action_name,
       object_schema,
       object_name,
       return_code
FROM unified_audit_trail
ORDER BY event_timestamp DESC
FETCH FIRST 30 ROWS ONLY;
```

### Ver diretórios lógicos

```sql
SELECT directory_name,
       directory_path
FROM dba_directories
ORDER BY directory_name;
```

## 12. Comandos que valem aparecer na revisão

### Criar perfil

```sql
CREATE PROFILE prof_lab_m2 LIMIT
  SESSIONS_PER_USER 3
  FAILED_LOGIN_ATTEMPTS 5;
```

### Criar usuário

```sql
CREATE USER app_owner IDENTIFIED BY AppOwner123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP;
```

### Criar role

```sql
CREATE ROLE role_leitura_m2;
```

### Conceder privilégios

```sql
GRANT CREATE SESSION TO role_leitura_m2;
GRANT role_leitura_m2 TO analista;
GRANT SELECT ON app_owner.produtos TO role_leitura_m2;
```

### Criar política de auditoria

```sql
CREATE AUDIT POLICY pol_logon_m2 ACTIONS LOGON;
AUDIT POLICY pol_logon_m2;
```

### SQL*Loader

```bash
sqlldr app_owner/AppOwner123@//localhost:1521/FREEPDB1 \
  control=/opt/oracle/labdata/produtos.ctl
```

### Data Pump

```bash
expdp system/Senha123@//localhost:1521/FREEPDB1 \
  DIRECTORY=dpump_dir \
  DUMPFILE=app_owner_m2.dmp \
  SCHEMAS=APP_OWNER
```

## 13. Resultado esperado

Ao final da revisão, o que precisa ficar claro é:

- segurança Oracle é controle de identidade, acesso e governança;
- usuário, schema, privilégio, role e perfil se conectam;
- auditoria existe para registrar e provar ações;
- carga em volume precisa de critério e ferramenta correta;
- SQL*Loader, tabela externa e Data Pump atendem cenários diferentes.

## Scripts originais do módulo

- `modulo2-material/02-teoria-modulo2.md`
  - base conceitual do módulo.
- `modulo2-material/02-pratica-modulo2.md`
  - roteiro prático completo com usuários, roles, auditoria e carga.
- `modulo2-material/modulo2-seguranca-carga/scripts/03-sqlldr.sh`
  - apoio para carga com `SQL*Loader`.
- `modulo2-material/modulo2-seguranca-carga/scripts/04-expdp.sh`
  - apoio para exportação lógica com `Data Pump`.
- `modulo2-material/modulo2-seguranca-carga/scripts/05-impdp.sh`
  - apoio para importação lógica com `Data Pump`.
