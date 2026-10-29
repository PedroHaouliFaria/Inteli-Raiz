"""create_purchases_confirmations_reviews_events

Revision ID: 551247208051
Revises: 
Create Date: 2026-10-28 10:48:44.119323
"""
from alembic import op
import sqlalchemy as sa


revision = '551247208051'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('case_id', sa.String(length=20), nullable=False),
        sa.Column('customer_id', sa.String(length=50), nullable=False),
        sa.Column('fixture_id', sa.String(length=80), nullable=False),
        sa.Column('status', sa.String(length=40), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('amount_cents', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('mcc', sa.String(length=10), nullable=False),
        sa.Column('card_brand', sa.String(length=30), nullable=False),
        sa.Column('card_type', sa.String(length=20), nullable=False),
        sa.Column('card_last4', sa.String(length=4), nullable=False),
        sa.Column('channel', sa.String(length=30), nullable=False),
        sa.Column('features_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchases_case_id'), 'purchases', ['case_id'], unique=True)
    op.create_index(op.f('ix_purchases_customer_id'), 'purchases', ['customer_id'], unique=False)

    op.create_table(
        'confirmations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('challenge_id', sa.String(length=20), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('answered_response', sa.String(length=20), nullable=True),
        sa.Column('answered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('idempotency_key', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_confirmations_challenge_id'), 'confirmations', ['challenge_id'], unique=True)
    op.create_index(op.f('ix_confirmations_purchase_id'), 'confirmations', ['purchase_id'], unique=False)

    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('review_id', sa.String(length=20), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('protocol', sa.String(length=30), nullable=False),
        sa.Column('kind', sa.String(length=20), nullable=False),
        sa.Column('reason', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_by', sa.String(length=20), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('protocol'),
    )
    op.create_index(op.f('ix_reviews_purchase_id'), 'reviews', ['purchase_id'], unique=False)
    op.create_index(op.f('ix_reviews_review_id'), 'reviews', ['review_id'], unique=True)

    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=40), nullable=False),
        sa.Column('from_status', sa.String(length=40), nullable=True),
        sa.Column('to_status', sa.String(length=40), nullable=True),
        sa.Column('payload', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_events_purchase_id'), 'events', ['purchase_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_events_purchase_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_reviews_review_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_purchase_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_confirmations_purchase_id'), table_name='confirmations')
    op.drop_index(op.f('ix_confirmations_challenge_id'), table_name='confirmations')
    op.drop_table('confirmations')
    op.drop_index(op.f('ix_purchases_customer_id'), table_name='purchases')
    op.drop_index(op.f('ix_purchases_case_id'), table_name='purchases')
    op.drop_table('purchases')
