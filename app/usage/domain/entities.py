from dataclasses import dataclass
from typing import Literal

Category = Literal["SOCIAL", "ENTERTAINMENT", "SYSTEM_UPDATES", "NAVIGATION_SEARCH"]

@dataclass(frozen=True)
class DataPlan:
    id: int
    line_id: int
    limit_bytes: int
    used_bytes: int
    start_at: str
    expiration_at: str
    is_active: bool

@dataclass(frozen=True)
class DataUsageBreakdown:
    used_social_bytes: int
    used_entertainment_bytes: int
    used_system_updates_bytes: int
    used_navigation_search_bytes: int

    @property
    def total(self) -> int:
        return (
            self.used_social_bytes
            + self.used_entertainment_bytes
            + self.used_system_updates_bytes
            + self.used_navigation_search_bytes
        )

@dataclass(frozen=True)
class Snapshot:
    phone_number: str
    client_full_name: str
    plan_id: int
    limit_bytes: int
    expiration_at: str
    breakdown: DataUsageBreakdown
    total_bytes: int
    percent: float
    expired: bool
