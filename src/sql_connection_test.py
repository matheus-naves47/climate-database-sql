from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Definir conexão com senha
string_conexao = 'postgresql+psycopg2://postgres:passwd@localhost:5432/special_coffee_br_dwgd_database'

engine = create_engine(string_conexao)

try:
    # Tenta abrir a conexão com o banco
    with engine.connect() as conexao:
        # Executa uma query básica do PostgreSQL
        resultado = conexao.execute(text("SELECT version();")).fetchone()
        
        print("✅ Conexão bem-sucedida ao PostgreSQL!")
        print(f"Informações do Servidor: {resultado[0]}")

except OperationalError as erro:
    print("❌ Falha ao conectar ao banco de dados.")
    print("Verifique se o serviço está rodando e se a senha está correta.")
    print(f"Detalhe técnico: {erro}")