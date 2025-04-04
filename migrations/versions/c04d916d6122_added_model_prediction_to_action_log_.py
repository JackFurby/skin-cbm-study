"""added model prediction to action log table

Revision ID: c04d916d6122
Revises: b72cbfbaad63
Create Date: 2024-04-03 16:03:26.750342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04d916d6122'
down_revision = 'b72cbfbaad63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('action', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model_malignant', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('action', schema=None) as batch_op:
        batch_op.drop_column('model_malignant')

    # ### end Alembic commands ###
