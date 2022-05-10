"""empty message

Revision ID: 44ebda0e7dc8
Revises: 88cf0b3a5278
Create Date: 2022-05-09 13:18:27.893700

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '44ebda0e7dc8'
down_revision = '88cf0b3a5278'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###
