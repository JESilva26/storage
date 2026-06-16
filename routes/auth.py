from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Response,
    status
)

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy import select

from passlib.context import CryptContext

from database import get_db
from schemas import UserCreate, UserResponse

import models

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, response: Response, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    result = db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_mail = result.scalars().first()
    if existing_mail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = pwd_context.hash(
        user.password
    )

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    response.set_cookie(
        key="user_id",
        value=str(new_user.id)
    )
    
    return new_user

@router.post("/signup")
def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = UserCreate(
        username=username,
        email=email,
        password=password
    )

    created_user = create_user(
        user,
        Response(),
        db
    )

    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )

    response.set_cookie(
        key="user_id",
        value=str(created_user.id)
    )

    return response

@router.post("/login")
def login(
    db: Annotated[Session, Depends(get_db)],
    email: str = Form(...),
    password: str = Form(...),
):
    result = db.execute(
        select(models.User).where(models.User.email == email)
    )

    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )

    if not pwd_context.verify(
        password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )

    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )

    response.set_cookie(
        key="user_id",
        value=str(existing_user.id)
    )

    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(
        "/",
        status_code=status.HTTP_303_SEE_OTHER
    )

    response.delete_cookie(
        "user_id"
    )

    return response