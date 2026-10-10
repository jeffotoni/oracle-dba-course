LOAD DATA
INFILE '/opt/oracle/labdata/produtos.csv'
INTO TABLE produtos_carga
TRUNCATE
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
  id_produto,
  nome_produto,
  categoria,
  preco
)
