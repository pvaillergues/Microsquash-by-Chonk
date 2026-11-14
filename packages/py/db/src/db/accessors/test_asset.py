"""Le seul lieu qui lit ou écrit les lignes de ``test_assets``.

Les routes importent ces fonctions directement : aucun hôte ne contient de requête ORM.
"""

import uuid
from collections import Counter
from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db.models.test_asset import TestAsset


class AssetIn(BaseModel):
    id: uuid.UUID
    reference: str
    name: str
    project: str
    type: str
    status: str
    owner: str | None
    description: str | None
    created_at: Any
    updated_at: Any


def _asset_in(row: TestAsset) -> AssetIn:
    return AssetIn(
        id=row.id,
        reference=row.reference,
        name=row.name,
        project=row.project,
        type=row.type,
        status=row.status,
        owner=row.owner,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


async def list_assets(
    session: AsyncSession,
    *,
    q: str | None = None,
    project: str | None = None,
    type: str | None = None,
    status: str | None = None,
) -> list[AssetIn]:
    """Les actifs correspondant aux filtres ; ``q`` cherche dans la référence, le nom et la
    description."""
    statement = select(TestAsset)
    if q:
        statement = statement.where(
            TestAsset.reference.contains(q)  # type: ignore[union-attr]
            | TestAsset.name.contains(q)  # type: ignore[union-attr]
            | TestAsset.description.contains(q)  # type: ignore[union-attr]
        )
    if project:
        statement = statement.where(TestAsset.project == project)
    if type:
        statement = statement.where(TestAsset.type == type)
    if status:
        statement = statement.where(TestAsset.status == status)
    result = await session.execute(statement.order_by(TestAsset.reference))  # type: ignore[arg-type]
    rows = result.scalars().all()
    return [_asset_in(row) for row in rows]


async def _by_reference(session: AsyncSession, reference: str) -> TestAsset | None:
    result = await session.execute(
        select(TestAsset).where(TestAsset.reference == reference)  # type: ignore[arg-type]
    )
    return result.scalars().first()


async def get_asset(session: AsyncSession, reference: str) -> AssetIn | None:
    """L'actif portant cette référence, s'il existe."""
    row = await _by_reference(session, reference)
    return _asset_in(row) if row is not None else None


async def read_asset(session: AsyncSession, asset_id: str) -> AssetIn | None:
    """L'actif portant cet identifiant UUID, s'il existe."""
    try:
        parsed = uuid.UUID(asset_id)
    except ValueError:
        return None
    row = await session.get(TestAsset, parsed)
    return _asset_in(row) if row is not None else None


async def create_asset(session: AsyncSession, asset: object) -> AssetIn:
    row = TestAsset(**asset.model_dump())
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return _asset_in(row)


async def upsert_asset(session: AsyncSession, asset: object, *, update: bool) -> AssetIn:
    """Crée l'actif, ou met à jour celui qui porte déjà la même référence."""
    data = asset.model_dump()
    existing = await _by_reference(session, data["reference"])
    if existing is None or not update:
        row = TestAsset(**data)
        session.add(row)
    else:
        for key, value in data.items():
            setattr(existing, key, value)
        row = existing
    await session.commit()
    await session.refresh(row)
    return _asset_in(row)


async def update_asset(session: AsyncSession, asset_id: str, changes: object) -> AssetIn:
    row = await session.get(TestAsset, uuid.UUID(asset_id))
    for key, value in changes.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    await session.commit()
    await session.refresh(row)
    return _asset_in(row)


async def delete_asset(session: AsyncSession, asset_id: str) -> None:
    row = await session.get(TestAsset, uuid.UUID(asset_id))
    await session.delete(row)
    await session.commit()


async def stats(
    session: AsyncSession,
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    """Les volumétries : par projet, par type et par statut."""
    result = await session.execute(select(TestAsset))
    rows = result.scalars().all()
    by_project = Counter(row.project for row in rows)
    by_type = Counter(row.type for row in rows)
    by_status = Counter(row.status for row in rows)
    return dict(by_project), dict(by_type), dict(by_status)
