from typing import List
from domain.repositories import BillingRepository
from domain.services import BssGateway
from domain.entities import CustomerSummary, Invoice

class GetCustomerSummaryByPhoneNumberUseCase:
    def __init__(self, bss_gateway: BssGateway):
        self._bss = bss_gateway

    def execute(self, phone_number: str) -> CustomerSummary:
        return self._bss.get_customer_summary_by_phone_number(phone_number)

class GetBillingHistoryByPhoneNumberUseCase:
    def __init__(self, repo: BillingRepository):
        self._repo = repo

    def execute(self, phone_number: str) -> List[Invoice]:
        return self._repo.list_invoices_by_phone_number(phone_number)
