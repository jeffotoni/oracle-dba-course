-- ============================================================
-- SCRIPT: criar_usuarios_simulacao.sql
-- OBJETIVO:
-- Criar usuários para simular carga no Oracle e alimentar
-- o dashboard de monitoramento em tempo real.
--
-- EXECUTAR COMO:
-- SYSTEM ou SYSDBA conectado no service FREEPDB1
-- ============================================================


-- ============================================================
-- 1. LIMPEZA OPCIONAL
-- Remove usuários antigos caso existam.
-- Se for a primeira execução, os erros de usuário inexistente
-- serão ignorados.
-- ============================================================

BEGIN
  FOR r IN (
    SELECT username
    FROM dba_users
    WHERE username IN (
      'SIM_OWNER',
      'SIM_USER_01',
      'SIM_USER_02',
      'SIM_USER_03'
    )
  ) LOOP
    EXECUTE IMMEDIATE 'DROP USER ' || r.username || ' CASCADE';
  END LOOP;
END;



-- ============================================================
-- 2. CRIAÇÃO DO USUÁRIO DONO DOS OBJETOS
-- SIM_OWNER será o schema que armazenará a tabela de carga.
-- ============================================================

CREATE USER sim_owner IDENTIFIED BY SimOwner123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION TO sim_owner;
GRANT CREATE TABLE TO sim_owner;
GRANT CREATE SEQUENCE TO sim_owner;
GRANT CREATE PROCEDURE TO sim_owner;


-- ============================================================
-- 3. CRIAÇÃO DOS USUÁRIOS SIMULADOS
-- Estes serão os usuários que o Python usará para abrir sessões.
-- ============================================================

CREATE USER sim_user_01 IDENTIFIED BY SimUser123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

CREATE USER sim_user_02 IDENTIFIED BY SimUser123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

CREATE USER sim_user_03 IDENTIFIED BY SimUser123
  DEFAULT TABLESPACE USERS
  TEMPORARY TABLESPACE TEMP
  QUOTA UNLIMITED ON USERS;

GRANT CREATE SESSION TO sim_user_01;
GRANT CREATE SESSION TO sim_user_02;
GRANT CREATE SESSION TO sim_user_03;


-- ============================================================
-- 4. TABELA PRINCIPAL DE CARGA
-- Tabela com massa de dados para consultas simuladas.
-- ============================================================

CREATE TABLE sim_owner.carga_lab
NOLOGGING
AS
SELECT
  LEVEL AS id,
  'CLIENTE_' || MOD(LEVEL, 1000) AS cliente,
  CASE MOD(LEVEL, 5)
    WHEN 0 THEN 'INFORMATICA'
    WHEN 1 THEN 'MOVEIS'
    WHEN 2 THEN 'AUDIO'
    WHEN 3 THEN 'VIDEO'
    ELSE 'PERIFERICOS'
  END AS categoria,
  CASE MOD(LEVEL, 6)
    WHEN 0 THEN 'BELO HORIZONTE'
    WHEN 1 THEN 'SAO PAULO'
    WHEN 2 THEN 'RIO DE JANEIRO'
    WHEN 3 THEN 'CURITIBA'
    WHEN 4 THEN 'SALVADOR'
    ELSE 'RECIFE'
  END AS cidade,
  ROUND(DBMS_RANDOM.VALUE(50, 5000), 2) AS valor_total,
  SYSDATE - MOD(LEVEL, 365) AS data_venda,
  CASE MOD(LEVEL, 4)
    WHEN 0 THEN 'ABERTA'
    WHEN 1 THEN 'FATURADA'
    WHEN 2 THEN 'CANCELADA'
    ELSE 'ENTREGUE'
  END AS status_venda
FROM dual
CONNECT BY LEVEL <= 100000;


-- ============================================================
-- 5. CHAVE PRIMÁRIA E ÍNDICES
-- Um índice para algumas consultas performarem melhor
-- e outro cenário para consultas com funçãovarredura ficarem
-- mais custosas.
-- ============================================================

ALTER TABLE sim_owner.carga_lab
ADD CONSTRAINT pk_carga_lab PRIMARY KEY (id);

CREATE INDEX sim_owner.idx_carga_lab_cat_cid
ON sim_owner.carga_lab (categoria, cidade);

CREATE INDEX sim_owner.idx_carga_lab_data
ON sim_owner.carga_lab (data_venda);


-- ============================================================
-- 6. TABELA PARA SIMULAR LOCK
-- O Python atualizará esta tabela ocasionalmente.
-- Em modo intenso, mais de uma sessão pode tentar atualizar
-- o mesmo registro, gerando espera por lock.
-- ============================================================

CREATE TABLE sim_owner.lock_lab (
  id NUMBER PRIMARY KEY,
  descricao VARCHAR2(200),
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

INSERT INTO sim_owner.lock_lab (id, descricao)
VALUES (1, 'REGISTRO PARA TESTE DE LOCK');

COMMIT;


-- ============================================================
-- 7. PERMISSÕES PARA OS USUÁRIOS SIMULADOS
-- Eles conseguem consultar a tabela de carga e atualizar
-- a tabela de lock.
-- ============================================================

GRANT SELECT ON sim_owner.carga_lab TO sim_user_01;
GRANT SELECT ON sim_owner.carga_lab TO sim_user_02;
GRANT SELECT ON sim_owner.carga_lab TO sim_user_03;

GRANT SELECT, UPDATE ON sim_owner.lock_lab TO sim_user_01;
GRANT SELECT, UPDATE ON sim_owner.lock_lab TO sim_user_02;
GRANT SELECT, UPDATE ON sim_owner.lock_lab TO sim_user_03;


-- ============================================================
-- 8. COLETA DE ESTATÍSTICAS
-- Ajuda o otimizador do Oracle a escolher planos mais coerentes.
-- ============================================================

BEGIN
  DBMS_STATS.GATHER_SCHEMA_STATS(
    ownname => 'SIM_OWNER',
    cascade => TRUE
  );
END;



-- ============================================================
-- 9. VALIDAÇÃO FINAL
-- ============================================================

SELECT username
FROM dba_users
WHERE username IN (
  'SIM_OWNER',
  'SIM_USER_01',
  'SIM_USER_02',
  'SIM_USER_03'
)
ORDER BY username;

SELECT COUNT(*) AS total_registros
FROM sim_owner.carga_lab;

SELECT categoria, COUNT(*) AS total
FROM sim_owner.carga_lab
GROUP BY categoria
ORDER BY categoria;

SELECT *
FROM sim_owner.lock_lab;