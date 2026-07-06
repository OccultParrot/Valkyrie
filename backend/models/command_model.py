from sqlmodel import SQLModel, Field, BIGINT, Column, DateTime


class Announcement(SQLModel):
    message: str

class DirectMessage(SQLModel):
    message: str
    target: int