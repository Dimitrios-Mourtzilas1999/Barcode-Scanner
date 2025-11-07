"""add users

Revision ID: b30ef1e70532
Revises: fa47aeab803e
Create Date: 2025-11-07 11:41:18.443714

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b30ef1e70532"
down_revision = "fa47aeab803e"
branch_labels = None
depends_on = None


def upgrade():
    users_table = sa.table(
        "users",
        sa.column("id", sa.Integer),
        sa.column("username", sa.String),
        sa.column("password", sa.String),
        sa.column("role_id", sa.Integer),
    )

    data = [
        {
            "username": "dimimour",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            "role_id": 1,
        },
        {
            "username": "nikosmour",
            "password": "eff774745a997944ea2a033de3fbb5a2904ac02c8dd59996cbde178ca2641075",
            "role_id": 2,
        },
    ]
    op.bulk_insert(users_table, data)


def downgrade():
    pass
