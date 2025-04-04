"""added tmdbId column to a Films

Revision ID: 026aed5fa184
Revises: bfc23f23af4c
Create Date: 2025-02-19 22:01:49.456291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '026aed5fa184'
down_revision: Union[str, None] = 'bfc23f23af4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films', sa.Column('tmdbId', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('films', 'tmdbId')
    # ### end Alembic commands ###
