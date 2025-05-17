"""Set server defaults

Revision ID: ac9c90590731
Revises: 5ae24caa7e96
Create Date: 2025-05-17 20:29:26.941510

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ac9c90590731"
down_revision: str | None = "5ae24caa7e96"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "id", server_default=sa.text("gen_random_uuid()"))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "id", server_default=None)
