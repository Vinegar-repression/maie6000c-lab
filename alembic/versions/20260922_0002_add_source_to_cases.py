"""add source to cases

Revision ID: 20260922_0002
Revises: 20260713_0001
Create Date: 2026-09-22
"""

import sqlalchemy as sa
from alembic import op

revision = "20260922_0002"
down_revision = "20260713_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cases",
        sa.Column("source", sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("cases", "source")
