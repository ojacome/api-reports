# 📡 Api Reports Backend

Backend desarrollado en **Python + FastAPI**, estructurado con **Arquitectura Hexagonal (Ports & Adapters) e Inyeccion de Dependencias** y desplegado mediante **Docker**.  
Provee servicios REST y WebSockets para el manejo de clientes, consumos, planes y facturación.

---

## 🔧 Requisitos

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

> ⚠️ No necesitas instalar Python ni dependencias manualmente, todo se ejecuta dentro de contenedores.

---

## ▶️ Ejecución del proyecto
 

```bash
git clone https://github.com/ojacome/api-reports.git
cd api-reports
docker compose up --build
docker compose exec -T db sh -c 'mysql -utelcox -ptelcox telcox' < db/seed_usage.sql

