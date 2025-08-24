from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from usage.application.use_cases import GetSnapshotByPhoneNumberUseCase
from usage.infrastructure.repos.plan_repo import SqlAlchemyPlanRepository
from usage.infrastructure.repos.usage_repo import SqlAlchemyUsageRepository

ws_router = APIRouter()

@ws_router.websocket("/ws/usage")
async def usage_ws(ws: WebSocket):
    await ws.accept()
    try:
        phone_number = ws.query_params.get("phone_number")
        if not phone_number or len(phone_number) < 5:
            await ws.send_json({
                "type": "error",
                "message": "phone_number es requerido y debe tener al menos 5 caracteres"
            })
            await ws.close(code=1008)  # Cierre intencional por dato inválido
            return

        usecase = GetSnapshotByPhoneNumberUseCase(
            plans=SqlAlchemyPlanRepository(),
            usage=SqlAlchemyUsageRepository()
        )
        snapshot = usecase.execute(phone_number)

        await ws.send_json({
            "type": "snapshot",
            "phone_number": snapshot.phone_number,
            "client_full_name": snapshot.client_full_name,
            "plan_id": snapshot.plan_id,
            "limit_bytes": snapshot.limit_bytes,
            "expiration_at": snapshot.expiration_at,
            "breakdown": {
                "used_social_bytes": snapshot.breakdown.used_social_bytes,
                "used_entertainment_bytes": snapshot.breakdown.used_entertainment_bytes,
                "used_system_updates_bytes": snapshot.breakdown.used_system_updates_bytes,
                "used_navigation_search_bytes": snapshot.breakdown.used_navigation_search_bytes,
            },
            "total_bytes": snapshot.total_bytes,
            "percent": snapshot.percent,
            "expired": snapshot.expired,
        })

        while True:
            _ = await ws.receive_text()   
            await ws.send_json({"type": "noop"})

    except WebSocketDisconnect:
        return
    except Exception as e:
        await ws.send_json({"type": "error", "message": str(e)})
        await ws.close(code=1000)  # cierre normal
