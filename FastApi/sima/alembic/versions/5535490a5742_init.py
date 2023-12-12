"""init

Revision ID: 5535490a5742
Revises: 
Create Date: 2023-12-12 18:52:59.634383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5535490a5742'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dynamic_api_data',
    sa.Column('subject_name', sa.String(length=255), nullable=True, comment='接口所属主题域'),
    sa.Column('api_name', sa.String(length=255), nullable=True, comment='接口名称'),
    sa.Column('api_desc', sa.Text(), nullable=True, comment='用于生成接口描述文档'),
    sa.Column('api_version', sa.String(length=255), nullable=True, comment='接口版本'),
    sa.Column('methods', sa.String(length=255), nullable=True, comment='接口请求方式'),
    sa.Column('jinja_content', sa.Text(), nullable=True, comment='jinja2格式的内容'),
    sa.Column('inner_validate', sa.Text(), nullable=True, comment='内部保留的验证器'),
    sa.Column('custom_validate', sa.Text(), nullable=True, comment='自定义的验证器'),
    sa.Column('target_desc', sa.Text(), nullable=True, comment='指标描述'),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='id'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dynamic_api_data')
    # ### end Alembic commands ###
