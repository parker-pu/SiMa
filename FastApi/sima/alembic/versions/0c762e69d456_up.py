"""up

Revision ID: 0c762e69d456
Revises: 5535490a5742
Create Date: 2023-12-12 19:43:16.547070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c762e69d456'
down_revision = '5535490a5742'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dynamic_api_data', sa.Column('api_status', sa.BOOLEAN(), server_default='1', nullable=True, comment='激活'))
    op.create_index(op.f('ix_dynamic_api_data_api_status'), 'dynamic_api_data', ['api_status'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dynamic_api_data_api_status'), table_name='dynamic_api_data')
    op.drop_column('dynamic_api_data', 'api_status')
    # ### end Alembic commands ###