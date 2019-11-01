"""Added params in processed data

Revision ID: 9f2446706f91
Revises: 6b75a01d10b5
Create Date: 2019-10-29 10:58:57.714223

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = '9f2446706f91'
down_revision = '6b75a01d10b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tabProcessedData', Column('params', String()))


def downgrade():
    op.remove_column('tabProcessedData', 'params')
