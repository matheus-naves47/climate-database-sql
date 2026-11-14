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


# Pipeline de Ingestão e Modelagem SQL: Dados Climáticos (BR-DWGD)

Este projeto demonstra a construção e a implementação de um pipeline de dados analíticos completo para armazenar e consultar dados climáticos históricos do conjunto de dados **BR-DWGD (Brazilian Daily Weather Gridded Data)**. O foco atual da base de dados são as **Regiões de Cafés Especiais do Brasil**, contemplando as resoluções regional e municipal.

O objetivo principal deste repositório é aplicar técnicas de **Engenharia de Dados e Modelagem Relacional**, estruturando a ingestão massiva de arquivos particionados (`.parquet`) para um banco de dados **PostgreSQL** otimizado para consultas analíticas.

---

## Arquitetura e Fases do Projeto

O fluxo de dados foi desenhado para evoluir desde a extração bruta até o carregamento num banco de dados.

*   **Fase 1: Extração e Pré-processamento (em [special-coffee-climate-change](https://github.com/matheus-naves47/special-coffee-climate-change))**
    *   Processamento de dados brutos em formato `.nc` (NetCDF) utilizando linguagem R (pacote `exactextract`).
    *   Extração de métricas climáticas (precipitação, temperaturas, ETo, radiação, etc.) para os polígonos das regiões cafeeiras e seus respectivos municípios.
    *   Armazenamento particionado em formato `.parquet`.
*   **Fase 2: Ingestão e Modelagem Relacional (Este repositório)**
    *   Desenvolvimento de scripts em **Python** (via `pandas` e `SQLAlchemy`) para leitura em lote.
    *   Modelagem *Snowflake* no **PostgreSQL**, separando dados cadastrais (Região/Município) de dados transacionais climáticos (`clima_regional` e `clima_municipal`).
    *   Criação de chaves primárias/estrangeiras e índices para otimização de performance.
---

## Ferramentas Utilizadas

- **Banco de Dados:** PostgreSQL (Configurado via `systemctl` / fedora-server)
- **Linguagem:** Python 3.x
- **Bibliotecas de Engenharia:** `pandas`, `SQLAlchemy`, `psycopg2-binary`, `pyarrow`
- **Orquestração de IA (Roadmap):** API do Gemini, LangChain, Streamlit

## Configuração da conexão com o PostgreSQL

Os scripts de conexão e ingestão carregam a senha do usuário `naves` pela variável de ambiente `POSTGRES_PASSWORD`. Defina-a no terminal antes de executar os scripts:

```bash
export POSTGRES_PASSWORD='sua senha'
```

A conexão é criada com `URL.create`, do SQLAlchemy, para tratar corretamente caracteres especiais na senha. Não armazene a senha diretamente nos scripts nem a versione no repositório.

Para testar a conexão:

```bash
python src/sql_connection_test.py
```

O script de teste e o carregamento de amostra usam o banco `special_coffee_br_dwgd_test`:

```bash
python src/load_data_test_run.py
```

O carregamento completo usa o banco `special_coffee_br_dwgd`:

```bash
python src/load_data.py
```

No repositório, encontram-se amostras das tabelas em .csv e um dump do banco de dados de teste (1000 linhas). Posteriormente, o banco será disponibilizado integralmente.