"""add suppliers table

Revision ID: be7882be76c5
Revises: 0475c8cd3667
Create Date: 2025-12-03 22:39:31.851277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be7882be76c5'
down_revision = '0475c8cd3667'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.add_column('product', sa.Column('supplier_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_product_supplier',
        'product', 'suppliers',
        ['supplier_id'], ['id']
    )

def downgrade():
    op.drop_constraint('fk_product_supplier', 'product', type_='foreignkey')
    op.drop_column('product', 'supplier_id')
    op.drop_table('suppliers')
