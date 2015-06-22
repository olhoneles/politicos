"""create legislature table

Revision ID: 3a41443d8839
Revises: 1e976fcba749
Create Date: 2015-06-21 22:26:53.461218

"""

# revision identifiers, used by Alembic.
revision = '3a41443d8839'
down_revision = '1e976fcba749'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'legislature',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date_start', sa.Date, nullable=False),
        sa.Column('date_end', sa.Date, nullable=False),
        sa.Column('institution_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_institution',
        'legislature', 'institution',
        ['institution_id'], ['id']
    )

    op.create_unique_constraint(
        'uk_legislature',
        'legislature',
        ['institution_id', 'date_start', 'date_end']
    )


def downgrade():
    op.drop_constraint('fk_institution', 'legislature', type_='foreignkey')
    op.drop_constraint('uk_legislature', 'legislature', type_='unique')
    op.drop_table('legislature')
