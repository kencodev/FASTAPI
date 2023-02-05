"""create posts table

Revision ID: 36fc441b6f7a
Revises: 
Create Date: 2023-02-05 11:38:33.162786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36fc441b6f7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.INTEGER(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=None, onupdate=True, server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table('posts')
