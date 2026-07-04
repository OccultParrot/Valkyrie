from sqlmodel import SQLModel, Field, BIGINT, Column, DateTime

class Announcement(SQLModel):
    message: str