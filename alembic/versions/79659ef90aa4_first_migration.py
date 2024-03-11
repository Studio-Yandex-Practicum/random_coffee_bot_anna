"""First migration

Revision ID: 79659ef90aa4
Revises: 
Create Date: 2024-03-11 12:00:22.972124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79659ef90aa4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=13), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('meeting',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_1', sa.Integer(), nullable=False),
    sa.Column('user_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_1'], ['user.user_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_2'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meeting')
    op.drop_table('user')
    # ### end Alembic commands ###