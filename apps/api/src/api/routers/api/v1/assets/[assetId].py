"""Un actif de test : sa fiche, son cycle de vie, sa suppression.

Sert ``/api/v1/assets/{assetId}``.
"""

from typing import Annotated

from db.accessors.test_asset import delete_asset, read_asset, update_asset
from fastapi import APIRouter, HTTPException, Path

from api.routers.api.v1.assets.route import AssetUpdate, SessionDep

router = APIRouter(tags=["patrimoine"])

IdPath = Annotated[str, Path(max_length=36, description="L'identifiant UUID de l'actif")]


async def _load(session: object, asset_id: str):
    asset = await read_asset(session, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="actif introuvable")
    return asset


@router.get("", operation_id="get_asset", summary="La fiche d'un actif")
async def get_asset(session: SessionDep, asset_id: IdPath):
    return await _load(session, asset_id)


@router.patch("", operation_id="patch_asset", summary="Modifier un actif (statut inclus)")
async def patch_asset(session: SessionDep, asset_id: IdPath, changes: AssetUpdate):
    await _load(session, asset_id)
    return await update_asset(session, asset_id, changes)


@router.delete("", operation_id="delete_asset", summary="Supprimer un actif", status_code=204)
async def remove_asset(session: SessionDep, asset_id: IdPath) -> None:
    await _load(session, asset_id)
    await delete_asset(session, asset_id)
