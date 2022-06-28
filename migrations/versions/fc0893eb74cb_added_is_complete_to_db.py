"""Added is_complete to db

Revision ID: fc0893eb74cb
Revises: 04b0e2449d5a
Create Date: 2022-05-05 17:50:56.649086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc0893eb74cb'
down_revision = '04b0e2449d5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###
