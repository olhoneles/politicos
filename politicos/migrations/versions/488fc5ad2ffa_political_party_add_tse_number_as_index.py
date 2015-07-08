"""political party: add tse_number as index

Revision ID: 488fc5ad2ffa
Revises: 192bd4ccdacb
Create Date: 2015-07-08 13:44:38.208146

"""

# revision identifiers, used by Alembic.
revision = '488fc5ad2ffa'
down_revision = '192bd4ccdacb'

from alembic import op


def upgrade():
    op.create_index('idx_tse_number', 'political_party', ['tse_number'])


def downgrade():
    op.drop_index('idx_tse_number', 'political_party')
