"""changed explanation version location

Revision ID: c98615cfcdcb
Revises: 07cb99d91120
Create Date: 2024-02-26 14:29:20.897834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c98615cfcdcb'
down_revision = '07cb99d91120'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('demographic', schema=None) as batch_op:
        batch_op.drop_column('explanation_version')

    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('explanation_version', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_column('explanation_version')

    with op.batch_alter_table('demographic', schema=None) as batch_op:
        batch_op.add_column(sa.Column('explanation_version', sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###
