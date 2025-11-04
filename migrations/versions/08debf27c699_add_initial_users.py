"""Add initial users

Revision ID: 08debf27c699
Revises: 06facfea8f3d
Create Date: 2025-11-04 21:09:07.568845

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision = '08debf27c699'
down_revision = '06facfea8f3d'
branch_labels = None
depends_on = None


def upgrade():
    users_table = table('users',
                        column('id',Integer),
                        column('username',String),
                        column('password',String),
                        column('role_id',Integer)
                        )
    op.bulk_insert(users_table,
                   [{
                       'username':'nikosmour',
                       'password':'8fc200735dae172c7f4843d837f038546786958dddc0c53c255e54b236446135',
                       'role_id':2
                   },
                   {
                       'username':'dimimour',
                       'password':'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                       'role_id':1
                   },
                   
                   ])


def downgrade():
     op.execute("DELETE FROM users WHERE username IN ('nikosmour', 'dimimour')")
