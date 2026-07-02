import os

from sqlalchemy import create_engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

engine = create_engine(os.environ['DATABASE_URL'])


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
