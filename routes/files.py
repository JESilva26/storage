from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile
)

from fastapi.responses import (
    FileResponse,
    RedirectResponse
)

from sqlalchemy.orm import Session

from database import get_db

import models

import os
import shutil

router = APIRouter()

@router.post("/upload")
def upload_file(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
):
    user_id = request.cookies.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )

    upload_dir = f"uploads/{user_id}"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    filepath = f"{upload_dir}/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    new_file = models.File(
        user_id=int(user_id),
        filename=file.filename,
        filepath=filepath
    )

    db.add(new_file)
    db.commit()

    return RedirectResponse(
        url="/account",
        status_code=303
    )
    
@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    user_id = request.cookies.get("user_id")

    file = db.get(models.File, file_id)

    if file is None:
        raise HTTPException(404)

    if file.user_id != int(user_id):
        raise HTTPException(403)

    return FileResponse(
        path=file.filepath,
        filename=file.filename
    )
    
@router.post("/delete/{file_id}")
def delete_file(
    file_id: int,
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    user_id = request.cookies.get("user_id")

    file = db.get(models.File, file_id)

    if file is None:
        raise HTTPException(404)

    if file.user_id != int(user_id):
        raise HTTPException(403)

    if os.path.exists(file.filepath):
        os.remove(file.filepath)

    db.delete(file)
    db.commit()

    return RedirectResponse(
        url="/account",
        status_code=303
    )