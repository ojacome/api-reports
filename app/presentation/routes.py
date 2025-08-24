from fastapi import APIRouter, Depends, HTTPException
from application.use_cases import GetCustomerSummaryByPhoneNumberUseCase, GetBillingHistoryByPhoneNumberUseCase
from presentation.schemas import CustomerSummaryOut, BillingListOut, InvoiceOut
from container import Container

router = APIRouter()

def get_container() -> Container:
    return Container()

@router.get("/customers/{phone_number}/summary", response_model=CustomerSummaryOut)
def get_customer_summary(phone_number: str, container: Container = Depends(get_container)):
    usecase: GetCustomerSummaryByPhoneNumberUseCase = container.summary_usecase()
    try:
        summary = usecase.execute(phone_number)
        return CustomerSummaryOut(**summary.__dict__)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error contacting BSS: {e}")

@router.get("/customers/{phone_number}/billing", response_model=BillingListOut)
def get_billing(phone_number: str, container: Container = Depends(get_container)):
    usecase: GetBillingHistoryByPhoneNumberUseCase = container.billing_usecase()
    invoices = usecase.execute(phone_number)
    return BillingListOut(items=[InvoiceOut(**inv.__dict__) for inv in invoices])
