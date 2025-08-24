from sqlalchemy import select
from infrastructure.db import SessionLocal, engine
from usage.infrastructure.models_usage import UsageBase, DataUsageAccumulatorsModel
from usage.domain.entities import DataUsageBreakdown

UsageBase.metadata.create_all(bind=engine)

class SqlAlchemyUsageRepository:
    def get_breakdown_by_plan_id(self, plan_id: int) -> DataUsageBreakdown:
        with SessionLocal() as db:
            row = db.execute(
                select(DataUsageAccumulatorsModel).where(DataUsageAccumulatorsModel.plan_id == plan_id)
            ).scalars().first()
            if not row:
                return DataUsageBreakdown(
                    used_social_bytes=0,
                    used_entertainment_bytes=0,
                    used_system_updates_bytes=0,
                    used_navigation_search_bytes=0,
                )
            return DataUsageBreakdown(
                used_social_bytes=row.used_social_bytes or 0,
                used_entertainment_bytes=row.used_entertainment_bytes or 0,
                used_system_updates_bytes=row.used_system_updates_bytes or 0,
                used_navigation_search_bytes=row.used_navigation_search_bytes or 0,
            )
