from datetime import datetime, time
from sqlalchemy import String, Time, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    day_start_offset: Mapped[time] = mapped_column(Time, nullable=False, default=time(0,0,0))
    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(back_populates="owner", cascade="all, delete-orphan", lazy="selectin")
    habbits: Mapped[list["Habbit"]] = relationship(back_populates="owner", cascade="all, delete-orphan", lazy="selectin")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="owner", cascade="all, delete-orphan", lazy="raise")