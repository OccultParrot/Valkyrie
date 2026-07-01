from sqlmodel import SQLModel, Field, BIGINT


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    discord_id: int = Field(nullable=False, sa_type=BIGINT)
    steam_id: int = Field(nullable=False, sa_type=BIGINT)
    steam_name: str | None = Field(default=None, nullable=True)
    balance: int = Field(default=0)
