# Revisão do Módulo 3 - aula 4

> Revisão do módulo 3: backup, recuperação, `ARCHIVELOG`, `Data Pump`, `RMAN`, restore e recovery em Oracle.

## Ideia central do módulo

O módulo 3 trata de um dos pontos mais críticos da administração Oracle:

```txt
Proteger dados
Restaurar operação
Reduzir perda e indisponibilidade
```

Em termos práticos:

- backup é preparação;
- recuperação é resposta à falha;
- `Data Pump` atende dump e restore lógico;
- `RMAN` atende backup físico, restore e recovery estrutural.

## O que precisa ficar claro

- backup não é a mesma coisa que recuperação;
- backup lógico e backup físico atendem problemas diferentes;
- `ARCHIVELOG` é central para recuperação consistente;
- `RMAN` é a ferramenta principal de proteção física do Oracle;
- `control file`, `SPFILE` e archivelogs fazem parte da estratégia;
- restore de datafile e tablespace exige leitura operacional cuidadosa;
- parte prática do módulo usa binários nativos Oracle dentro do container.

## 1. Fundamentos

### O que é backup

Backup é a cópia controlada dos dados e metadados necessários para restaurar o ambiente ou parte dele.

### O que é recuperação

Recuperação é o processo de devolver o banco a um estado consistente depois de falha, perda, erro ou corrupção.

### Regra curta

```txt
Backup = preparar
Recuperação = responder
```

## 2. Por que isso é crítico

O módulo 3 existe porque falhas reais acontecem por:

- erro humano;
- falha de instância;
- perda de disco;
- corrupção;
- falha lógica;
- problema de sistema operacional;
- problema de armazenamento.

Sem estratégia de backup e recuperação, a administração fica incompleta.

## 3. Tipos de falha

### Falha de instância

A instância para, mas os arquivos físicos continuam existindo.

### Falha de mídia

Há perda ou dano em arquivo físico, como:

- datafile;
- control file;
- redo log.

### Erro humano

Inclui:

- exclusão indevida;
- update errado em massa;
- comando administrativo incorreto.

### Corrupção

Pode atingir:

- bloco;
- estrutura;
- dados;
- arquivo.

## 4. Backup lógico x backup físico

### Backup lógico

Trabalha com objetos e dados em camada lógica.

Exemplo mental:

- PostgreSQL: `pg_dump`
- MySQL / MariaDB: `mysqldump`
- MongoDB: `mongodump`
- Oracle: `expdp`

### Backup físico

Trabalha com os arquivos reais do banco, incluindo:

- datafiles;
- control files;
- archived redo logs;
- `SPFILE`;
- backups gerados pelo `RMAN`.

### Regra prática

```txt
Dump lógico = objetos e dados
Backup físico = estrutura operacional do banco
```

### Leitura correta

- `expdp` e `impdp` ajudam em dump lógico, cópia de schema e restore seletivo;
- `RMAN` ajuda a restaurar a infraestrutura física do banco.

## 5. Backup frio x backup quente

### Backup frio

É feito com o banco parado.

### Backup quente

É feito com o banco em operação, normalmente com apoio de logs e estratégia adequada.

### Regra curta

```txt
Frio = banco parado
Quente = banco em operação
```

No Oracle moderno, a conversa prática de recuperação séria normalmente leva a:

- `ARCHIVELOG`
- `RMAN`
- retenção
- restore e recovery testados

## 6. ARCHIVELOG

Esse ponto é central no módulo.

### O que é

No modo `ARCHIVELOG`, o Oracle mantém cópia dos redo logs arquivados, permitindo recuperação mais completa.

### Por que importa

Sem `ARCHIVELOG`, a capacidade de recuperação fica mais limitada.

### Regra prática

```txt
ARCHIVELOG melhora a capacidade de recuperação
```

## 7. FRA

`FRA` (`Fast Recovery Area`) é a área controlada pelo Oracle para armazenar arquivos de recuperação.

