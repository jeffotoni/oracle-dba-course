# Configuração ORDS para Dashboard Simples de Estatísticas Oracle

Este arquivo consolida os comandos necessários para usar o **ORDS como camada de API** do projeto de monitoramento Oracle, criando o usuário `MONITOR_APP`, concedendo permissões de leitura nas views administrativas e publicando endpoints REST para o dashboard.

A proposta da solução é:

```text
Oracle Free 23ai
    ↓
Views administrativas do Oracle
    ↓
ORDS REST Services
    ↓
Dashboard HTML/CSS/JS
    ↓
Atualização automática via fetch()
```

---

## 1. Premissas do ambiente

Este roteiro considera o ambiente que já foi definido no projeto:

```text
Banco: Oracle Free Full 23ai
PDB / Service Name: FREEPDB1
Host Windows: localhost
Porta Oracle no Windows: 1522
Usuário administrativo: system
Senha administrativa: OraclePwd123
ORDS: http://localhost:8181/ords
```

> Importante: os comandos de criação do usuário devem ser executados dentro do PDB `FREEPDB1`, não no `CDB$ROOT`.

---

## 2. Validar se Oracle e ORDS estão de pé

Execute no PowerShell, dentro da pasta do `compose.yaml` do projeto:

```powershell
docker compose ps
```

Para acompanhar os logs do Oracle:

```powershell
docker compose logs -f oracle-free-full-23ai
```

O banco estará pronto quando aparecer algo similar a:

```text
DATABASE IS READY TO USE!
```

Para acompanhar os logs do ORDS:

```powershell
docker compose logs -f ords
```

Teste no navegador:

```text
http://localhost:8181/ords
```

---

## 3. Conectar no Oracle como administrador

Você pode executar os comandos via **DBeaver**, **SQL Developer** ou outro cliente Oracle.

Conexão recomendada:

```text
Host: localhost
Porta: 1522
Service Name: FREEPDB1
Usuário: system
Senha: OraclePwd123
```

Se for conectar como `SYS`:

```text
Host: localhost
Porta: 1522
Service Name: FREEPDB1
Usuário: sys
Senha: OraclePwd123
Role: SYSDBA
```

Valide o container atual:

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

O retorno esperado é:

```text
FREEPDB1
```

Se estiver conectado como `SYS` e aparecer `CDB$ROOT`, altere para o PDB:

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
```

---

## 4. Criar o usuário MONITOR_APP

Execute como `SYSTEM` ou `SYS` conectado no `FREEPDB1`:

```sql
CREATE USER monitor_app IDENTIFIED BY MonitorApp123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION TO monitor_app;
GRANT CREATE TABLE TO monitor_app;
GRANT CREATE VIEW TO monitor_app;
GRANT CREATE PROCEDURE TO monitor_app;
GRANT CREATE SEQUENCE TO monitor_app;
```

### Observação

Para este projeto, o usuário `MONITOR_APP` será o schema responsável por publicar os endpoints REST no ORDS.

---

## 5. Conceder permissões nas views administrativas

Execute como `SYSTEM` ou `SYS` conectado no `FREEPDB1`:

```sql
GRANT SELECT ON SYS.V_$INSTANCE TO monitor_app;
GRANT SELECT ON SYS.V_$DATABASE TO monitor_app;
GRANT SELECT ON SYS.V_$SESSION TO monitor_app;
GRANT SELECT ON SYS.V_$SYSTEM_EVENT TO monitor_app;
GRANT SELECT ON SYS.V_$SQLAREA TO monitor_app;
GRANT SELECT ON SYS.V_$PDBS TO monitor_app;
GRANT SELECT ON SYS.V_$SYSSTAT TO monitor_app;
GRANT SELECT ON SYS.DBA_TABLESPACE_USAGE_METRICS TO monitor_app;
```

### Por que usar `SYS.V_$...`?

As views conhecidas como `V$INSTANCE`, `V$SESSION`, `V$SQLAREA` etc. são sinônimos públicos. Para conceder permissão diretamente a outro usuário, normalmente usamos os objetos base `SYS.V_$INSTANCE`, `SYS.V_$SESSION`, `SYS.V_$SQLAREA` e assim por diante.

### Se a permissão de tablespace falhar

Se a view `DBA_TABLESPACE_USAGE_METRICS` não estiver acessível no seu ambiente, remova temporariamente o endpoint de tablespaces e mantenha o dashboard com instância, banco, sessões, waits e SQLs custosos.

---

## 6. Testar permissões do MONITOR_APP

Conecte no Oracle como:

```text
Usuário: monitor_app
Senha: MonitorApp123
Service Name: FREEPDB1
```

Execute:

```sql
SELECT instance_name, status, database_status
FROM v$instance;

