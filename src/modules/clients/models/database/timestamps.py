from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, text
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Mexico_City")

def now_tz():
    return datetime.now(TZ)

class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=now_tz,
        server_default=text("TIMEZONE('America/Mexico_City', now())")
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=now_tz,
        onupdate=now_tz,
        server_default=text("TIMEZONE('America/Mexico_City', now())")
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
