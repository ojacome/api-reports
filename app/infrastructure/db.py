# app/infrastructure/db.py
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from config import settings
from infrastructure.models import Base, InvoiceModel, PaymentMethodEnum

engine = create_engine(settings.DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def seed_initial_data():
    """Seed some invoice rows if table is empty (nueva estructura)."""
    # Crea tablas si no existen (no hace ALTER)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        exists = db.execute(select(InvoiceModel.id).limit(1)).first()
        if exists:
            return

        invoices = [
            # DNI 0912345678 (Alice R.)
            InvoiceModel(
                customer_dni="0912345678",
                customer_name="Alice R.",
                period="2025-05",
                total=25.00,
                tax=3.00,
                discount=0.00,
                payment_method=PaymentMethodEnum.TARJETA,
                payment_date=datetime(2025, 5, 25, 14, 30, 0),
            ),
            InvoiceModel(
                customer_dni="0912345678",
                customer_name="Alice R.",
                period="2025-06",
                total=30.00,
                tax=3.60,
                discount=2.00,
                payment_method=PaymentMethodEnum.TRANSFERENCIA,
                payment_date=datetime(2025, 6, 28, 9, 15, 0),
            ),
            # DNI 0923456789 (Bruno S.)
            InvoiceModel(
                customer_dni="0923456789",
                customer_name="Bruno S.",
                period="2025-06",
                total=20.00,
                tax=2.40,
                discount=0.00,
                payment_method=PaymentMethodEnum.EFECTIVO,
                payment_date=datetime(2025, 6, 20, 18, 5, 0),
            ),
        ]

        db.add_all(invoices)
        db.commit()
 