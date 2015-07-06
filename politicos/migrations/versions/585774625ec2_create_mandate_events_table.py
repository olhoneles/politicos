"""create mandate events table

Revision ID: 585774625ec2
Revises: 2cbbef3d8e8f
Create Date: 2015-07-06 00:58:44.470013

"""

# revision identifiers, used by Alembic.
revision = '585774625ec2'
down_revision = '2cbbef3d8e8f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'mandate_events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('mandate_id', sa.Integer, nullable=False),
        sa.Column('mandate_events_type_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_mandate',
        'mandate_events', 'mandate',
        ['mandate_id'], ['id']
    )

    op.create_foreign_key(
        'fk_mandate_events_type',
        'mandate_events', 'mandate_events_type',
        ['mandate_events_type_id'], ['id']
    )

    op.create_unique_constraint(
        'uk_mandate_events',
        'mandate_events',
        ['mandate_id', 'mandate_events_type_id', 'date']
    )


def downgrade():
    op.drop_constraint('fk_mandate', 'mandate_events', type_='foreignkey')
    op.drop_constraint(
        'fk_mandate_events_type', 'mandate_events', type_='foreignkey'
    )
    op.drop_constraint('uk_mandate_events', 'mandate_events', type_='unique')
    op.drop_table('mandate_events')
