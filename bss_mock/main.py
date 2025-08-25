from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mock BSS", version="2.0.0")

BSS_DATA = {
  "0969786985": {
    "customer_id": 1,
    "dni": "0929668846",
    "name": "Jesus Jacome",
    "product_type": "MOVIL",
    "phone_number": "0969786985",
    "balance_usd": 12.75,
    "balance_limit_usd": 30.0,
    "minutes_remaining": 320,
    "minutes_limit": 600
  },
  "0923456789": {
    "customer_id": 2,
    "dni": "0923456781",
    "name": "Bruno S.",
    "product_type": "FIJO",
    "phone_number": "0923456789",
    "balance_usd": 3.5,
    "balance_limit_usd": 20.0,
    "minutes_remaining": 45,
    "minutes_limit": 200
  },
  "0934567890": {
    "customer_id": 3,
    "dni": "0934567893",
    "name": "Carla M.",
    "product_type": "MOVIL",
    "phone_number": "0934567890",
    "balance_usd": 0.0,
    "balance_limit_usd": 10.0,
    "minutes_remaining": 0,
    "minutes_limit": 100
  }
}

@app.get("/bss/customers/by-phone-number/{phone_number}/summary")
def get_summary_by_phone_number(phone_number: str):
    if phone_number not in BSS_DATA:
        raise HTTPException(status_code=404, detail="Customer not found in BSS")
    return BSS_DATA[phone_number]
