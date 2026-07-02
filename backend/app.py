import dotenv
from fastapi import FastAPI

from middleware.logging import log_requests
from routes.users import router as users_router

dotenv.load_dotenv()

app = FastAPI()

app.middleware("http")(log_requests)

app.include_router(users_router, prefix="/api")
