from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine

from routes.auth import router as auth_router
from routes.files import router as files_router
from routes.pages import router as pages_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.include_router(files_router)
app.include_router(pages_router)


@app.exception_handler(StarletteHTTPException)
def custom_exception(
    request: Request,
    exception: StarletteHTTPException
):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again"
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code
    )