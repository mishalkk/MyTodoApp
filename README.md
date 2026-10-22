# MyTodo

A fun little personal project I’m building in my spare time to experiment and learn. Nothing too serious—just a task manager that can grow with whatever ideas I want to try next.

The backend uses FastAPI and PostgreSQL, with n8n as the integration layer. n8n gives me room to connect MyTodo to other tools and take the project in different directions.

The first idea is a simple Telegram integration: add new tasks and check my task list throughout the day, without needing an elaborate frontend. Later, I’d like to connect Google Calendar and Google Drive and explore what else I can build around them.

## Technology stack

- Python 3.12+ and FastAPI — backend API
- SQLAlchemy — database models and queries
- Alembic — database migrations
- PostgreSQL 16 — application data
- n8n — workflow automation and integrations
- Docker Compose — local service management

## Data model

- A category contains epics and/or tasks directly.
- An epic belongs to one category.
- A task requires a category and may belong to an epic in that category.
- Task statuses are `todo`, `in_progress`, and `done`.

A composite foreign key ensures that a task and its epic belong to the same category.

## Current status

Implemented:

- Backend and Docker Compose configuration, including n8n
- Database connection and health endpoints
- Category, epic, and task models
- Initial Alembic migration

Planned:

- Category create/list endpoints, followed by epic and task endpoints
- Telegram actions for listing, adding, completing, and removing tasks
- Google Calendar and Google Drive integrations
- Later enhancements such as priorities, due dates, reminders, and tags

## Running the backend

The current setup requires Docker Compose, an existing configured database, and a root `.env` file containing:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `DB_HOST`, `DB_PORT`
- `APP_DB_NAME`, `APP_DB_USER`, `APP_DB_PASSWORD`

Inside Docker Compose, use `postgres` as the database host and `5432` as the port. Use a regular database login for the backend and keep administrator credentials separate. Do not commit `.env`.

From the project root:

```powershell
docker compose up -d postgres
docker compose up -d --build backend
```

Once PostgreSQL is ready, open:

- [API documentation](http://localhost:8000/docs)
- [API health](http://localhost:8000/health)
- [Database connectivity](http://localhost:8000/health/db)

Rebuild the backend after source changes; the current configuration does not mount local source files into the container.

Fresh-install database role provisioning is not yet automated.

## Database migrations

Schema changes are managed explicitly with Alembic, rather than during API startup.

Follow this workflow:

1. Update the SQLAlchemy models.
2. Autogenerate a migration.
3. Review the generated migration.
4. Apply it with Alembic.

Keep migration files in version control. When generating migrations inside a container, ensure the files are saved back to the host repository.

Existing databases created before Alembic require schema verification before stamping a baseline. Do not run the initial migration against existing unversioned tables. Fresh-database execution of the initial migration has not yet been verified.

Preserve existing database volumes.

## Deployment notes

The current scope is personal, single-user use. The backend binds to localhost, and PostgreSQL has no published host port.

The n8n configuration includes deployment-specific reverse proxy URLs and publishes port 5678 on all host interfaces. Review its network access and proxy configuration before deploying elsewhere.

## Further reading

See [the backend plan](docs/backend-plan.md) for architecture details and the implementation sequence.

## A personal note: where this might go

MyTodo starts as a simple task manager, but this little repository also gives me a place to explore ideas as my interests and the technology around me evolve.

One idea I’d love to try is an experience and skill tree system inspired by Skyrim. As I spend time doing things, I could gain experience in different categories and gradually develop my own skill trees. It could be a playful way to reflect on what I actually spend time on, which interests keep coming back, and which skills I want to develop next.

That wouldn’t be an objective measure of who I am or what I should become—just another way to notice patterns and ask myself better questions.

It’s a slightly silly idea, and that’s part of the fun. As AI, automation, and other tools make new things possible, I want to keep experimenting and gradually bring some of those possibilities into this application.

The name might change. The scope might change completely. The immediate goal is still to build a useful personal task manager, but the broader purpose of this repository is to document what I’m trying, what I’m learning, and what new tools enable me to create.

If you’re reading this—whether you’re a person browsing my GitHub or an AI trying to make sense of this project—that’s the thread connecting it all: a personal experiment that grows with me, with room for whatever crazy idea comes next.
