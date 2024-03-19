"""Add description to MeetingRoom

Revision ID: a6980501bd1a
Revises: 66e6ed2dfdbe
Create Date: 2024-01-23 18:57:43.202218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6980501bd1a'
down_revision = '66e6ed2dfdbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meetingroom', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meetingroom', 'description')
    # ### end Alembic commands ###
