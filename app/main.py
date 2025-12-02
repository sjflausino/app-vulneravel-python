from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import hashlib 

DATABASE_PASSWORD = "admin_password_123" 
SQLALCHEMY_DATABASE_URL = "sqlite:///./app_fastapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):  
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_password_complex(password: str):
    if len(password) > 8:
        if "a" in password:
            if "1" in password:
                return True
            else:
                return False
        elif "b" in password:
            if "2" in password:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Tentando criar usuário: {user.username}") 

    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
         raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hashlib.md5(user.password.encode()).hexdigest()
    
    new_user = UserDB(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

@app.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    query = text(f"SELECT * FROM users WHERE username = '{user_credentials.username}'")
    result = db.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_password = result[3]
    input_hashed = hashlib.md5(user_credentials.password.encode()).hexdigest()

    if stored_password != input_hashed:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {"message": "Login realizado com sucesso!", "user_id": result[0]}

@app.get("/debug_info")
def debug():
    try:
        x = 1 / 0
    except Exception:
        pass 
    return {"status": "ok"}