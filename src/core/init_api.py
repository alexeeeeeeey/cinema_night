from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

app = FastAPI()


@app.exception_handler(NoResultFound)
async def no_result_found_handler(request: Request, exc: NoResultFound):
    raise HTTPException(status_code=404, detail="Not Found")


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    if hasattr(exc.orig, "pgcode") and exc.orig.pgcode == "23503":
        raise HTTPException(
            status_code=400, detail="Invalid reference: related object does not exist"
        )

    raise HTTPException(status_code=409, detail="Conflict")
