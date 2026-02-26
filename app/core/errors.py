from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


def http_error(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)


# Example exception handler (optional)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
