"""empty message

Revision ID: 5f55d1449a6e
Revises: 573060de1870
Create Date: 2022-07-29 17:29:46.240399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f55d1449a6e'
down_revision = '573060de1870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playstyle', sa.Column('is_mouse', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('playstyle', 'is_mouse')
    # ### end Alembic commands ###
