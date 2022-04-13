"""empty message

Revision ID: 62b727e68ce0
Revises: 9d611811933b
Create Date: 2022-04-13 23:53:14.350256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b727e68ce0'
down_revision = '9d611811933b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('role', sa.String(length=10), nullable=True))
    op.drop_index('ix_user_email', table_name='user')
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True))
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.drop_column('user', 'role')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###
