# Backend and database plan

## Architecture

MyTodo uses FastAPI, SQLAlchemy, Alembic, PostgreSQL, and n8n. Docker Compose runs the services. The backend is published on localhost; PostgreSQL is accessed through the Compose network without a published database port.

- A category contains epics and/or direct tasks.
- An epic belongs to one category and contains tasks.
- A task requires a category and optionally belongs to an epic in that category.
- A composite foreign key enforces task/epic category consistency.
- Task statuses are todo, in_progress, and done.

## Database management

- PostgreSQL initialization provisions its administrator and database only when the data volume is empty. Fresh-install regular-role provisioning remains to be implemented.
- Application code uses a regular database login supplied through environment configuration. Never store credentials in source or migration files.
- SQLAlchemy models describe the schema. Alembic migrations create and evolve it as an explicit deployment step rather than on every API worker startup.
- Keep migration files in version control. A schema dump can be a reference, but avoid using both it and the initial migration to create the same tables.
- The initial revision is 0421cc4d5ed1. For an existing database, verify schema compatibility before stamping the baseline. For an empty database, apply migrations normally.
- Fresh-database execution of the initial migration has not yet been verified. Do not claim that a model/database comparison tests the migration itself.
- Future schema changes follow models -> autogenerate -> review -> upgrade. Preserve existing data and volumes.

## Implementation sequence

1. Backend/container setup, database connection, and health endpoints.
2. Category, epic, and task models and initial migration baseline.
3. Request-scoped database sessions and category request/response schemas.
4. Category create/list endpoints, then epic and task endpoints with relationship error handling.
5. n8n integration through the API; n8n's own internal database configuration is a separate concern.
6. Fresh-install provisioning and deployment readiness, including PostgreSQL health checks and explicit migration execution.

Current scope is single-user. Authentication and ownership need to be designed before expanding access. Sprints, priorities, and due dates are future work.
