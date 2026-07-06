from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.sql.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    # The plan amount (80 / 150 / 1000) of the key the user activated.
    amount: Mapped[int | None] = mapped_column(nullable=True, default=None)
    # The 8-digit account id taken from the activation key (kept as text to
    # preserve any leading zeros).
    account_id: Mapped[str | None] = mapped_column(nullable=True, default=None)
    # True once the user has started their trading session (single use).
    session_used: Mapped[bool] = mapped_column(nullable=False, default=False)
