"""Added some fields in PoliticalParty

Revision ID: b6484fc6bd4
Revises: 4c650f057f68
Create Date: 2015-06-03 23:32:28.969643

"""

# revision identifiers, used by Alembic.
revision = 'b6484fc6bd4'
down_revision = '4c650f057f68'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'political_party',
        sa.Column('website', type_=sa.String(2048), nullable=True)
    )

    op.add_column(
        'political_party',
        sa.Column('logo', type_=sa.String(2048), nullable=True)
    )

    op.add_column(
        'political_party',
        sa.Column('founded_date', type_=sa.DateTime, nullable=True)
    )


def downgrade():
    op.drop_column('political_party', 'website')
    op.drop_column('political_party', 'logo')
    op.drop_column('political_party', 'founded_date')
