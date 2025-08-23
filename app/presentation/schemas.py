from pydantic import BaseModel
from typing import List, Literal

ProductType = Literal["FIJO", "MOVIL"]
PaymentMethod = Literal["TRANSFERENCIA", "TARJETA", "EFECTIVO", "MONEDEROS DIGITALES"]

class CustomerSummaryOut(BaseModel):
    customer_id: int
    dni: str
    name: str
    product_type: ProductType
    phone_number: str
    balance_usd: float
    balance_limit_usd: float
    minutes_remaining: int
    minutes_limit: int

class InvoiceOut(BaseModel):
    id: int
    customer_dni: str
    customer_name: str
    period: str
    total: float
    tax: float
    discount: float
    payment_method: PaymentMethod
    payment_date: str

class BillingListOut(BaseModel):
    items: List[InvoiceOut]
