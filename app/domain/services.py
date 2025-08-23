from typing import Protocol
from .entities import CustomerSummary

class BssGateway(Protocol):
    def get_customer_summary_by_dni(self, dni: str) -> CustomerSummary:
        ...
