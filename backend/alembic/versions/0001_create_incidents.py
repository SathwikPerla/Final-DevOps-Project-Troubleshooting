"""Create incidents table

Revision ID: 0001_create_incidents
Revises: 
Create Date: 2026-10-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_incidents"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="OPEN"),
        sa.Column("service", sa.String(length=100), nullable=False, server_default="api-gateway"),
        sa.Column("assignee", sa.String(length=120), nullable=False, server_default="DevOps On-Call"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table("incidents")
