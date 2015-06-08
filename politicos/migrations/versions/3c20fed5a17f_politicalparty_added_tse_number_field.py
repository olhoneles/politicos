"""PoliticalParty: Added tse_number field

Revision ID: 3c20fed5a17f
Revises: b6484fc6bd4
Create Date: 2015-06-07 22:32:45.062573

"""

# revision identifiers, used by Alembic.
revision = '3c20fed5a17f'
down_revision = 'b6484fc6bd4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'political_party',
        sa.Column('tse_number', type_=sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_column('political_party', 'tse_number')
