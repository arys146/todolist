from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from .task import task_tag
from .habbit import habbit_tag

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),  index=True)
    owner: Mapped["User"] = relationship(back_populates="tags", lazy="joined")
    tasks: Mapped[list["Task"]] = relationship(secondary=task_tag, back_populates="tags", lazy="raise")
    habbits: Mapped[list["Habbit"]] = relationship(secondary=habbit_tag, back_populates="tags", lazy="raise")