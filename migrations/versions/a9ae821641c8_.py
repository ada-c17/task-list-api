"""empty message

Revision ID: a9ae821641c8
Revises: 1d75c9950a8b
Create Date: 2022-05-06 13:12:57.465173

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a9ae821641c8'
down_revision = '1d75c9950a8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.Boolean(), nullable=True))
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###
