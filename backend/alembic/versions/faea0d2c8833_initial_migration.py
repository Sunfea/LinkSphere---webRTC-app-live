"""Initial migration

Revision ID: faea0d2c8833
Revises: 
Create Date: 2025-11-05 01:52:33.475767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faea0d2c8833'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Create otps table
    op.create_table(
        'otps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('otp', sa.String(), nullable=False),
        sa.Column('expiry', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otps_email'), 'otps', ['email'], unique=False)
    op.create_index(op.f('ix_otps_id'), 'otps', ['id'], unique=False)
    
    # Create rooms table
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('room_id')
    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)
    op.create_index(op.f('ix_rooms_room_id'), 'rooms', ['room_id'], unique=True)
    
    # Create room_participants association table
    op.create_table(
        'room_participants',
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order
    op.drop_table('room_participants')
    op.drop_index(op.f('ix_rooms_room_id'), table_name='rooms')
    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')
    op.drop_index(op.f('ix_otps_id'), table_name='otps')
    op.drop_index(op.f('ix_otps_email'), table_name='otps')
    op.drop_table('otps')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
