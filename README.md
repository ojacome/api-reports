# – FastAPI + Hexagonal + MySQL + Docker (v4, DNI-based)
- Consultas por DNI: `/api/customers/{dni}/summary` y `/api/customers/{dni}/billing`
- Campos extra: product_type (FIJO|MOVIL), phone_number, balance_limit_usd, minutes_limit
- BSS mock: `/bss/customers/by-dni/{dni}/summary`

Run:

  docker compose build --no-cache 
  docker compose up

  docker compose down -v        # <- elimina contenedores y volúmenes (incluye dbdata)