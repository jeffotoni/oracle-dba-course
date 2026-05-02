-- Validacao do ambiente
SELECT instance_name,
       status,
       version
FROM v$instance;

SELECT name,
       dbid,
       cdb,
       open_mode
FROM v$database;

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container
FROM dual;

-- Componentes instalados
SELECT product, version, status
FROM product_component_version;
