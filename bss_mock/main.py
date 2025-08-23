from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mock BSS (DNI-based)", version="2.0.0")

BSS_DATA = {
  "0912345678": {
    "customer_id": 1,
    "dni": "0912345678",
    "name": "Alice R.",
    "product_type": "MOVIL",
    "phone_number": "+593991234567",
    "balance_usd": 12.75,
    "balance_limit_usd": 30.0,
    "minutes_remaining": 320,
    "minutes_limit": 600
  },
  "0923456789": {
    "customer_id": 2,
    "dni": "0923456789",
    "name": "Bruno S.",
    "product_type": "FIJO",
    "phone_number": "+59342223344",
    "balance_usd": 3.5,
    "balance_limit_usd": 20.0,
    "minutes_remaining": 45,
    "minutes_limit": 200
  },
  "0934567890": {
    "customer_id": 3,
    "dni": "0934567890",
    "name": "Carla M.",
    "product_type": "MOVIL",
    "phone_number": "+593987654321",
    "balance_usd": 0.0,
    "balance_limit_usd": 10.0,
    "minutes_remaining": 0,
    "minutes_limit": 100
  }
}

@app.get("/bss/customers/by-dni/{dni}/summary")
def get_summary_by_dni(dni: str):
    if dni not in BSS_DATA:
        raise HTTPException(status_code=404, detail="Customer not found in BSS")
    return BSS_DATA[dni]
