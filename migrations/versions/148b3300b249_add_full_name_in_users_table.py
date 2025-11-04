"""Add full_name in users table

Revision ID: 148b3300b249
Revises: 08debf27c699
Create Date: 2025-11-04 22:00:31.218247

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '148b3300b249'
down_revision = '08debf27c699'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String(length=30), nullable=True, server_default=''))


def downgrade():
    pass
