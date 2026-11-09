# Pipeline de Ingestão e Modelagem SQL: Dados Climáticos (BR-DWGD)

Este projeto consiste na construção de um pipeline de dados analíticos para armazenar e consultar dados climáticos históricos do conjunto de dados **BR-DWGD (Brazilian Daily Weather Gridded Data)**, com foco nas **Regiões de Cafés Especiais do Brasil**. 

O objetivo principal deste repositório é aplicar técnicas de **Engenharia de Dados e Modelagem Relacional**, realizando a ingestão de arquivos `.parquet` para um banco de dados **PostgreSQL** utilizando **Python**.

---

## Arquitetura do Projeto

O fluxo de dados foi dividido em duas fases. Este repositório foca na **Fase 2**:

1. **Fase 1: Extração ([special-coffee-climate-change](https://github.com/matheus-naves47/special-coffee-climate-change))**
   - Dados brutos em formato `.nc` (NetCDF) foram processados utilizando linguagem R (pacote `exactextract`).
   - Foram extraídas métricas climáticas específicas para os polígonos das regiões cafeeiras.
   - Os resultados foram salvos localmente em partições anuais no formato `.parquet`.

2. **Fase 2: Ingestão e Modelagem (Este Repositório)**
   - **Python** (via `pandas` e `SQLAlchemy`) lê os arquivos `.parquet` em lote.
   - Os dados são tipados e carregados em tabelas normalizadas no **PostgreSQL**.
   - Criação de índices para otimização de consultas temporais e espaciais.

## Ferramentas Utilizadas

- **Banco de Dados:** PostgreSQL
- **Linguagem:** Python 3.15.0
- **Bibliotecas:** `pandas`, `SQLAlchemy`, `psycopg2-binary`, `pyarrow`