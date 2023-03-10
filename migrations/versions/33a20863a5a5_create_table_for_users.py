"""create table for users

Revision ID: 33a20863a5a5
Revises: 9d83d7fc9298
Create Date: 2023-02-16 09:54:40.961384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33a20863a5a5'
down_revision = '9d83d7fc9298'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###
