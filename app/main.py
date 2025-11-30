from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- CONFIGURAÇÃO DO BANCO DE DADOS (SQLite) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./app_fastapi.db"

# connect_args={"check_same_thread": False} é necessário apenas para SQLite no FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- MODELO DO BANCO DE DADOS (Tabela) ---
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)

# --- ESQUEMAS DO PYDANTIC (Validação de Dados) ---
# Isso define o que a API espera receber e devolver
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# --- INICIALIZAÇÃO DO APP ---
app = FastAPI()

# Cria as tabelas no banco automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

# --- DEPENDÊNCIA (Gerenciamento de Sessão) ---
# Garante que o banco abre e fecha a conexão a cada requisição (evita Database Locked)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS ---

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se usuário já existe
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Cria novo usuário
    new_user = UserDB(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users