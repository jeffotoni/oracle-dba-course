-- Parametros
SELECT name, value
FROM v$parameter
WHERE name = 'spfile';

SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'open_cursors';

SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'processes';

SELECT name,
       value,
       isdefault,
       issys_modifiable
FROM v$parameter
WHERE name = 'sessions';

SELECT name,
       value,
       issys_modifiable
FROM v$parameter
WHERE name IN ('open_cursors', 'processes', 'sessions')
ORDER BY name;

-- Containers
SELECT con_id,
       name,
       open_mode
FROM v$pdbs
ORDER BY con_id;

-- Comandos de demonstracao
-- ALTER SYSTEM SET open_cursors = 500 SCOPE=BOTH;
-- SHUTDOWN IMMEDIATE;
-- STARTUP;

-- Usuario de laboratorio
-- CREATE USER aluno IDENTIFIED BY Aluno123;
-- GRANT CREATE SESSION TO aluno;
-- GRANT CREATE TABLE TO aluno;
-- GRANT CREATE VIEW TO aluno;
-- GRANT SELECT_CATALOG_ROLE TO aluno;
