"""added sample_id to samples

Revision ID: 5a3aef2aeab4
Revises: b24f0f09646e
Create Date: 2024-02-27 14:37:40.614606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a3aef2aeab4'
down_revision = 'b24f0f09646e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sample_id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.drop_column('sample_id')

    # ### end Alembic commands ###
