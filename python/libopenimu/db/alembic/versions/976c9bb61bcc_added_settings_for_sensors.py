"""added settings for sensors

Revision ID: 976c9bb61bcc
Revises: 9f2446706f91
Create Date: 2023-11-30 09:18:13.301296

"""
from alembic import op
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = '976c9bb61bcc'
down_revision = '9f2446706f91'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tabSensors', Column('settings', String()))


def downgrade():
    op.drop_column('tabSensors', 'settings')
