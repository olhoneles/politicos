"""create legislator events type table

Revision ID: 408d279887d6
Revises: 585774625ec2
Create Date: 2015-07-07 19:18:47.828429

"""

# revision identifiers, used by Alembic.
revision = '408d279887d6'
down_revision = '585774625ec2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'legislator_events_type',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(100), nullable=False),
        sa.Column('slug', sa.Unicode(255), nullable=False),
    )

    op.create_unique_constraint('uk_name', 'legislator_events_type', ['name'])
    op.create_unique_constraint('uk_slug', 'legislator_events_type', ['slug'])


def downgrade():
    op.drop_constraint('uk_name', 'legislator_events_type', type_='unique')
    op.drop_constraint('uk_slug', 'legislator_events_type', type_='unique')

    op.drop_table('legislator_events_type')
