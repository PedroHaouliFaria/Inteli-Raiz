"""add_analysis_columns_and_chat_messages

Revision ID: a1b2c3d4e5f6
Revises: 7376252b05a7
Create Date: 2026-10-29 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '7376252b05a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Colunas de análise na tabela purchases
    with op.batch_alter_table('purchases') as batch_op:
        batch_op.add_column(sa.Column('analysis_score', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('analysis_score_source', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('analysis_model_version', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('analysis_decision', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('analysis_policy_version', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('analysis_gaps_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('analysis_evaluated_at', sa.DateTime(timezone=True), nullable=True))

    # Tabela de mensagens do chat
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('message_id', sa.String(length=20), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=10), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tools_used_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_chat_messages_message_id'), 'chat_messages', ['message_id'], unique=True)
    op.create_index(op.f('ix_chat_messages_purchase_id'), 'chat_messages', ['purchase_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_chat_messages_purchase_id'), table_name='chat_messages')
    op.drop_index(op.f('ix_chat_messages_message_id'), table_name='chat_messages')
    op.drop_table('chat_messages')

    with op.batch_alter_table('purchases') as batch_op:
        batch_op.drop_column('analysis_evaluated_at')
        batch_op.drop_column('analysis_gaps_json')
        batch_op.drop_column('analysis_policy_version')
        batch_op.drop_column('analysis_decision')
        batch_op.drop_column('analysis_model_version')
        batch_op.drop_column('analysis_score_source')
        batch_op.drop_column('analysis_score')
