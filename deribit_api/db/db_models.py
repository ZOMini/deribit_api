import datetime
import uuid

from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP, UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column
)
from sqlalchemy.sql import func
from typing_extensions import Annotated


class Base(DeclarativeBase):
    pass


uuidpk = Annotated[uuid.UUID, mapped_column(
    UUID(as_uuid=True),
    default=uuid.uuid4,
    primary_key=True,
    unique=True,
    nullable=False)]
timestamp_int = Annotated[datetime.datetime, mapped_column(
    TIMESTAMP(timezone=False),
    server_default=func.current_timestamp())]
ticker_str = Annotated[str, mapped_column(
    ENUM('BTC', 'ETH', name='tickerenum'))]
value_float = Annotated[float, mapped_column(
    nullable=False)]


class Currency(MappedAsDataclass, Base):
    __tablename__ = 'currencies'

    id: Mapped[uuidpk] = mapped_column(init=False)
    timestamp: Mapped[timestamp_int] = mapped_column(init=False)
    ticker: Mapped[ticker_str]
    value: Mapped[value_float]

    def __repr__(self) -> str:
        return str(self.id)
