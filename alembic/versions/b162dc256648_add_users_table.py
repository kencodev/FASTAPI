"""add users table

Revision ID: ee1b07436c01
Revises: 36fc441b6f7a
Create Date: 2023-02-05 11:43:31.215714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee1b07436c01'
down_revision = '36fc441b6f7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('email', sa.String(),  nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
