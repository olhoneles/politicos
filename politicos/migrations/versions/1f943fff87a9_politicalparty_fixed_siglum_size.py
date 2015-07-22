"""PoliticalParty: Fixed siglum size

Revision ID: 1f943fff87a9
Revises: 3c20fed5a17f
Create Date: 2015-06-08 22:05:48.444754

"""

# revision identifiers, used by Alembic.
revision = '1f943fff87a9'
down_revision = '3c20fed5a17f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'political_party', 'siglum', type_=sa.Unicode(15), nullable=False
    )


def downgrade():
    op.alter_column(
        'political_party', 'siglum', type_=sa.Unicode(2048), nullable=False
    )
