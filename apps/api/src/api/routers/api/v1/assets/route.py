"""L'inventaire des actifs de test : recherche, filtres et création.

Sert ``/api/v1/assets`` — ``route.py`` est l'index du dossier.
"""

from typing import Annotated

from db.accessors.test_asset import AssetIn, create_asset, get_asset, list_assets
from db.engine import get_session_maker
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(tags=["patrimoine"])


def get_session():
    maker = get_session_maker()
    yield maker()


SessionDep = Annotated[object, Depends(get_session)]

SearchDep = Annotated[str | None, Query(max_length=100)]


class AssetCreate(BaseModel):
    reference: str = Field(max_length=50)
    name: str = Field(max_length=200)
    project: str = Field(max_length=100)
    type: str = Field(max_length=30)
    status: str = Field(max_length=30)
    owner: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=2000)


class AssetUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=200)
    project: str | None = Field(default=None, max_length=100)
    type: str | None = Field(default=None, max_length=30)
    status: str | None = Field(default=None, max_length=30)
    owner: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=2000)


class AssetList(BaseModel):
    total: int
    items: list[AssetIn]


@router.get("", operation_id="list_assets", summary="L'inventaire des actifs, filtré")
async def get_assets(
    session: SessionDep,
    q: SearchDep = None,
    project: SearchDep = None,
    type: SearchDep = None,
    status: SearchDep = None,
) -> AssetList:
    """Les actifs de test, filtrables par projet, type, statut et recherche sur la référence, le
    nom et la description."""
    items = await list_assets(session, q=q, project=project, type=type, status=status)
    return AssetList(total=len(items), items=items)


@router.post("", operation_id="create_asset", summary="Créer un actif", status_code=201)
async def post_asset(session: SessionDep, asset: AssetCreate) -> AssetIn:
    found = await get_asset(session, asset.reference)
    if found is not None:
        raise HTTPException(status_code=409, detail=f"la référence {asset.reference} existe déjà")
    return await create_asset(session, asset)
