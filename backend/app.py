import dotenv
from fastapi import FastAPI

from middleware.logging import log_requests
from routes import router

dotenv.load_dotenv()

app = FastAPI()

app.middleware("http")(log_requests)

app.include_router(router, prefix="/api")
