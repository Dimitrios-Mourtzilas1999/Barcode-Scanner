"""add roles

Revision ID: fa47aeab803e
Revises: 720a970c61b8
Create Date: 2025-11-07 11:34:50.161323

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fa47aeab803e"
down_revision = "720a970c61b8"
branch_labels = None
depends_on = None


def upgrade():
    roles_table = sa.table(
        "roles",
        sa.column("role", sa.String),
    )

    data = [{"role": "admin"}, {"role": "user"}]
    op.bulk_insert(roles_table, data)


def downgrade():
    pass
