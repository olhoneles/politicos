"""create legislator events table

Revision ID: 192bd4ccdacb
Revises: 408d279887d6
Create Date: 2015-07-07 20:39:15.706543

"""

# revision identifiers, used by Alembic.
revision = '192bd4ccdacb'
down_revision = '408d279887d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'legislator_events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('legislator_id', sa.Integer, nullable=False),
        sa.Column('legislator_events_type_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_legislator_events_legislator',
        'legislator_events', 'legislator',
        ['legislator_id'], ['id']
    )

    op.create_foreign_key(
        'fk_legislator_events_type',
        'legislator_events', 'legislator_events_type',
        ['legislator_events_type_id'], ['id']
    )

    op.create_unique_constraint(
        'uk_legislator_events',
        'legislator_events',
        ['legislator_id', 'legislator_events_type_id', 'date']
    )


def downgrade():
    op.drop_constraint(
        'fk_legislator_events_legislator',
        'legislator_events',
        type_='foreignkey'
    )
    op.drop_constraint(
        'fk_legislator_events_type', 'legislator_events', type_='foreignkey'
    )
    op.drop_constraint(
        'uk_legislator_events', 'legislator_events', type_='unique'
    )
    op.drop_table('legislator_events')
