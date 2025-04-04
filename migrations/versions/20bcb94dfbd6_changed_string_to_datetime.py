"""changed string to datetime

Revision ID: 20bcb94dfbd6
Revises: 31d1cc2791c4
Create Date: 2024-02-05 10:48:28.663227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20bcb94dfbd6'
down_revision = '31d1cc2791c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consent', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.DateTime(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consent', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DateTime(),
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)

    # ### end Alembic commands ###
