from typing import List, Protocol
from .entities import Invoice

class BillingRepository(Protocol):
    def list_invoices_by_phone_number(self, phone_number: str) -> List[Invoice]:
        ...
