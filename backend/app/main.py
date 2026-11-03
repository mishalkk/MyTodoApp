from typing import Annotated

from fastapi import (FastAPI, HTTPException, Depends, Query, status)

from sqlalchemy import text, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine, get_db
from app.models import Category, Epic, Task
from app.schemas import (
    CategoryCreate, CategoryRead,
    EpicCreate, EpicRead, 
    TaskCreate, TaskRead
    )


app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Page to health check Database Connections
@app.get("/health/db")
def db_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code = 503,
            detail      = "Database Unavailable",
        ) from None

    return {"status": "ok"}

# ----------------------------------------------------------------------------------------
# Categories API
# ----------------------------------------------------------------------------------------

@app.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Annotated[Session, Depends(get_db)]):
    category = Category(
        name = payload.name,
        description = payload.description
    )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not create the category",
        ) from None

    return category


@app.get("/categories", response_model=list[CategoryRead])
def get_categories(
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = select(Category).order_by(Category.id).offset(offset).limit(limit)

    try:
        categories = db.scalars(statement).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve categories"
        ) from None

    return categories


# ----------------------------------------------------------------------------------------
# Epic APIs
# ----------------------------------------------------------------------------------------
@app.post("/epics", response_model=EpicRead, status_code=status.HTTP_201_CREATED)
def create_epic(payload: EpicCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        category = db.get(Category, payload.category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        epic = Epic(
            category_id = payload.category_id,
            name = payload.name,
            description = payload.description,
        )

        db.add(epic)
        db.commit()
        db.refresh(epic)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not create the epic"
        ) from None

    return epic


@app.get("/epics", response_model=list[EpicRead])
def get_epics(
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = select(Epic).order_by(Epic.id).offset(offset).limit(limit)

    try:
        epics = db.scalars(statement).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve epics"
        ) from None

    return epics

# ----------------------------------------------------------------------------------------
# Task APIs
# ----------------------------------------------------------------------------------------
@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        # find category
        category = db.get(Category, payload.category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # find epic if its in the input or payload
        if payload.epic_id is not None:
            epic = db.get(Epic, payload.epic_id)

            if epic.category_id != payload.category_id:
                raise HTTPException(status_code=422, detail="Epic does not belong to the specified category")

            if epic is None:
                raise HTTPException(status_code=404, detail="Epic not found")

        task = Task(
            category_id = payload.category_id,
            epic_id = payload.epic_id,
            title = payload.title,
            description = payload.description
        )

        db.add(task)
        db.commit()
        db.refresh(task)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not create the Task"
        )

    return task


@app.get("/tasks", response_model=list[TaskRead])
def get_tasks(
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = select(Task).order_by(Task.id).offset(offset).limit(limit)

    try:
        tasks = db.scalars(statement).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="Could not retrieve epics"
            ) from None

    return tasks