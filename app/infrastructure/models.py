import datetime
from enum import Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Enum as SAEnum, DateTime, func

Base = declarative_base()

class PaymentMethodEnum(str, Enum):
    TRANSFERENCIA = "TRANSFERENCIA"
    TARJETA = "TARJETA"
    EFECTIVO = "EFECTIVO"
    MONEDEROS_DIGITALES = "MONEDEROS DIGITALES"

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_dni: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    period: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    total: Mapped[float] = mapped_column(Float, nullable=False)
    tax: Mapped[float] = mapped_column(Float, nullable=False)
    discount: Mapped[float] = mapped_column(Float, nullable=False)

    payment_method: Mapped[PaymentMethodEnum] = mapped_column(
        SAEnum(PaymentMethodEnum, name="payment_method_enum"),  # ENUM nativo en MySQL
        nullable=False
    )
    payment_date: Mapped[datetime] = mapped_column(
        DateTime(),                         
        nullable=False,
        server_default=func.now()          
    )
