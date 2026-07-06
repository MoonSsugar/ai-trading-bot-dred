from uuid import UUID
from uuid_utils.compat import uuid7

from sqlalchemy.orm import Mapped, mapped_column


from app.sql.models.base import Base, TimestampMixin


class Key(Base, TimestampMixin):
    __tablename__ = "keys"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    key: Mapped[str] = mapped_column(unique=True, nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    is_used: Mapped[bool] = mapped_column(nullable=False, default=False)
