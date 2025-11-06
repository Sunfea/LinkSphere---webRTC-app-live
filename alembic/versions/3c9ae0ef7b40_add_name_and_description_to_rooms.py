"""add_name_and_description_to_rooms

Revision ID: 3c9ae0ef7b40
Revises: faea0d2c8833
Create Date: 2025-11-06 16:06:16.975587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c9ae0ef7b40'
down_revision: Union[str, Sequence[str], None] = 'faea0d2c8833'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add name column to rooms table
    op.add_column('rooms', sa.Column('name', sa.String(), nullable=False))
    
    # Add description column to rooms table
    op.add_column('rooms', sa.Column('description', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove description column from rooms table
    op.drop_column('rooms', 'description')
    
    # Remove name column from rooms table
    op.drop_column('rooms', 'name')