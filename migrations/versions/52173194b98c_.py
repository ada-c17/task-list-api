"""empty message

Revision ID: 52173194b98c
Revises: c8cfaf1fa74a
Create Date: 2022-05-12 12:58:19.712992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52173194b98c'
down_revision = 'c8cfaf1fa74a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###