"""default value for permission

Revision ID: cee8c8dc26ec
Revises: 4cc716d9987a
Create Date: 2025-05-17 19:07:20.292614

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cee8c8dc26ec"
down_revision: str | None = "4cc716d9987a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("users", "permission", server_default=sa.text("'USER'"))


def downgrade() -> None:
    op.alter_column("users", "permission", server_default=None)
