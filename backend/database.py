import os
from typing import Annotated

import dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

dotenv.load_dotenv()

engine = create_engine(os.environ['DATABASE_URL'])


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
