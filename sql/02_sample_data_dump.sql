-- Executar este arquivo com psql. \copy grava no sistema de arquivos do cliente;
-- /tmp evita as restricoes de acesso do usuario postgres a /home/naves.
-- Cada CSV contém 1000 linhas, ordenados pela chave primária.
\copy (SELECT * FROM regiao ORDER BY id_regiao LIMIT 1000) TO '/tmp/amostra_regiao.csv' WITH (FORMAT CSV, HEADER TRUE);
\copy (SELECT * FROM municipio ORDER BY id_municipio LIMIT 1000) TO '/tmp/amostra_municipio.csv' WITH (FORMAT CSV, HEADER TRUE);
\copy (SELECT * FROM clima_regional ORDER BY id_medicao LIMIT 1000) TO '/tmp/amostra_clima_regional.csv' WITH (FORMAT CSV, HEADER TRUE);
\copy (SELECT * FROM clima_municipal ORDER BY id_medicao LIMIT 1000) TO '/tmp/amostra_clima_municipal.csv' WITH (FORMAT CSV, HEADER TRUE);

-- Executar no terminal para exportar o arquivo .dump
-- pg_dump -h localhost -U naves -F c -d special_coffee_br_dwgd_test -f /home/naves/Projetos/climate-database-sql/data/sample/special_coffee_br_dwgd_sample.dump 