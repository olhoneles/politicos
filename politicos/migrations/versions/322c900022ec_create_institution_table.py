"""create institution table

Revision ID: 322c900022ec
Revises: 594fc9f784e1
Create Date: 2015-06-13 11:55:59.290055

"""

# revision identifiers, used by Alembic.
revision = '322c900022ec'
down_revision = '594fc9f784e1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'institution',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('siglum', sa.String(15), nullable=False),
        sa.Column('logo', sa.String(2048), nullable=True),
    )

    op.create_unique_constraint('uk_siglum', 'institution', ['siglum'])
    op.create_unique_constraint('uk_name', 'institution', ['name'])


def downgrade():
    op.drop_constraint('uk_siglum', 'institution', type_='unique')
    op.drop_constraint('uk_name', 'institution', type_='unique')

    op.drop_table('institution')
