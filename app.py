from datetime import datetime, timedelta
import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Configurações de Segurança (JWT)
SECRET_KEY = "sua_chave_secreta_super_segura_aqui"  # Em produção, usar variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração do Banco de Dados
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "tasks_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Utilitários de Criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- MODELOS DO BANCO DE DADOS ---
class UserModel(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  tasks = relationship("TaskModel", back_populates="owner")


class TaskModel(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  description = Column(String, nullable=True)
  status = Column(String, default="Pendente")
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer, ForeignKey("users.id"))

  owner = relationship("UserModel", back_populates="tasks")


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API - Secured", version="2.0", description="API com JWT"
)


# --- SCHEMAS PYDANTIC ---
class UserCreate(BaseModel):
  username: str
  password: str


class TaskCreate(BaseModel):
  title: str
  description: str | None = None


class Token(BaseModel):
  access_token: str
  token_type: str


# --- FUNÇÕES AUXILIARES ---
def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (
      expires_delta
      or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Não foi possível validar as credenciais",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  db = SessionLocal()
  user = db.query(UserModel).filter(UserModel.username == username).first()
  db.close()
  if user is None:
    raise credentials_exception
  return user


# --- ROTAS DA API ---
@app.get("/")
def read_root():
  return {"message": "Bem-vindo à API Segura de Gestão de Tarefas!"}


@app.post("/register", status_code=201)
def register_user(user: UserCreate):
  db = SessionLocal()
  existing_user = (
      db.query(UserModel).filter(UserModel.username == user.username).first()
  )
  if existing_user:
    db.close()
    raise HTTPException(
        status_code=400, detail="Este nome de utilizador já está registado."
    )

  hashed_password = get_password_hash(user.password)
  new_user = UserModel(username=user.username, hashed_password=hashed_password)
  db.add(new_user)
  db.commit()
  db.close()
  return {"message": "Utilizador registado com sucesso!"}


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  db = SessionLocal()
  user = (
      db.query(UserModel).filter(UserModel.username == form_data.username).first()
  )
  db.close()

  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Utilizador ou senha incorretos",
        headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}


@app.post("/tasks/", status_code=201)
def create_task(task: TaskCreate, current_user: UserModel = Depends(get_current_user)):
  db = SessionLocal()
  db_task = TaskModel(
      title=task.title, description=task.description, user_id=current_user.id
  )
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  db.close()
  return {
      "message": "Tarefa criada com sucesso!",
      "task_id": db_task.id,
      "title": db_task.title,
  }


@app.get("/tasks/")
def list_tasks(current_user: UserModel = Depends(get_current_user)):
  db = SessionLocal()
  tasks = db.query(TaskModel).filter(TaskModel.user_id == current_user.id).all()
  db.close()
  return tasks