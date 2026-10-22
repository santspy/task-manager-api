"""create users and tasks tables

Revision ID: 1c54544f0114
Revises: 
Create Date: 2026-10-22 
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1c54544f0114'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Criar tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    # 2. Criar tabela tasks
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)

def downgrade() -> None:
    # Comandos de remoção ficam apenas aqui no downgrade
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')