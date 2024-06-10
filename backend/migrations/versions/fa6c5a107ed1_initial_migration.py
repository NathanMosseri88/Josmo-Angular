"""initial migration

Revision ID: fa6c5a107ed1
Revises: 
Create Date: 2024-06-10 10:21:24.869841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa6c5a107ed1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proposal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('run_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('view_by', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('pairs_cases', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('include_columns', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('stock_filters', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('file_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('styles', sa.String(), nullable=False))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password')

    with op.batch_alter_table('proposal', schema=None) as batch_op:
        batch_op.drop_column('styles')
        batch_op.drop_column('file_name')
        batch_op.drop_column('status')
        batch_op.drop_column('stock_filters')
        batch_op.drop_column('include_columns')
        batch_op.drop_column('pairs_cases')
        batch_op.drop_column('view_by')
        batch_op.drop_column('run_type')

    # ### end Alembic commands ###