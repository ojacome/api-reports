from sqlalchemy import select
from infrastructure.db import SessionLocal, engine
from usage.infrastructure.models_usage import UsageBase, ClientModel, PhoneLineModel, DataPlanModel
from usage.domain.entities import DataPlan

UsageBase.metadata.create_all(bind=engine)

class SqlAlchemyPlanRepository:
    def get_active_plan_by_phone_number(self, phone_number: str):
        with SessionLocal() as db:
            stmt = (
                select(DataPlanModel, ClientModel.full_name, PhoneLineModel.id)
                .join(PhoneLineModel, PhoneLineModel.id == DataPlanModel.line_id)
                .join(ClientModel, ClientModel.id == PhoneLineModel.client_id)
                .where(PhoneLineModel.phone_number == phone_number)
                .where(DataPlanModel.is_active == True)
            )
            row = db.execute(stmt).first()
            if not row:
                raise ValueError("No active data plan for this phone_number")
            plan_row, full_name, _ = row
            plan = DataPlan(
                id=plan_row.id,
                line_id=plan_row.line_id,
                limit_bytes=plan_row.limit_bytes,
                used_bytes=plan_row.used_bytes or 0,
                start_at=plan_row.start_at.isoformat() if plan_row.start_at else "",
                expiration_at=plan_row.expiration_at.isoformat() if plan_row.expiration_at else "",
                is_active=bool(plan_row.is_active),
            )
            return plan, full_name