Ela se relaciona com:

- archived redo logs;
- backups;
- control file autobackup;
- arquivos de recovery.

### O que precisa ficar claro

- não é só “uma pasta”;
- ela participa da estratégia de proteção do banco;
- seu tamanho e uso precisam ser observados.

## 8. RMAN

`RMAN` (`Recovery Manager`) é a ferramenta principal de backup físico, restore e recovery do Oracle.

### O que ele faz

- backup do banco;
- backup incremental;
- backup de archivelogs;
- backup de control file;
- backup de `SPFILE`;
- validação de backups;
- restore;
- recovery;
- retenção;
- cruzamento de catálogo com arquivos reais.

### Regra curta

```txt
RMAN = ferramenta central de proteção física Oracle
```

## 9. Control file e SPFILE

### Control file

Guarda metadados estruturais essenciais do banco.

### SPFILE

Guarda parâmetros persistentes da instância.

### Leitura prática

- ambos são críticos;
- ambos entram na estratégia de backup;
- perder esses arquivos pode complicar seriamente a recuperação.

## 10. Binários nativos Oracle no módulo 3

Assim como no módulo 2, parte importante da prática não acontece só na IDE.

O módulo 3 depende de binários nativos Oracle, principalmente:

- `expdp`
- `impdp`
- `rman`
- `sqlplus`

### Regra prática

```txt
Consultas e validações SQL = Oracle SQL Developer, CloudBeaver, DBeaver ou equivalente
Data Pump e RMAN = terminal dentro do container Oracle
```

### Entrar no container

```bash
podman exec -it oracle-free bash
```

### Validar binários

```bash
which sqlplus
which expdp
which impdp
which rman
```

## 11. Queries essenciais de revisão

### Ver instância

```sql
SELECT instance_name,
       status
FROM v$instance;
```

### Ver banco e modo de log

```sql
SELECT name,
       open_mode,
       log_mode
FROM v$database;
```

### Ver container atual

```sql
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;
```

### Ver parâmetros da FRA

```sql
SELECT name,
       value
FROM v$parameter
WHERE name IN ('db_recovery_file_dest', 'db_recovery_file_dest_size')
ORDER BY name;
```

### Ver datafiles

```sql
SELECT file_id,
       file_name,
       tablespace_name,
       status
FROM dba_data_files
ORDER BY file_id;
```

### Ver archived logs

```sql
SELECT sequence#,
       archived,
       status,
       first_time
FROM v$archived_log
ORDER BY sequence# DESC;
```

### Ver uso da FRA

```sql
SELECT name,
       space_limit / 1024 / 1024 AS fra_limit_mb,
       space_used / 1024 / 1024 AS fra_used_mb,
       space_reclaimable / 1024 / 1024 AS fra_reclaimable_mb
FROM v$recovery_file_dest;
```

### Ver jobs de backup do RMAN

```sql
SELECT session_key,
       input_type,
       status,
       start_time,
       end_time
FROM v$rman_backup_job_details
ORDER BY start_time DESC
FETCH FIRST 10 ROWS ONLY;
```

## 12. Fluxo prático mínimo do módulo

```txt
1. Validar instância, banco, PDB e log_mode
2. Configurar FRA
3. Habilitar ARCHIVELOG
4. Criar objetos de laboratório
5. Fazer dump lógico com expdp
6. Importar com impdp
7. Entrar no RMAN
8. Configurar retenção e control file autobackup
9. Fazer backup completo e incremental
10. Validar, listar e cruzar backups
11. Simular recovery de instância e tablespace
```

## 13. Comandos que valem aparecer na revisão

### Entrar no container

```bash
podman exec -it oracle-free bash
```

### Exportar schema com Data Pump

