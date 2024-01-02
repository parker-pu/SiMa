"""init db

Revision ID: 8d6e032cc6d1
Revises: 6dc0a0eb6868
Create Date: 2023-12-28 15:09:07.551869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d6e032cc6d1'
down_revision = '6dc0a0eb6868'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('databases',
    sa.Column('db_host', sa.String(length=255), nullable=True, comment='数据库地址'),
    sa.Column('db_port', sa.INTEGER(), nullable=False, comment='数据库端口'),
    sa.Column('db_type', sa.String(length=255), nullable=False, comment='数据库类型'),
    sa.Column('scan_db_name', sa.String(length=255), nullable=False, comment='需要扫描的数据库'),
    sa.Column('username', sa.String(length=255), nullable=False, comment='用户名'),
    sa.Column('password', sa.String(length=255), nullable=False, comment='密码'),
    sa.Column('use_status', sa.BOOLEAN(), nullable=False, comment='使用状态'),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_databases_db_host'), 'databases', ['db_host'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_databases_db_host'), table_name='databases')
    op.drop_table('databases')
    # ### end Alembic commands ###