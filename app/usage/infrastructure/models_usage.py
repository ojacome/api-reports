from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, BigInteger, Boolean, DateTime, Enum as SAEnum, ForeignKey, func

UsageBase = declarative_base()

class ClientModel(UsageBase):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dni: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=True)

class PhoneLineModel(UsageBase):
    __tablename__ = "phone_lines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    product_type: Mapped[str] = mapped_column(SAEnum("FIJO", "MOVIL", name="product_type_enum"), nullable=False)

class DataPlanModel(UsageBase):
    __tablename__ = "data_plans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    line_id: Mapped[int] = mapped_column(Integer, ForeignKey("phone_lines.id", ondelete="CASCADE"), nullable=False, index=True)
    limit_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    used_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    start_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False, server_default=func.now())
    expiration_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class DataUsageAccumulatorsModel(UsageBase):
    __tablename__ = "data_usage_accumulators"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("data_plans.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    used_social_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    used_entertainment_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    used_system_updates_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    used_navigation_search_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False, server_default=func.now())

class UsageEventModel(UsageBase):
    __tablename__ = "usage_events"
    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    line_id: Mapped[int] = mapped_column(Integer, ForeignKey("phone_lines.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("data_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(SAEnum("SOCIAL","ENTERTAINMENT","SYSTEM_UPDATES","NAVIGATION_SEARCH", name="usage_category_enum"), nullable=False)
    bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    timestamp_event: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    ingested_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False, server_default=func.now())
