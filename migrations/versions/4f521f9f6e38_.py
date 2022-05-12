"""empty message

Revision ID: 4f521f9f6e38
Revises: 18eda02cfff8
Create Date: 2022-05-11 19:39:35.117299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f521f9f6e38'
down_revision = '18eda02cfff8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###
