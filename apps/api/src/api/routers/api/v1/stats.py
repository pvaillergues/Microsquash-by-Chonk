"""Le tableau de bord du patrimoine : volumétrie par projet, type et statut.

Sert ``/api/v1/stats``.
"""

from db.accessors.test_asset import stats
from fastapi import APIRouter

from api.routers.api.v1.assets.route import SessionDep

router = APIRouter(tags=["patrimoine"])


@router.get("", operation_id="patrimoine_stats", summary="La volumétrie du patrimoine")
async def get_stats(session: SessionDep) -> dict[str, dict[str, int]]:
    """Le nombre d'actifs par projet, par type et par statut."""
    by_project, by_type, by_status = await stats(session)
    return {"by_project": by_project, "by_type": by_type, "by_status": by_status}