SELECT name, open_mode, log_mode
FROM v$database;

SELECT username, status, COUNT(*) AS total_sessions
FROM v$session
WHERE username IS NOT NULL
GROUP BY username, status
ORDER BY username, status;
```

Se essas consultas funcionarem, o usuário está pronto para o ORDS.

---

## 7. Habilitar o schema MONITOR_APP no ORDS

Conectado como `MONITOR_APP`, execute:

```sql
BEGIN
  ORDS.ENABLE_SCHEMA(
    p_enabled             => TRUE,
    p_schema              => 'MONITOR_APP',
    p_url_mapping_type    => 'BASE_PATH',
    p_url_mapping_pattern => 'monitor_app',
    p_auto_rest_auth      => FALSE
  );

  COMMIT;
END;
/
```

Com isso, os endpoints do schema ficarão sob este prefixo:

```text
http://localhost:8181/ords/monitor_app/
```

---

## 8. Criar módulo REST de monitoramento

Conectado como `MONITOR_APP`, execute:

```sql
BEGIN
  ORDS.DEFINE_MODULE(
    p_module_name    => 'monitor',
    p_base_path      => '/monitor/',
    p_items_per_page => 25,
    p_status         => 'PUBLISHED'
  );

  COMMIT;
END;
/
```

O módulo `monitor` criará endpoints neste padrão:

```text
http://localhost:8181/ords/monitor_app/monitor/...
```

---

## 9. Criar endpoint GET /health

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'health'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'health',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT 'ok' AS status,
             SYSTIMESTAMP AS checked_at
      FROM dual
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/health
```

---

## 10. Criar endpoint GET /stats/instance

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT instance_name,
             status,
             database_status
      FROM v$instance
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/instance
```

---

## 11. Criar endpoint GET /stats/database

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT name,
             open_mode,
             log_mode
      FROM v$database
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/database
```

---

## 12. Criar endpoint GET /stats/container

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container,
             USER AS current_user
      FROM dual
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/container
```

---

## 13. Criar endpoint GET /stats/sessions

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT username,
             status,
             COUNT(*) AS total_sessions
      FROM v$session
      WHERE username IS NOT NULL
      GROUP BY username, status
      ORDER BY username, status
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/sessions
```

---

## 14. Criar endpoint GET /stats/waits

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT event,
             total_waits,
             time_waited
      FROM v$system_event
      WHERE wait_class <> 'Idle'
      ORDER BY time_waited DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/waits
```

---

## 15. Criar endpoint GET /stats/sql

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT sql_id,
             executions,
             elapsed_time,
             cpu_time,
             buffer_gets
      FROM v$sqlarea
      ORDER BY elapsed_time DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/sql
```

---

## 16. Criar endpoint GET /stats/tablespaces

```sql
BEGIN
  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT tablespace_name,
             used_percent,
             tablespace_size,
             used_space
      FROM dba_tablespace_usage_metrics
      ORDER BY used_percent DESC
    ]'
  );

  COMMIT;
END;
/
```

Teste:

```text
http://localhost:8181/ords/monitor_app/monitor/stats/tablespaces
```

---

## 17. Configurar CORS se o frontend estiver em outra origem

Se você abrir o dashboard por outro endereço, por exemplo:

```text
http://localhost:5500
```

mas a API estiver em:

```text
http://localhost:8181
```

então o navegador pode bloquear as chamadas por CORS.

Para liberar chamadas do frontend local, conectado como `MONITOR_APP`, execute:

```sql
BEGIN
  ORDS.SET_MODULE_ORIGINS_ALLOWED(
    p_module_name       => 'monitor',
    p_origins_allowed   => 'http://localhost:5500,http://127.0.0.1:5500'
  );

  COMMIT;
END;
/
```

Se quiser remover as origens permitidas depois:

```sql
BEGIN
  ORDS.SET_MODULE_ORIGINS_ALLOWED(
    p_module_name       => 'monitor',
    p_origins_allowed   => ''
  );

  COMMIT;
END;
/
```

> Para a apresentação, o caminho mais simples é servir o frontend localmente em `http://localhost:5500` e liberar essa origem no módulo ORDS.

---

## 18. Testes via PowerShell

Use `curl.exe` no PowerShell:

```powershell
curl.exe http://localhost:8181/ords/monitor_app/monitor/health
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/instance
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/database
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/container
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/sessions
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/waits
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/sql
curl.exe http://localhost:8181/ords/monitor_app/monitor/stats/tablespaces
```

---

