"""create political_party table

Revision ID: 4c650f057f68
Revises: None
Create Date: 2015-05-11 13:32:38.652391

"""

# revision identifiers, used by Alembic.
revision = '4c650f057f68'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'political_party',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(2048), nullable=False),
        sa.Column('siglum', sa.Unicode(2048), nullable=False),
        sa.Column('wikipedia', sa.Unicode(2048), nullable=True),
    )


def downgrade():
    pass
