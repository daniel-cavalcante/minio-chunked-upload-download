"""create upload table

Revision ID: 8bbc56a2d8d2
Revises: 
Create Date: 2023-07-21 08:41:03.064580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8bbc56a2d8d2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bucket_object",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("bucket_name", sa.UUID(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("upload")
