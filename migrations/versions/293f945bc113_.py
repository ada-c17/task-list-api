"""empty message

Revision ID: 293f945bc113
Revises: deb8c711baf5
Create Date: 2022-05-09 15:18:47.079955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '293f945bc113'
down_revision = 'deb8c711baf5'
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
