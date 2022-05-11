"""empty message

Revision ID: 29b56e6de13e
Revises: abe298a97523
Create Date: 2022-05-10 22:34:22.292547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29b56e6de13e'
down_revision = 'abe298a97523'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
