"""add content column to posts table

Revision ID: a6176cc9ccc6
Revises: ea1f54caa4b7
Create Date: 2023-06-10 13:58:17.172158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6176cc9ccc6'
down_revision = 'ea1f54caa4b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
