"""La table ``test_assets`` : une ligne par actif du patrimoine de test.

Un actif est un cas de test, une exigence ou une campagne, décrit par sa référence unique dans le
patrimoine, son projet, son type, son statut de cycle de vie et son responsable.
"""

import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(UTC)


class TestAsset(SQLModel, table=True):
    __tablename__ = "test_assets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reference: str = Field(max_length=50, unique=True, index=True)
    name: str = Field(max_length=200)
    project: str = Field(max_length=100, index=True)
    type: str = Field(max_length=30, index=True)
    status: str = Field(max_length=30, index=True)
    owner: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now, sa_column_kwargs={"onupdate": _now})
