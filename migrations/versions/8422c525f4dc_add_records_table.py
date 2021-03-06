"""Add records table

Revision ID: 8422c525f4dc
Revises:
Create Date: 2020-05-16 20:22:36.953038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8422c525f4dc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("amount", sa.Numeric(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("happened_at", sa.DateTime(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("records")
    # ### end Alembic commands ###
