"""initial schema

Revision ID: 0421cc4d5ed1
Revises: 
Create Date: 2026-10-22 21:40:01.426057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0421cc4d5ed1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "length(trim(name)) > 0",
            name="categories_name_check",
        ),
        sa.PrimaryKeyConstraint("id", name="categories_pkey"),
    )

    op.create_table(
        "epics",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("category_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "length(trim(name)) > 0",
            name="epics_name_check",
        ),
        sa.PrimaryKeyConstraint("id", name="epics_pkey"),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="epics_category_id_fkey",
        ),
        sa.UniqueConstraint(
            "id",
            "category_id",
            name="epics_id_category_unique",
        ),
    )

    op.create_index(
        "epics_category_id_idx",
        "epics",
        ["category_id"],
    )

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("category_id", sa.BigInteger(), nullable=False),
        sa.Column("epic_id", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Text(),
            server_default=sa.text("'todo'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "length(trim(title)) > 0",
            name="tasks_title_check",
        ),
        sa.CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')",
            name="tasks_status_check",
        ),
        sa.PrimaryKeyConstraint("id", name="tasks_pkey"),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="tasks_category_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["epic_id", "category_id"],
            ["epics.id", "epics.category_id"],
            name="tasks_epic_id_category_id_fkey",
        ),
    )

    op.create_index(
        "tasks_category_id_idx",
        "tasks",
        ["category_id"],
    )
    op.create_index(
        "tasks_epic_id_idx",
        "tasks",
        ["epic_id"],
    )    


def downgrade() -> None:
    op.drop_index("tasks_epic_id_idx", table_name="tasks")
    op.drop_index("tasks_category_id_idx", table_name="tasks")
    op.drop_table("tasks")

    op.drop_index("epics_category_id_idx", table_name="epics")
    op.drop_table("epics")

    op.drop_table("categories")