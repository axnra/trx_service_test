from fastapi import FastAPI
from app.routes import address

app = FastAPI(title="Tron wallet info service")

# Register address-related routes
app.include_router(address.router)
