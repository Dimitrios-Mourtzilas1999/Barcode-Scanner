"""add data

Revision ID: e247dc90a08e
Revises: 7c60af00d5f4
Create Date: 2025-11-08 14:33:34.645602

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'e247dc90a08e'
down_revision = '7c60af00d5f4'
branch_labels = None
depends_on = None

metadata = sa.MetaData()

def upgrade():
    metadata = sa.MetaData()

    # Define tables
    roles_table = sa.Table(
        'roles',
        metadata,
        sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
        sa.Column('role', sa.String(50), nullable=False)
    )

    users_table = sa.Table(
        'users',
        metadata,
        sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(128), nullable=False)
    )

    # Seed data
    role_data = [
        {'role': 'admin'},
        {'role': 'user'}
    ]

    users_data = [
        {'username': 'dimimour', 'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'},
        {'username': 'nikosmour', 'password': 'eff774745a997944ea2a033de3fbb5a2904ac02c8dd59996cbde178ca2641075'}
    ]

    # Insert data using Alembic
    op.bulk_insert(roles_table, role_data)
    op.bulk_insert(users_table, users_data)





def downgrade():
    op.drop_table('users')
    op.drop_table('roles')