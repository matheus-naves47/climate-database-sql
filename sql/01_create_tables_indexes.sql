-- 1. Tabela de Regiões
CREATE TABLE regiao (
    id_regiao SERIAL PRIMARY KEY,
    nome_regiao VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Tabela de Municípios
CREATE TABLE municipio (
    id_municipio SERIAL PRIMARY KEY,
    nome_municipio VARCHAR(100) NOT NULL,
    uf_sigla VARCHAR(2) NOT NULL,
    id_regiao INT NOT NULL,
    
    CONSTRAINT fk_regiao 
        FOREIGN KEY (id_regiao) REFERENCES regiao (id_regiao) ON DELETE CASCADE
);

-- 3. Dados Climáticos Regionais (1 Arquivo)
CREATE TABLE clima_regional (
    id_medicao BIGSERIAL PRIMARY KEY,
    id_regiao INT NOT NULL,
    data_ref DATE NOT NULL,
    pr_mm DECIMAL(8, 2),
    tmax_c DECIMAL(5, 2),
    tmin_c DECIMAL(5, 2),
    eto_mm DECIMAL(8, 2),
    rh_pct DECIMAL(5, 2),
    rs DECIMAL(8, 2),
    u2_m_s DECIMAL(5, 2),
    
    CONSTRAINT fk_clima_regiao FOREIGN KEY (id_regiao) REFERENCES regiao (id_regiao)
);

-- 4. Dados Climáticos Municipais (64 Arquivos)
CREATE TABLE clima_municipal (
    id_medicao BIGSERIAL PRIMARY KEY,
    id_municipio INT NOT NULL,
    data_ref DATE NOT NULL,
    pr_mm DECIMAL(8, 2),
    tmax_c DECIMAL(5, 2),
    tmin_c DECIMAL(5, 2),
    eto_mm DECIMAL(8, 2),
    rh_pct DECIMAL(5, 2),
    rs DECIMAL(8, 2),
    u2_m_s DECIMAL(5, 2),
    
    CONSTRAINT fk_clima_municipio FOREIGN KEY (id_municipio) REFERENCES municipio (id_municipio)
);

-- Índices essenciais
CREATE INDEX idx_clima_reg_data ON clima_regional (data_ref);
CREATE INDEX idx_clima_mun_data ON clima_municipal (data_ref);