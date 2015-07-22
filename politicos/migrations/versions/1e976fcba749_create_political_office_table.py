"""Create political office table

Revision ID: 1e976fcba749
Revises: 322c900022ec
Create Date: 2015-06-20 17:10:25.744695

"""

# revision identifiers, used by Alembic.
revision = '1e976fcba749'
down_revision = '322c900022ec'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'political_office',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(100), nullable=False),
        sa.Column('slug', sa.Unicode(255), nullable=False),
    )

    op.create_unique_constraint('uk_name', 'political_office', ['name'])
    op.create_unique_constraint('uk_slug', 'political_office', ['slug'])


def downgrade():
    op.drop_constraint('uk_name', 'political_office', type_='unique')
    op.drop_constraint('uk_slug', 'political_office', type_='unique')

    op.drop_table('political_office')
