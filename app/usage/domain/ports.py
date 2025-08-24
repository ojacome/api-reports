from .entities import DataPlan, DataUsageBreakdown

class PlanRepository:
    def get_active_plan_by_phone_number(self, phone_number: str) -> tuple[DataPlan, str]:
        raise NotImplementedError

class UsageRepository:
    def get_breakdown_by_plan_id(self, plan_id: int) -> DataUsageBreakdown:
        raise NotImplementedError
