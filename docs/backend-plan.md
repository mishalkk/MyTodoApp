# Backend and database plan

Agreed on 2026-10-15. This is a plan; the Python backend has not been implemented.

## Goal

Add a Python FastAPI backend backed by PostgreSQL. Manage schema changes through SQLAlchemy models and Alembic migrations rather than manual SQL or creating tables on every API startup.

## Domain

- A category contains epics and/or tasks directly.
- An epic belongs to one category and contains tasks.
- A task always belongs to a category and optionally to an epic.
- When a task references an epic, both must belong to the same category. Preserve the composite foreign key enforcing this.
- Current task statuses: todo, in_progress, done.
- Sprints, priorities, and due dates are future work.

## Responsibilities

- Docker Compose starts PostgreSQL, n8n, and eventually the API.
- PostgreSQL's POSTGRES_USER initializes an administrator on first startup with an empty data volume. FastAPI must use a separate regular application login, todo_app.
- An initialization script will provision the application login and appropriate database access for fresh installations. Changing initialization scripts or environment variables does not update an existing database volume.
- SQLAlchemy defines the application's database models.
- Alembic migrations create and evolve tables, constraints, and indexes. Run migrations as an explicit deployment step before starting the API, not independently in every API worker.
- Keep administrator credentials out of the API configuration. Decide whether migrations use the application owner or a separate migration role before implementation.
- The persistent postgres_data volume preserves database roles, schema, and data across container recreation.
- A schema-only dump is a reference/export, not the future source of schema initialization. Avoid running both schema.sql and an initial migration to create the same tables.

## Existing database

The user created categories, epics, and tasks interactively. The shared schema export includes identity primary keys, checks, indexes, category foreign keys, and the composite task-to-epic foreign key. The user confirmed tests allowing direct category tasks and epic tasks, and rejecting a category/epic mismatch.

Before making changes, verify the live schema and roles, confirm the test transaction was rolled back, and back up any data to preserve. A dump was pasted in chat; no db/schema.sql file was found in the project when this plan was saved.

Create an initial Alembic migration that can build a fresh database. Compare the existing schema with that migration before stamping the existing database at the baseline revision. Stamping records a revision without executing its migration; do not stamp an unverified or mismatched schema.

## Implementation order

1. Inspect the running database, ownership, privileges, and active Compose volume. Confirm any data to retain.
2. Scaffold the Python backend with FastAPI, SQLAlchemy, a PostgreSQL driver, and Alembic. Provide configuration examples without committing secrets.
3. Model the existing schema and create the initial migration. Verify it on a fresh disposable database, then baseline the existing database after checking it matches.
4. Add fresh-install role provisioning, a PostgreSQL health check, API container configuration, and an explicit migration step to Compose. Preserve existing volumes.
5. Implement category create/list endpoints first; then epic and task endpoints. Test database relationship constraints and API error handling.
6. Connect n8n to the API for application operations. Keep n8n's own internal database configuration a separate decision.

## Next discussion

Begin with categories as the first complete API feature: create a category and list categories. Decide how the API will be accessed and authenticated before exposing it outside the local environment. A frontend is not required to begin testing the API.
