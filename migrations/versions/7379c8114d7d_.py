"""empty message

Revision ID: 7379c8114d7d
Revises: 2496a0fcf480
Create Date: 2024-01-15 18:16:10.416775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7379c8114d7d'
down_revision = '2496a0fcf480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ai', schema=None) as batch_op:
        batch_op.alter_column('shap_impaint_telea_image_url',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('shap_inpaint_ns_image_url',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('shap_blur_image_url',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('saliency_image_url',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ai', schema=None) as batch_op:
        batch_op.alter_column('saliency_image_url',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('shap_blur_image_url',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('shap_inpaint_ns_image_url',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('shap_impaint_telea_image_url',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###