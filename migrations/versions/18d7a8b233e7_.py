"""empty message

Revision ID: 18d7a8b233e7
Revises: d72b7b7d248f
Create Date: 2022-05-06 11:40:32.322794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18d7a8b233e7'
down_revision = 'd72b7b7d248f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
