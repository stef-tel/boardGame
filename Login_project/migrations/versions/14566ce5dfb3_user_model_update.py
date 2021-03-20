"""User Model Update

Revision ID: 14566ce5dfb3
Revises: 
Create Date: 2020-04-24 01:38:52.879198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14566ce5dfb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('lastActivity', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('numberConnection', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'numberConnection')
    op.drop_column('user', 'lastActivity')
    # ### end Alembic commands ###