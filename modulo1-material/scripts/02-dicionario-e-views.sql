-- Dicionario de dados
SELECT table_name
FROM dictionary
WHERE table_name LIKE 'DBA_%'
ORDER BY table_name;

SELECT table_name
FROM dictionary
WHERE table_name LIKE 'V$%'
ORDER BY table_name;

-- Usuarios, roles e privilegios
SELECT username, account_status, default_tablespace, profile
FROM dba_users
ORDER BY username;

SELECT role
FROM dba_roles
ORDER BY role;

SELECT grantee, privilege
FROM dba_sys_privs
WHERE grantee IN ('SYSTEM', 'SYS')
ORDER BY grantee, privilege;

SELECT * FROM session_privs ORDER BY privilege;
SELECT * FROM user_role_privs ORDER BY granted_role;
