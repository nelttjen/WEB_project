"""empty message

Revision ID: 1ab52f3df10a
Revises: 7e95a7c33640
Create Date: 2022-04-30 01:05:06.079197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ab52f3df10a'
down_revision = '7e95a7c33640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apex_orders', sa.Column('confirm_code', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apex_orders', 'confirm_code')
    # ### end Alembic commands ###
