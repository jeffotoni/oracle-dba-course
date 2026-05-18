Oracle carga e movimentação de dados: escolha rápida

1. SQL*Loader (sqlldr)

Quando usar:

Arquivo externo (CSV, TXT, delimitado, fixo) → carregar para tabela Oracle

Ideal para:

* CSV de 10 MB até centenas de GB
* Arquivos TXT gigantes
* Carga inicial em massa
* Batch noturno
* Dados vindos de ERP, mainframe, legado

Melhor cenário:

* Grande volume (1 GB, 10 GB, 500 GB)
* Performance alta com DIRECT=TRUE
* Não precisa consultar arquivo antes

⸻

Exemplo:

arquivo.csv
1,Jefferson,MG
2,Maria,SP


control.ctl

LOAD DATA
INFILE 'arquivo.csv'
INTO TABLE clientes
FIELDS TERMINATED BY ','
(
  id,
  nome,
  estado
)


Rodar:
sqlldr user/password control=control.ctl direct=true log=load.log



Vantagens:

* Muito rápido
* Bulk load pesado
* Suporta milhões de linhas

Limitações:

* Precisa control file
* Menos flexível para análise SQL imediata



2. Tabela Externa (External Table)

Quando usar:

Quer consultar arquivo como se fosse tabela, usando SQL

Ideal para:

* CSV médio/grande
* Validar antes de importar
* JOIN com tabelas Oracle
* ETL
* Arquivo de 1 MB a dezenas/centenas de GB

⸻

Melhor cenário:

* Você quer fazer:


SELECT * FROM arquivo_externo WHERE estado='MG';


Exemplo:

CREATE DIRECTORY ext_dir AS '/u01/files';

CREATE TABLE clientes_ext (
  id NUMBER,
  nome VARCHAR2(100),
  estado VARCHAR2(2)
)
ORGANIZATION EXTERNAL (
  TYPE ORACLE_LOADER
  DEFAULT DIRECTORY ext_dir
  ACCESS PARAMETERS (
    RECORDS DELIMITED BY NEWLINE
    FIELDS TERMINATED BY ','
  )
  LOCATION ('arquivo.csv')
);

Usar:
SELECT * FROM clientes_ext;

Inserir:
INSERT INTO clientes
SELECT * FROM clientes_ext;


Vantagens:

* SQL direto no arquivo
* Sem carga inicial obrigatória
* Ótimo para validação

Limitações:

* Mais lento que SQL*Loader para carga definitiva
* Depende do arquivo permanecer no disco

⸻

⸻

3. Data Pump (expdp / impdp)

Quando usar:

Oracle → Oracle

Ideal para:

* Migrar schemas
* Backup lógico
* Exportar tabelas
* Clonar ambiente DEV/QA/PROD
* Mover milhões/bilhões de registros entre bancos Oracle

⸻

Melhor cenário:

* Banco Oracle para outro Oracle
* Estrutura + dados
* Muito mais moderno que exp/imp


Export:
expdp system/password schemas=RH directory=DATA_PUMP_DIR dumpfile=rh.dmp logfile=exp.log

Import
impdp system/password schemas=RH directory=DATA_PUMP_DIR dumpfile=rh.dmp logfile=imp.log

Só uma tabela:
expdp system/password tables=RH.CLIENTES directory=DATA_PUMP_DIR dumpfile=clientes.dmp


Vantagens:

* Muito rápido Oracle-to-Oracle
* Preserva índices, grants, constraints
* Paralelismo

Limitações:

* Não serve para CSV/TXT
* Formato Oracle proprietário

⸻

4. SQL*Plus (sqlplus)

Quando usar:

Administração, scripts SQL, automação simples

Ideal para:

* Rodar scripts .sql
* Criar tabelas
* INSERTs pequenos
* ETL simples
* Agendamento shell


Exemplo:
sqlplus user/password@ORCL

@script.sql


CSV para insert manual:
INSERT INTO clientes VALUES (1,'Jefferson','MG');
COMMIT;

Vantagens:

* Simples
* Universal
* Scripts

Limitações:

* Péssimo para arquivos gigantes
* Não é ferramenta de bulk load

⸻

Regra prática por tamanho / uso

Cenário

Melhor ferramenta

CSV 5 MB

SQL*Plus / External Table

CSV 500 MB

SQL*Loader

CSV 50 GB

SQL*Loader Direct Path

Validar CSV antes

External Table

Oracle → Oracle schema

Data Pump

Backup tabela Oracle

expdp

Restaurar Oracle

impdp

Script SQL admin

sqlplus

Regra de ouro:

Use:

sqlldr

Quando arquivo externo é grande e precisa entrar rápido

external table

Quando quer ler/filtrar/validar com SQL antes

expdp / impdp

Quando origem e destino são Oracle

sqlplus

Quando é administração ou scripts


Exemplo realista:

Você recebeu clientes_500GB.csv

Melhor:
sqlldr user/password control=clientes.ctl direct=true parallel=true


Você quer analisar primeiro:
SELECT COUNT(*) FROM clientes_ext;
SELECT estado, COUNT(*) FROM clientes_ext GROUP BY estado;



Você quer migrar PROD Oracle → QA Oracle:
expdp ...
impdp ...


Dica de performance pesada:
SQL*Loader:

direct=true
parallel=true
errors=100000
rows=50000
bindsize=10485760
readsize=10485760


Resumo:

Arquivo → Oracle:
SQL*Loader

Arquivo + SQL:
External Table

Oracle → Oracle:
Data Pump

Script/Admin:
SQL*Plus


