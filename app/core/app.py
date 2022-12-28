from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import DomainError

app = FastAPI()


@app.exception_handler(DomainError)
def handle_domain_error(req: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
