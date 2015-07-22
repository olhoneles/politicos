"""PoliticalParty: Add some indexes

Revision ID: 3ba5c639daba
Revises: 1f943fff87a9
Create Date: 2015-06-08 22:07:09.814059

"""

# revision identifiers, used by Alembic.
revision = '3ba5c639daba'
down_revision = '1f943fff87a9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'political_party', 'name', type_=sa.Unicode(255), nullable=False
    )

    op.create_index('idx_founded_date', 'political_party', ['founded_date'])
    op.create_unique_constraint('uk_siglum', 'political_party', ['siglum'])
    op.create_unique_constraint('uk_name', 'political_party', ['name'])


def downgrade():
    op.drop_index('idx_founded_date', 'political_party')
    op.drop_constraint('uk_siglum', 'political_party', type_='unique')
    op.drop_constraint('uk_name', 'political_party', type_='unique')

    op.alter_column(
        'political_party', 'name', type_=sa.Unicode(2048), nullable=False
    )
