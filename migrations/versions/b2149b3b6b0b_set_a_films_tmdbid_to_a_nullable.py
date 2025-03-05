"""Set a films.tmdbId to a nullable

Revision ID: b2149b3b6b0b
Revises: 63c63ed0bae7
Create Date: 2025-03-05 22:50:09.594870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b2149b3b6b0b'
down_revision: Union[str, None] = '63c63ed0bae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('films', 'tmdbId',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('films', 'tmdbId',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
