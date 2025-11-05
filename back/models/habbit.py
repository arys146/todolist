from sqlalchemy import Column, String, Boolean, DateTime, Table, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from models.base import Base

DEFAULT_PRIORITY = 5

habbit_tag = Table(
    "habbit_tag",
    Base.metadata,
    Column("habbit_id", ForeignKey("habbits.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Habbit(Base):
    __tablename__ = "habbits"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    schedule: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=DEFAULT_PRIORITY)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    owner: Mapped["User"] = relationship(back_populates="habbits", lazy="joined")
    tags: Mapped[list["Tag"]] = relationship(secondary=habbit_tag, back_populates="habbits", lazy="selectin")

    trackers: Mapped[list["HabbitTracker"]] = relationship(back_populates="habbit", cascade="all, delete-orphan", lazy="raise")