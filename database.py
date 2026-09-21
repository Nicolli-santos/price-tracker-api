from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define que o banco de dados será um arquivo local chamado pricetracker.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./pricetracker.db"

# Cria a conexão com o SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para criar as tabelas
Base = declarative_base()

# Função para abrir e fechar a conexão com o banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()