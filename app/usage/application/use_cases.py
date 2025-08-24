from datetime import datetime, timezone
from usage.domain.entities import Snapshot
from usage.domain.ports import PlanRepository, UsageRepository

class GetSnapshotByPhoneNumberUseCase:
    def __init__(self, plans: PlanRepository, usage: UsageRepository):
        self._plans = plans
        self._usage = usage

    def execute(self, phone_number: str) -> Snapshot:
        plan, client_full_name = self._plans.get_active_plan_by_phone_number(phone_number)
        breakdown = self._usage.get_breakdown_by_plan_id(plan.id)
        total = breakdown.total
        limit = max(plan.limit_bytes, 0)
        pct = (total / limit * 100.0) if limit > 0 else 0.0
        now = datetime.now(timezone.utc).isoformat()
        expired = now >= plan.expiration_at
        return Snapshot(
            phone_number=phone_number,
            client_full_name=client_full_name,
            plan_id=plan.id,
            limit_bytes=limit,
            expiration_at=plan.expiration_at,
            breakdown=breakdown,
            total_bytes=total,
            percent=round(pct, 2),
            expired=expired,
        )