```bash
podman exec -i oracle-free bash -lc "expdp app_rman/AppRman123@//localhost:1521/FREEPDB1 \
schemas=APP_RMAN \
directory=DATA_PUMP_DIR \
dumpfile=app_rman_m3.dmp \
logfile=app_rman_m3_exp.log"
```

### Importar schema com remapeamento

```bash
podman exec -i oracle-free bash -lc "impdp system/Senha123@//localhost:1521/FREEPDB1 \
schemas=APP_RMAN \
directory=DATA_PUMP_DIR \
dumpfile=app_rman_m3.dmp \
logfile=app_rman_m3_imp.log \
remap_schema=APP_RMAN:APP_RMAN_CLONE"
```

### Entrar no RMAN

```bash
rman target /
```

### Configuração inicial do RMAN

```rman
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
SHOW ALL;
```

### Backup completo

```rman
BACKUP DATABASE PLUS ARCHIVELOG;
```

### Backup incremental

```rman
BACKUP INCREMENTAL LEVEL 0 DATABASE TAG 'BKP_L0_MOD3';
BACKUP INCREMENTAL LEVEL 1 DATABASE TAG 'BKP_L1_MOD3';
```

### Validar backups

```rman
VALIDATE DATABASE;
RESTORE DATABASE VALIDATE;
REPORT OBSOLETE;
```

### Cruzar catálogo

```rman
CROSSCHECK BACKUP;
CROSSCHECK ARCHIVELOG ALL;
```

### Restore e recover de tablespace

```rman
RESTORE TABLESPACE ts_rman_lab;
RECOVER TABLESPACE ts_rman_lab;
```

### Exemplo de PITR

```rman
RUN {
  SET UNTIL TIME "TO_DATE('2026-04-14 10:00:00','YYYY-MM-DD HH24:MI:SS')";
  RESTORE DATABASE;
  RECOVER DATABASE;
}
```

## 14. Exemplos práticos que valem reforçar

## 14.1. Dump lógico antes de RMAN

No módulo 3, vale reforçar que o primeiro raciocínio de dump em laboratório costuma ser:

```txt
expdp / impdp
```

Isso ajuda em:

- laboratório;
- desenvolvimento;
- cópia de schema;
- restore seletivo;
- comparação com `pg_dump`, `mysqldump` e `mongodump`.

## 14.2. RMAN como proteção séria

Quando a conversa sai de dump lógico e entra em proteção operacional do banco, o pensamento muda para:

```txt
ARCHIVELOG + FRA + RMAN + retenção + teste de recovery
```

## 14.3. Recovery de instância

É o cenário mais simples para demonstrar que o Oracle se recupera automaticamente após parada abrupta.

Exemplo:

```sql
SHUTDOWN ABORT;
STARTUP;
```

## 14.4. Recovery de datafile ou tablespace

É o cenário que ajuda a turma a visualizar:

- perda de arquivo físico;
- restore;
- recovery;
- retorno ao estado consistente.

## 14.5. Block recover

Vale apresentar como recurso avançado, sem necessidade de induzir corrupção real em toda turma.

Exemplo:

```rman
BLOCKRECOVER DATAFILE <FILE_ID> BLOCK <BLOCK_NUMBER>;
```

## 15. Resultado esperado

Ao final da revisão, o que precisa ficar claro é:

- backup não é recuperação;
- `expdp` e `impdp` atendem dump e restore lógico;
- `RMAN` atende proteção física, restore e recovery;
- `ARCHIVELOG` é central para recuperação;
- `FRA`, `control file` e `SPFILE` fazem parte da estratégia;
- binários nativos Oracle precisam aparecer no fluxo prático do módulo;
- recuperação precisa ser pensada como disciplina operacional, não só como comando.

## Scripts originais do módulo

- `modulo3-material/03-teoria-modulo3.md`
  - base conceitual de backup e recuperação.
- `modulo3-material/03-pratica-modulo3.md`
  - roteiro prático completo com `Data Pump`, `ARCHIVELOG`, `RMAN`, restore e recovery.
