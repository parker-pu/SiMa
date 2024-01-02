"""init sc

Revision ID: 630cb93b2cb2
Revises: 9a06e555181d
Create Date: 2023-12-30 17:23:10.806465

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '630cb93b2cb2'
down_revision = '9a06e555181d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scan_table_history', sa.Column('add_column', sa.String(length=255), nullable=True, comment='新增字段'))
    op.add_column('scan_table_history', sa.Column('up_column', sa.String(length=255), nullable=True, comment='更新字段'))
    op.add_column('scan_table_history', sa.Column('del_column', sa.String(length=255), nullable=True, comment='删除字段'))
    op.drop_column('scan_table_history', 'up_table')
    op.drop_column('scan_table_history', 'add_table')
    op.drop_column('scan_table_history', 'del_table')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scan_table_history', sa.Column('del_table', mysql.VARCHAR(length=255), nullable=True, comment='删除字段'))
    op.add_column('scan_table_history', sa.Column('add_table', mysql.VARCHAR(length=255), nullable=True, comment='新增字段'))
    op.add_column('scan_table_history', sa.Column('up_table', mysql.VARCHAR(length=255), nullable=True, comment='更新字段'))
    op.drop_column('scan_table_history', 'del_column')
    op.drop_column('scan_table_history', 'up_column')
    op.drop_column('scan_table_history', 'add_column')
    # ### end Alembic commands ###
