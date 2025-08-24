# usage/infrastructure/repos/plan_repo.py
from usage.domain.ports import PlanRepository
from sqlalchemy import select
from infrastructure.db import SessionLocal
from usage.infrastructure.models_usage import DataPlanModel, PhoneLineModel, ClientModel
from usage.domain.entities import DataPlan

class SqlAlchemyPlanRepository(PlanRepository):
    def get_active_plan_by_phone_number(self, phone_number: str) -> tuple[DataPlan, str]:
        with SessionLocal() as db:
            row = db.execute(
                select(DataPlanModel, ClientModel.full_name)
                .join(PhoneLineModel, PhoneLineModel.id == DataPlanModel.line_id)
                .join(ClientModel, ClientModel.id == PhoneLineModel.client_id)
                .where(PhoneLineModel.phone_number == phone_number, DataPlanModel.is_active.is_(True))
            ).first()

            if not row:
                raise ValueError("No active data plan for this phone_number")

            plan_row, full_name = row
            plan = DataPlan(
                id=plan_row.id,
                line_id=plan_row.line_id,
                limit_bytes=plan_row.limit_bytes,
                used_bytes=plan_row.used_bytes or 0,
                start_at=plan_row.start_at,          
                expiration_at=plan_row.expiration_at, 
                is_active=bool(plan_row.is_active),
            )
            return plan, full_name
