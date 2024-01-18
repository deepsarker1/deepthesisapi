"""empty message

Revision ID: 8d28845363b8
Revises: aab50edc4157
Create Date: 2024-01-15 16:54:31.180756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d28845363b8'
down_revision = 'aab50edc4157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ai',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('prediction', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ai')
    # ### end Alembic commands ###