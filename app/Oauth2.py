from datetime import datetime, timedelta
import json
from typing import List
from jose import JWTError, jwt
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire_time})
    jwt_encoded = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.tokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not verify credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    tokens = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == tokens.id).first()

    return user.__dict__
