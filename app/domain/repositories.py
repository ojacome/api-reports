from typing import List, Protocol
from .entities import Invoice

class BillingRepository(Protocol):
    def list_invoices_by_dni(self, dni: str) -> List[Invoice]:
        ...
