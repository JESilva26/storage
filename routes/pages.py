from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db
import models

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=False)
def home(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    user_id = request.cookies.get("user_id")

    current_user = None

    if user_id:
        current_user = db.get(
            models.User,
            int(user_id)
        )

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "current_user": current_user
        }
    )
    
@router.get("/account", include_in_schema=False)
def account(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    user_id = request.cookies.get("user_id")

    if user_id is None:
        return RedirectResponse(
            "/login_page",
            status_code=status.HTTP_303_SEE_OTHER
        )

    current_user = db.get(
        models.User,
        int(user_id)
    )

    files = db.execute(
        select(models.File)
        .where(models.File.user_id == current_user.id)
    ).scalars().all()

    return templates.TemplateResponse(
        request,
        "account.html",
        {
            "current_user": current_user,
            "files": files
        }
    )
    
@router.get("/login_page", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html"
    )


@router.get("/signup_page", include_in_schema=False)
def signup_page(request: Request):
    return templates.TemplateResponse(
        request,
        "signup.html"
    )