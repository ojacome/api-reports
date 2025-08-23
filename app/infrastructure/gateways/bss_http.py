import httpx
from config import settings
from domain.entities import CustomerSummary

class BssHttpGateway:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.BSS_BASE_URL
        self._client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_customer_summary_by_dni(self, dni: str) -> CustomerSummary:
        r = self._client.get(f"/bss/customers/by-dni/{dni}/summary")
        r.raise_for_status()
        data = r.json()
        return CustomerSummary(
            customer_id=int(data["customer_id"]),
            dni=data["dni"],
            name=data["name"],
            product_type=data["product_type"],
            phone_number=data["phone_number"],
            balance_usd=float(data["balance_usd"]),
            balance_limit_usd=float(data["balance_limit_usd"]),
            minutes_remaining=int(data["minutes_remaining"]),
            minutes_limit=int(data["minutes_limit"]),
        )
