from sqlalchemy import select, update
from infrastructure.db import SessionLocal
from usage.infrastructure.models_usage import (
    DataUsageAccumulatorsModel,
    DataPlanModel,
    UsageEventModel,
)
from usage.domain.enums import DataCategory
from usage.domain.entities import DataUsageBreakdown 
from usage.domain.ports import UsageRepository


_COL_BY_CATEGORY = {
    DataCategory.SOCIAL: "used_social_bytes",
    DataCategory.ENTERTAINMENT: "used_entertainment_bytes",
    DataCategory.SYSTEM_UPDATES: "used_system_updates_bytes",
    DataCategory.NAVIGATION_SEARCH: "used_navigation_search_bytes",
}


class SqlAlchemyUsageRepository(UsageRepository):
    def __init__(self, SessionFactory=SessionLocal) -> None:
        self._Session = SessionFactory

    def add_bytes(self, plan_id: int, category: DataCategory, bytes_: int) -> None:
        if bytes_ <= 0:
            return

        col = _COL_BY_CATEGORY.get(category)
        if not col:
            raise ValueError(f"Unknown category: {category}")

        with self._Session.begin() as db:
            acc = db.execute(
                select(DataUsageAccumulatorsModel).where(
                    DataUsageAccumulatorsModel.plan_id == plan_id
                )
            ).scalar_one_or_none()
            if acc is None:
                acc = DataUsageAccumulatorsModel(plan_id=plan_id)
                db.add(acc)
                db.flush()  # crea la fila

            db.execute(
                update(DataUsageAccumulatorsModel)
                .where(DataUsageAccumulatorsModel.plan_id == plan_id)
                .values({col: getattr(DataUsageAccumulatorsModel, col) + bytes_})
            )

            db.execute(
                update(DataPlanModel)
                .where(DataPlanModel.id == plan_id)
                .values(used_bytes=DataPlanModel.used_bytes + bytes_)
            )

    def insert_usage_event(self, plan_id: int, category: DataCategory, bytes_: int) -> None:
        with self._Session.begin() as db:
            ev = UsageEventModel(plan_id=plan_id, category=category.value, bytes=bytes_)
            db.add(ev)

    def get_breakdown_by_plan_id(self, plan_id: int) -> DataUsageBreakdown:
        with self._Session() as db:
            acc = db.execute(
                select(DataUsageAccumulatorsModel).where(
                    DataUsageAccumulatorsModel.plan_id == plan_id
                )
            ).scalar_one_or_none()

            if acc is None:
                return DataUsageBreakdown(
                    used_social_bytes=0,
                    used_entertainment_bytes=0,
                    used_system_updates_bytes=0,
                    used_navigation_search_bytes=0,
                )

            return DataUsageBreakdown(
                used_social_bytes=acc.used_social_bytes or 0,
                used_entertainment_bytes=acc.used_entertainment_bytes or 0,
                used_system_updates_bytes=acc.used_system_updates_bytes or 0,
                used_navigation_search_bytes=acc.used_navigation_search_bytes or 0,
            )
