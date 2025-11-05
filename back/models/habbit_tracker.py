from datetime import date, datetime
from sqlalchemy import String,  func, ForeignKey, Integer, UniqueConstraint, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class HabbitTracker(Base):
    __tablename__ = "habbit_tracker"

    id: Mapped[int] = mapped_column(primary_key=True)
    habbit_id: Mapped[int] = mapped_column(ForeignKey("habbits.id", ondelete="CASCADE"), index=True)
    logical_date: Mapped[date] = mapped_column(Date, index=True)   
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)  
    habbit: Mapped["Habbit"] = relationship(back_populates="trackers", lazy="raise")

    __table_args__ = (
        UniqueConstraint("habbit_id", "logical_date", name="uq_habbit_day"),
    )