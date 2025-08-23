from typing import List
from enum import Enum as PyEnum
from sqlalchemy import select
from infrastructure.db import SessionLocal
from infrastructure.models import InvoiceModel
from domain.entities import Invoice

class MysqlBillingRepository:
    def __init__(self):
        self._Session = SessionLocal

    def list_invoices_by_dni(self, dni: str) -> List[Invoice]:
        with self._Session() as db:
            rows = (
                db.execute(
                    select(InvoiceModel)
                    .where(InvoiceModel.customer_dni == dni)
                    .order_by(InvoiceModel.period.desc(), InvoiceModel.id.desc())
                )
                .scalars()
                .all()
            )
            invoices: List[Invoice] = []
            for row in rows:
                method = row.payment_method.value if isinstance(row.payment_method, PyEnum) else str(row.payment_method)
                paid_at = row.payment_date.isoformat(timespec="seconds") if row.payment_date else ""
                invoices.append(
                    Invoice(
                        id=row.id,
                        customer_dni=row.customer_dni,
                        customer_name=row.customer_name,
                        period=row.period,
                        total=row.total,
                        tax=row.tax,
                        discount=row.discount,
                        payment_method=method,
                        payment_date=paid_at,
                    )
                )
            return invoices
