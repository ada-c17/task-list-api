"""Create relationship between goal and tasks

Revision ID: 5db2793e22f6
Revises: 8874a4c881ed
Create Date: 2022-05-11 15:57:28.962653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5db2793e22f6'
down_revision = '8874a4c881ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('goal', 'goal_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('goal_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'id')
    # ### end Alembic commands ###
