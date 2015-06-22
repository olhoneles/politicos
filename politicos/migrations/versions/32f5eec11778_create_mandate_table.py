"""Create mandate table

Revision ID: 32f5eec11778
Revises: 3a41443d8839
Create Date: 2015-06-29 22:49:29.941746

"""

# revision identifiers, used by Alembic.
revision = '32f5eec11778'
down_revision = '3a41443d8839'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'mandate',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date_start', sa.Date, nullable=False),
        sa.Column('date_end', sa.Date, nullable=False),
        sa.Column('legislator_id', sa.Integer, nullable=False),
        sa.Column('political_office_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_political_office',
        'mandate', 'political_office',
        ['political_office_id'], ['id']
    )

    op.create_foreign_key(
        'fk_legislator',
        'mandate', 'legislator',
        ['legislator_id'], ['id']
    )

    op.create_unique_constraint(
        'uk_mandate',
        'mandate',
        ['legislator_id', 'political_office_id', 'date_start', 'date_end']
    )


def downgrade():
    op.drop_constraint('fk_political_office', 'mandate', type_='foreignkey')
    op.drop_constraint('fk_legislator', 'mandate', type_='foreignkey')
    op.drop_constraint('uk_mandate', 'mandate', type_='unique')
    op.drop_table('mandate')
