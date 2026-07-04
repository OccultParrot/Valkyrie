from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, BIGINT, Column, DateTime


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    discord_id: int = Field(nullable=False, sa_type=BIGINT)
    steam_id: int = Field(nullable=False, sa_type=BIGINT)
    steam_name: str | None = Field(default=None, nullable=True)
    balance: int = Field(default=0)
    last_daily: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class UserUpdate(SQLModel):
    discord_id: int | None = None
    steam_id: int | None = None
    steam_name: str | None = None
    balance: int | None = None
