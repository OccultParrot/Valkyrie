import dotenv
from fastapi import FastAPI

from routes.users import router as users_router
from middleware.logging import log_requests

dotenv.load_dotenv()

app = FastAPI()

app.middleware("http")(log_requests)

app.include_router(users_router, prefix="/api")
