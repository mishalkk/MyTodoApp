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
3. Request-scoped database sessions and category/epic request-response schemas. **Completed.**
4. Category and epic create/list endpoints, then task endpoints with relationship error handling. Category and epic APIs are **completed and user-verified**; task APIs are next.
5. Automated fresh-install provisioning and deployment readiness, after the category, epic, and task APIs are in place (see below).
6. n8n integration through the API; n8n's own internal database configuration is a separate concern.

## Automated deployment (after API implementation)

Goal: after supplying server configuration and secrets, `docker compose up` initializes a fresh installation and starts the application without manual table creation.

- Wait for PostgreSQL readiness using a health check.
- Provision a regular application database login, keeping administrator credentials separate from backend configuration. Preserve existing database names, roles, data, and volumes on established installations.
- Run `alembic upgrade head` in a one-off migration service to create tables on a fresh database or apply pending migrations to an already versioned database.
- Start the backend only after provisioning and migrations succeed; do not run table creation in each API worker.
- Verify the initial migration against an isolated empty test database before declaring fresh deployment ready. Existing unversioned databases still require a verified baseline rather than automatic stamping.
- Keep PostgreSQL unpublished. Before server deployment, review the n8n reverse-proxy setup and replace the current public `5678:5678` binding with either a loopback-only binding or no host binding, as appropriate for that proxy. Do not make this port change before verifying the proxy dependency.

Defer this deployment work until the task APIs are implemented; the immediate focus is task request/response schemas and endpoints.

Current scope is single-user. Authentication and ownership need to be designed before expanding access. Sprints, priorities, and due dates are future work.
