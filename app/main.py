from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./app_fastapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- MODELO DO BANCO DE DADOS ---
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)  # <--- NOVO CAMPO (Vulnerável: Texto plano para o TCC)

# --- ESQUEMAS DO PYDANTIC (Validação) ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # <--- Agora exigimos senha na criação

class UserLogin(BaseModel):  # <--- Novo esquema para o Login
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# --- INICIALIZAÇÃO ---
app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS ---

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica duplicidade
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Cria usuário (Atenção: Salvando senha em texto puro para fins didáticos/TCC)
    new_user = UserDB(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

# --- NOVA ROTA DE LOGIN ---
@app.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Busca o usuário pelo nome
    user = db.query(UserDB).filter(UserDB.username == user_credentials.username).first()

    # Verifica se usuário existe e se a senha bate
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password != user_credentials.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {"message": "Login realizado com sucesso!", "user_id": user.id}