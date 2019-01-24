"""0_5_upgrade

Revision ID: 6b75a01d10b5
Revises: 
Create Date: 2019-01-24 13:13:30.479559

"""
from alembic import op
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = '6b75a01d10b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tabSensors', Column('hw_id', String()))


def downgrade():
    op.remove_column('tabSensors', 'hw_id')
