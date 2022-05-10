"""Establish one to many relationship between Goal and Task

Revision ID: 68393f965769
Revises: 88c7cd8fcd19
Create Date: 2022-05-09 22:56:55.742567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68393f965769'
down_revision = '88c7cd8fcd19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
