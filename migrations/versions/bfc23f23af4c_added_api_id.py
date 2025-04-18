"""added api id

Revision ID: bfc23f23af4c
Revises: cf76e82cd7b6
Create Date: 2025-01-29 22:43:43.232554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bfc23f23af4c'
down_revision: Union[str, None] = 'cf76e82cd7b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films', sa.Column('apiId', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('films', 'apiId')
    # ### end Alembic commands ###
