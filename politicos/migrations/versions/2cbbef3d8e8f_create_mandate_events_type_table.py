"""create mandate events type table

Revision ID: 2cbbef3d8e8f
Revises: 32f5eec11778
Create Date: 2015-07-05 13:23:45.985573

"""

# revision identifiers, used by Alembic.
revision = '2cbbef3d8e8f'
down_revision = '32f5eec11778'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'mandate_events_type',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
    )

    op.create_unique_constraint('uk_name', 'mandate_events_type', ['name'])
    op.create_unique_constraint('uk_slug', 'mandate_events_type', ['slug'])


def downgrade():
    op.drop_constraint('uk_name', 'mandate_events_type', type_='unique')
    op.drop_constraint('uk_slug', 'mandate_events_type', type_='unique')

    op.drop_table('mandate_events_type')
