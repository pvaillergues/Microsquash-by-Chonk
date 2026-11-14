"""Le patrimoine de test : la table test_assets.

Revision ID: pat01_test_assets
Revises: None
Create Date: 2026-11-14

Une branche indépendante par capacité qui possède une table : ``down_revision = None``, étiquetée
par la capacité (``patrimoine``), à monter jusqu'à ``heads``.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "pat01_test_assets"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = ("patrimoine",)
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "test_assets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("reference", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("project", sa.String(length=100), nullable=False),
        sa.Column("type", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("owner", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("reference"),
    )
    op.create_index(op.f("ix_test_assets_reference"), "test_assets", ["reference"])
    op.create_index(op.f("ix_test_assets_project"), "test_assets", ["project"])
    op.create_index(op.f("ix_test_assets_type"), "test_assets", ["type"])
    op.create_index(op.f("ix_test_assets_status"), "test_assets", ["status"])


def downgrade() -> None:
    op.drop_index(op.f("ix_test_assets_status"), table_name="test_assets")
    op.drop_index(op.f("ix_test_assets_type"), table_name="test_assets")
    op.drop_index(op.f("ix_test_assets_project"), table_name="test_assets")
    op.drop_index(op.f("ix_test_assets_reference"), table_name="test_assets")
    op.drop_table("test_assets")
