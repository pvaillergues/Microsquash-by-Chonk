"""L'import CSV du patrimoine : ajoute les actifs, met à jour ceux déjà référencés.

Sert ``/api/v1/assets/import``.
"""

import csv
import io

from db.accessors.test_asset import get_asset, upsert_asset
from fastapi import APIRouter, HTTPException, UploadFile

from api.routers.api.v1.assets.route import AssetCreate, SessionDep

router = APIRouter(tags=["patrimoine"])

VALID_TYPES = {"cas_de_test", "exigence", "campagne"}
VALID_STATUSES = {"brouillon", "relu", "execute", "archive"}


def _row_to_create(row: dict[str, str]) -> AssetCreate:
    reference = (row.get("reference") or "").strip()
    name = (row.get("name") or "").strip()
    project = (row.get("project") or "").strip()
    type_ = (row.get("type") or "cas_de_test").strip() or "cas_de_test"
    status = (row.get("status") or "brouillon").strip() or "brouillon"
    if not reference or not name:
        raise ValueError("reference et name sont obligatoires")
    if type_ not in VALID_TYPES:
        raise ValueError(f"type invalide : {type_}")
    if status not in VALID_STATUSES:
        raise ValueError(f"statut invalide : {status}")
    return AssetCreate(
        reference=reference,
        name=name,
        project=project,
        type=type_,
        status=status,
        owner=(row.get("owner") or "").strip() or None,
        description=(row.get("description") or "").strip() or None,
    )


@router.post("", operation_id="import_assets", summary="Importer des actifs depuis un CSV")
async def import_assets(session: SessionDep, file: UploadFile) -> dict[str, object]:
    """Un CSV (séparateur point-virgule ou virgule) avec les colonnes reference, name, project,
    type, status, owner, description. Les références déjà présentes sont mises à jour, les
    nouvelles créées."""
    raw = await file.read()
    text = raw.decode("utf-8-sig")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ";"
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    created = 0
    updated = 0
    errors: list[str] = []
    for line_number, row in enumerate(reader, start=2):
        try:
            asset = _row_to_create(row)
        except ValueError as error:
            errors.append(f"ligne {line_number}: {error}")
            continue
        existing = await get_asset(session, asset.reference)
        await upsert_asset(session, asset, update=existing is not None)
        if existing is None:
            created += 1
        else:
            updated += 1
    if not (created or updated) and not errors:
        raise HTTPException(status_code=400, detail="aucune ligne lisible dans le fichier")
    return {"created": created, "updated": updated, "errors": errors}
