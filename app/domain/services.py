from typing import Protocol
from .entities import CustomerSummary

class BssGateway(Protocol):
    def get_customer_summary_by_phone_number(self, dni: str) -> CustomerSummary:
        ...
