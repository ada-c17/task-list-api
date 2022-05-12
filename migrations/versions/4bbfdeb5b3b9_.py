"""empty message

Revision ID: 4bbfdeb5b3b9
Revises: 349b7cbc3a91
Create Date: 2022-05-09 21:41:09.708906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bbfdeb5b3b9'
down_revision = '349b7cbc3a91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
