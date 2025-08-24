from datetime import datetime, timezone
from usage.domain.enums import DataCategory
from usage.infrastructure.repos.plan_repo import SqlAlchemyPlanRepository
from usage.infrastructure.repos.usage_repo import SqlAlchemyUsageRepository
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
        
        exp_dt = plan.expiration_at  # datetime | None
        now_dt = datetime.now(timezone.utc)
        expired = bool(exp_dt and now_dt >= (exp_dt if exp_dt.tzinfo else exp_dt.replace(tzinfo=timezone.utc)))

        return Snapshot(
            phone_number=phone_number,
            client_full_name=client_full_name,
            plan_id=plan.id,
            limit_bytes=limit,
            expiration_at=exp_dt.isoformat() if exp_dt else "", 
            breakdown=breakdown,
            total_bytes=total,
            percent=round(pct, 2),
            expired=expired,
        )

class ApplyUsageEventUseCase:
    def __init__(self, plans: SqlAlchemyPlanRepository, usage: SqlAlchemyUsageRepository):
        self.plans = plans
        self.usage = usage

    def execute(self, phone_number: str, category: DataCategory, bytes_: int, record_event: bool = False):
        plan, _ = self.plans.get_active_plan_by_phone_number(phone_number)
        if not plan:
            raise ValueError("No active data plan for this phone_number")

        self.usage.add_bytes(plan_id=plan.id, category=category, bytes_=bytes_)
        if record_event:
            self.usage.insert_usage_event(plan_id=plan.id, category=category, bytes_=bytes_)

        from usage.application.use_cases import GetSnapshotByPhoneNumberUseCase
        snap = GetSnapshotByPhoneNumberUseCase(self.plans, self.usage).execute(phone_number)
        return snap