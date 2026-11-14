import os

from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import OperationalError

url = URL.create(
    drivername="postgresql+psycopg2",
    username="naves",
    password=os.environ["POSTGRES_PASSWORD"],
    host="localhost",
    port=5432,
    database="special_coffee_br_dwgd_test",
)

engine = create_engine(url)

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