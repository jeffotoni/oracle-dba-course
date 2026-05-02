-- Tablespaces e arquivos
SELECT tablespace_name, contents, status
FROM dba_tablespaces
ORDER BY tablespace_name;

SELECT file_id, file_name, tablespace_name, bytes/1024/1024 AS mb
FROM dba_data_files
ORDER BY file_id;

SELECT tablespace_name, file_name, bytes/1024/1024 AS mb
FROM dba_temp_files
ORDER BY tablespace_name;

SELECT name FROM v$datafile ORDER BY name;
SELECT member FROM v$logfile ORDER BY member;
SELECT name FROM v$controlfile ORDER BY name;

-- Memoria
SELECT * FROM v$sga;

SELECT pool, name, bytes
FROM v$sgastat
ORDER BY pool, bytes DESC;

-- Processos de background
SELECT name, description
FROM v$bgprocess
WHERE paddr <> '00'
ORDER BY name;

-- Sessoes e processos
SELECT sid, serial#, username, status, program
FROM v$session
ORDER BY sid;

SELECT spid, program
FROM v$process
ORDER BY spid;
