from datetime import datetime

from sqlalchemy import (BigInteger, Identity, Text, text, DateTime, func, 
                        CheckConstraint, ForeignKey, Index, UniqueConstraint, ForeignKeyConstraint)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# TODO: Optimise Data table size
# Parent class that every other model will inherite
class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__   = "categories"

    __table_args__  = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name = "categories_name_check",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key = True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Epic(Base):
    __tablename__  = "epics"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name = "epics_name_check"
        ),
        UniqueConstraint(
            "id", "category_id",
            name="epics_id_category_unique",
        ),
        Index("epics_category_id_idx", "category_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    
    # FK
    category_id: Mapped[int] = mapped_column(BigInteger, 
                                             ForeignKey("categories.id", name="epics_category_id_fkey"), 
                                             nullable=False)
    
    name: Mapped[str] = mapped_column(Text, nullable=False)
    
    description: Mapped[str|None] = mapped_column(Text, nullable=True) 
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Task(Base):
    __tablename__  = "tasks"

    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) > 0",
            name="tasks_title_check",
        ),
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')",
            name="tasks_status_check",
        ),
        ForeignKeyConstraint(
            ["epic_id", "category_id"],
            ["epics.id", "epics.category_id"],
            name="tasks_epic_id_category_id_fkey"
        ),
        Index("tasks_category_id_idx", "category_id"),
        Index("tasks_epic_id_idx", "epic_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)

    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id", name="tasks_category_id_fkey"), 
                                             nullable=False)

    epic_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True)
    
    title: Mapped[str] = mapped_column(Text, nullable=False)

    description: Mapped[str|None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(Text, server_default=text("'todo'"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
