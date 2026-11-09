# ==========================================
# load_data.py - VERSÃO DE TESTE
# ==========================================

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# 1. Configuração da Conexão
engine = create_engine('postgresql+psycopg2://postgres:passwd@localhost:5432/special_coffee_br_dwgd_database')

# ==========================================
# 1. POPULAR REGIÕES DE ORIGEM (CSV)
# ==========================================
print("Carregando CSV de Regiões e Municípios...")
df_csv = pd.read_csv("/home/naves/Projetos/climate-database-sql/data/raw/origin_regions.csv")

# 1. Extrair e Inserir Regiões Únicas
df_regioes = pd.DataFrame({'nome_regiao': df_csv['REGIAO'].unique()})
df_regioes.to_sql('regiao', engine, if_exists='append', index=False)

# 2. Ler as Regiões do banco (para pegar os id_regiao gerados)
df_regioes_db = pd.read_sql("SELECT id_regiao, nome_regiao FROM regiao", engine)

# 3. Preparar e Inserir Municípios
# Cruzar o CSV com os IDs do banco usando o nome da região
df_mun = df_csv.merge(df_regioes_db, left_on='REGIAO', right_on='nome_regiao')
df_mun_insert = df_mun[['MUNICIPIO', 'UF_SIGLA', 'id_regiao']].rename(
    columns={'MUNICIPIO': 'nome_municipio', 'UF_SIGLA': 'uf_sigla'}
)
df_mun_insert.to_sql('municipio', engine, if_exists='append', index=False)

# 4. Ler os Municípios do banco (para pegar os id_municipio gerados)
df_mun_db = pd.read_sql("SELECT id_municipio, nome_municipio, uf_sigla FROM municipio", engine)

# ==========================================
# 2. INGESTÃO CLIMA REGIONAL (1 Arquivo)
# ==========================================
print("Carregando Parquet Regional...")

df_clima_reg = pd.read_parquet('/home/naves/Projetos/CEPAGRI/special-coffee-climate-change/data/processed/BR_DWGD/regional/BR_DWGD_regions_daily.parquet')
df_clima_reg = df_clima_reg.rename(columns={
    'TMIN': 'tmin_c', 'TMAX': 'tmax_c', 'PR': 'pr_mm', 
    'ETO': 'eto_mm', 'RH': 'rh_pct', 'Rs': 'rs', 'U2': 'u2_m_s',
    'DATE': 'data_ref'  
})

df_clima_reg = df_clima_reg.merge(df_regioes_db, left_on='BSCA_REGION', right_on='nome_regiao')

# Em vez de usar .drop() para apagar as colunas uma a uma, 
# seleciona explicitamente apenas as que serão enviadas para o banco:
colunas_banco = ['id_regiao', 'data_ref', 'pr_mm', 'tmax_c', 'tmin_c', 'eto_mm', 'rh_pct', 'rs', 'u2_m_s']
df_clima_reg = df_clima_reg[colunas_banco]

# Insere apenas 100 linhas para teste
df_teste_reg = df_clima_reg.head(100)
df_teste_reg.to_sql('clima_regional', engine, if_exists='append', index=False, method='multi', chunksize=10000)

# ==========================================
# 3. INGESTÃO CLIMA MUNICIPAL (64 Arquivos)
# ==========================================
print("Iniciando carga dos 64 Parquets Municipais...")
pasta_municipal = Path("/home/naves/Projetos/CEPAGRI/special-coffee-climate-change/data/processed/BR_DWGD/municipal_regions/")

for arquivo in pasta_municipal.glob("*.parquet"):
    print(f"Ingerindo teste: {arquivo.name}")
    df_clima_mun = pd.read_parquet(arquivo)
    
    df_clima_mun = df_clima_mun.rename(columns={
        'TMIN': 'tmin_c', 'TMAX': 'tmax_c', 'PR': 'pr_mm', 
        'ETO': 'eto_mm', 'RH': 'rh_pct', 'Rs': 'rs', 'U2': 'u2_m_s',
        'DATE': 'data_ref'
    })
    
    df_clima_mun = df_clima_mun.merge(df_mun_db, 
                                      left_on=['MUNICIPALITY', 'UF_2'], 
                                      right_on=['nome_municipio', 'uf_sigla'])
    
    # Seleciona apenas as colunas que vão para a tabela clima_municipal
    colunas_banco_mun = ['id_municipio', 'data_ref', 'pr_mm', 'tmax_c', 'tmin_c', 'eto_mm', 'rh_pct', 'rs', 'u2_m_s']
    df_clima_mun = df_clima_mun[colunas_banco_mun]
    
    df_teste_mun = df_clima_mun.head(100)
    df_teste_mun.to_sql('clima_municipal', engine, if_exists='append', index=False, method='multi', chunksize=10000)
    
    break

print("Pipeline de teste concluído!")

# Para testar no psql
# SELECT * FROM clima_regional LIMIT 10;
# SELECT * FROM clima_municipal LIMIT 10;