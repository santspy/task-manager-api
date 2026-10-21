from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.database.connection import get_db
from app.models.user import UserModel
from app.schemas.user import Token, UserCreate

router = APIRouter(tags=["Autenticação"])


@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
  existing_user = (
      db.query(UserModel).filter(UserModel.username == user.username).first()
  )
  if existing_user:
    raise HTTPException(
        status_code=400, detail="Este nome de utilizador já está registado."
    )

  hashed_password = get_password_hash(user.password)
  new_user = UserModel(username=user.username, hashed_password=hashed_password)
  db.add(new_user)
  db.commit()
  return {"message": "Utilizador registado com sucesso!"}


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
  user = (
      db.query(UserModel).filter(UserModel.username == form_data.username).first()
  )

  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Utilizador ou senha incorretos",
        headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}