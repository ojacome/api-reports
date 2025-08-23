from dataclasses import dataclass
from typing import Literal

ProductType = Literal["FIJO", "MOVIL"]
PaymentMethod = Literal["TRANSFERENCIA", "TARJETA", "EFECTIVO", "MONEDEROS DIGITALES"]

@dataclass(frozen=True)
class CustomerSummary:
    customer_id: int
    dni: str
    name: str
    product_type: ProductType
    phone_number: str
    balance_usd: float
    balance_limit_usd: float
    minutes_remaining: int
    minutes_limit: int

@dataclass(frozen=True)
class Invoice:
    id: int
    customer_dni: int
    customer_name: str
    period: str  # 'YYYY-MM'
    total: float
    tax: float
    discount: float
    payment_method: PaymentMethod
    payment_date: str
