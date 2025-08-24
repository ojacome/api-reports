from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conint, constr
from usage.domain.enums import DataCategory
from usage.application.use_cases import ApplyUsageEventUseCase, GetSnapshotByPhoneNumberUseCase
from usage.infrastructure.repos.plan_repo import SqlAlchemyPlanRepository
from usage.infrastructure.repos.usage_repo import SqlAlchemyUsageRepository
from presentation.ws_manager import manager

dev_router = APIRouter(prefix="/api/dev", tags=["dev"])

class UsageEventIn(BaseModel):
    phone_number: constr(min_length=5)
    category: DataCategory
    bytes: conint(strict=True, ge=1)
    record_event: bool = False

@dev_router.post("/usage-event", status_code=202)
def post_usage_event(payload: UsageEventIn):
    plans = SqlAlchemyPlanRepository()
    usage = SqlAlchemyUsageRepository()
    try:
        snap = ApplyUsageEventUseCase(plans, usage).execute(
            phone_number=payload.phone_number,
            category=payload.category,
            bytes_=payload.bytes,
            record_event=payload.record_event
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # (la estructura debe calzar con lo que envías en el WS)
    snapshot_payload = {
        "type": "snapshot",
        "phone_number": snap.phone_number,
        "client_full_name": snap.client_full_name,
        "plan_id": snap.plan_id,
        "limit_bytes": snap.limit_bytes,
        "expiration_at": snap.expiration_at,
        "breakdown": {
            "used_social_bytes": snap.breakdown.used_social_bytes,
            "used_entertainment_bytes": snap.breakdown.used_entertainment_bytes,
            "used_system_updates_bytes": snap.breakdown.used_system_updates_bytes,
            "used_navigation_search_bytes": snap.breakdown.used_navigation_search_bytes,
        },
        "total_bytes": snap.total_bytes,
        "percent": snap.percent,
        "expired": snap.expired,
    }
    # TODO investigar, no await en contexto sync 
    import anyio
    anyio.from_thread.run(manager.broadcast, payload.phone_number, snapshot_payload)

    return {"ok": True, "snapshot": snapshot_payload}
