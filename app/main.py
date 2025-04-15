from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import address

app = FastAPI(
    title="Tron Wallet Info Service",
    version="0.1.0",
    description="Fetch and store TRON wallet metrics from the blockchain.",
    contact={
        "name": "Evgeny",
        "url": "https://github.com/axnra"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

# Register address-related routes
app.include_router(address.router)
