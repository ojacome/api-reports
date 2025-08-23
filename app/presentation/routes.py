from fastapi import APIRouter, Depends, HTTPException
from application.use_cases import GetCustomerSummaryByDniUseCase, GetBillingHistoryByDniUseCase
from presentation.schemas import CustomerSummaryOut, BillingListOut, InvoiceOut
from container import Container

router = APIRouter()

def get_container() -> Container:
    return Container()

@router.get("/customers/{dni}/summary", response_model=CustomerSummaryOut)
def get_customer_summary(dni: str, container: Container = Depends(get_container)):
    usecase: GetCustomerSummaryByDniUseCase = container.summary_usecase()
    try:
        summary = usecase.execute(dni)
        return CustomerSummaryOut(**summary.__dict__)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error contacting BSS: {e}")

@router.get("/customers/{dni}/billing", response_model=BillingListOut)
def get_billing(dni: str, container: Container = Depends(get_container)):
    usecase: GetBillingHistoryByDniUseCase = container.billing_usecase()
    invoices = usecase.execute(dni)
    return BillingListOut(items=[InvoiceOut(**inv.__dict__) for inv in invoices])
