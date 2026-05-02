LOAD DATA
INFILE '/opt/oracle/labdata/produtos.csv'
INTO TABLE app_owner.produtos_carga
FIELDS TERMINATED BY ','
(
  id_produto,
  nome_produto,
  categoria,
  preco
)
