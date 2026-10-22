FROM python:3.12-slim

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY app ./app

# Copy Alembic migration files
COPY alembic.ini ./
COPY migrations ./migrations

RUN python -m pip install --no-cache-dir .
RUN groupadd --system app && useradd --system --gid app --no-create-home app

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]