## 19. Consultar módulos criados no ORDS

Conectado como `MONITOR_APP`, execute:

```sql
SELECT name,
       uri_prefix,
       status
FROM user_ords_modules
ORDER BY name;
```

Para consultar templates:

```sql
SELECT module_name,
       uri_template
FROM user_ords_templates
ORDER BY module_name, uri_template;
```

Para consultar handlers:

```sql
SELECT module_name,
       pattern,
       method,
       source_type
FROM user_ords_handlers
ORDER BY module_name, pattern, method;
```

Se alguma dessas views não existir no ambiente, valide os endpoints diretamente pelo navegador ou `curl.exe`.

---

## 20. Script único para recriar endpoints ORDS

Se você quiser recriar somente os endpoints, conectado como `MONITOR_APP`, pode executar este bloco completo:

```sql
BEGIN
  ORDS.DEFINE_MODULE(
    p_module_name    => 'monitor',
    p_base_path      => '/monitor/',
    p_items_per_page => 25,
    p_status         => 'PUBLISHED'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'health'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'health',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT 'ok' AS status,
             SYSTIMESTAMP AS checked_at
      FROM dual
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT instance_name,
             status,
             database_status
      FROM v$instance
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT name,
             open_mode,
             log_mode
      FROM v$database
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container,
             USER AS current_user
      FROM dual
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT username,
             status,
             COUNT(*) AS total_sessions
      FROM v$session
      WHERE username IS NOT NULL
      GROUP BY username, status
      ORDER BY username, status
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT event,
             total_waits,
             time_waited
      FROM v$system_event
      WHERE wait_class <> 'Idle'
      ORDER BY time_waited DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT sql_id,
             executions,
             elapsed_time,
             cpu_time,
             buffer_gets
      FROM v$sqlarea
      ORDER BY elapsed_time DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT tablespace_name,
             used_percent,
             tablespace_size,
             used_space
      FROM dba_tablespace_usage_metrics
      ORDER BY used_percent DESC
    ]'
  );

  ORDS.SET_MODULE_ORIGINS_ALLOWED(
    p_module_name     => 'monitor',
    p_origins_allowed => 'http://localhost:5500,http://127.0.0.1:5500'
  );

  COMMIT;
END;
/
```

---

## 21. URLs finais para usar no dashboard

```text
Health:
http://localhost:8181/ords/monitor_app/monitor/health

Instância:
http://localhost:8181/ords/monitor_app/monitor/stats/instance

Banco:
http://localhost:8181/ords/monitor_app/monitor/stats/database

Container atual:
http://localhost:8181/ords/monitor_app/monitor/stats/container

Sessões:
http://localhost:8181/ords/monitor_app/monitor/stats/sessions

Waits:
http://localhost:8181/ords/monitor_app/monitor/stats/waits

SQLs custosos:
http://localhost:8181/ords/monitor_app/monitor/stats/sql

Tablespaces:
http://localhost:8181/ords/monitor_app/monitor/stats/tablespaces
```

---

## 22. Como explicar essa decisão no trabalho

Texto sugerido para documentação ou apresentação:

```text
A solução utiliza o ORDS como camada de API REST, evitando a necessidade de criar um backend adicional em Go, Python ou Node.js. Como o objetivo do trabalho é demonstrar a leitura de métricas atuais do Oracle e sua exibição em um dashboard simples, o ORDS permite expor consultas SQL diretamente como endpoints HTTP. Dessa forma, o foco da implementação fica na consulta das views administrativas, na organização das métricas e na atualização periódica da interface.
```

---

## 23. Pontos de atenção para a apresentação

1. Execute os endpoints antes da apresentação para validar permissões.
2. Se `/stats/sql` falhar, provavelmente falta permissão em `V_$SQLAREA`.
3. Se `/stats/tablespaces` falhar, provavelmente falta permissão em `DBA_TABLESPACE_USAGE_METRICS`.
4. Se o dashboard HTML não conseguir chamar os endpoints, verifique CORS.
5. Para simplificar a apresentação, deixe o Oracle, o ORDS e o dashboard já abertos antes de demonstrar.

---

## 24. Ordem recomendada de execução

```text
1. Subir Oracle + ORDS pelo Docker Compose
2. Validar http://localhost:8181/ords
3. Conectar como SYSTEM no FREEPDB1
4. Criar usuário MONITOR_APP
5. Conceder grants nas views administrativas
6. Conectar como MONITOR_APP
7. Habilitar schema no ORDS
8. Criar módulo monitor
9. Criar endpoints REST
10. Testar endpoints no navegador ou curl.exe
11. Conectar o frontend HTML aos endpoints
```