"""L'export CSV du patrimoine : les mêmes filtres que l'inventaire.

Sert ``/api/v1/assets/export``.
"""

import csv
import io

from db.accessors.test_asset import list_assets
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from api.routers.api.v1.assets.route import SessionDep, SearchDep

router = APIRouter(tags=["patrimoine"])

COLUMNS = ("reference", "name", "project", "type", "status", "owner", "description")


@router.get("", operation_id="export_assets", summary="Exporter le patrimoine filtré en CSV")
async def export_assets(
    session: SessionDep,
    q: SearchDep = None,
    project: SearchDep = None,
    type: SearchDep = None,
    status: SearchDep = None,
) -> StreamingResponse:
    """Les actifs correspondant aux filtres, en CSV (point-virgule, pour Excel fr)."""
    items = await list_assets(session, q=q, project=project, type=type, status=status)
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(COLUMNS)
    for item in items:
        writer.writerow([getattr(item, column) or "" for column in COLUMNS])
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="patrimoine-test.csv"'},
    )
