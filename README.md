# – FastAPI + Hexagonal + MySQL + Docker (v4, DNI-based)
- Consultas por DNI: `/api/customers/{dni}/summary` y `/api/customers/{dni}/billing`
- Campos extra: product_type (FIJO|MOVIL), phone_number, balance_limit_usd, minutes_limit
- BSS mock: `/bss/customers/by-dni/{dni}/summary`

Run:

  docker compose build --no-cache 
  docker compose up -d

  docker compose down -v        # <- elimina contenedores y volúmenes (incluye dbdata)

  migraciones
  docker compose exec -T db sh -c 'mysql -utelcox -ptelcox telcox' < db/seed_usage.sql