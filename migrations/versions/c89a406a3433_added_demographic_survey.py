"""added_demographic_survey

Revision ID: c89a406a3433
Revises: 0c20435d96d9
Create Date: 2023-12-15 16:00:00.232393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c89a406a3433'
down_revision = '0c20435d96d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('demographic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skin_experience', sa.String(length=32), nullable=False),
    sa.Column('computer_experience', sa.String(length=32), nullable=False),
    sa.Column('age', sa.String(length=16), nullable=False),
    sa.Column('gender', sa.String(length=16), nullable=False),
    sa.Column('completed_study', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('demographic')
    # ### end Alembic commands ###
