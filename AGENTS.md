# MyTodo project instructions

## Local instructions

If AGENTS.local.md exists, read it for additional local working preferences and context. It is optional and excluded from Git. Keep personal preferences and conversation handoffs out of public project documentation.

## Architecture

- MyTodo uses FastAPI, SQLAlchemy, Alembic, PostgreSQL, and n8n for Telegram integration.
- Read docs/backend-plan.md for the architecture and implementation sequence.
- Categories contain epics and/or direct tasks. Each epic belongs to one category. Each task requires a category and optionally an epic in the same category. Preserve the composite foreign key enforcing this rule.
- Manage schema changes through models and Alembic migrations; do not create tables on every API startup.
- Use the normal models -> autogenerate -> review -> upgrade workflow. Existing databases that predate migrations require a verified baseline rather than recreating their tables.
- Preserve database names, existing volumes, and unrelated local changes. Do not reset or overwrite them as part of setup.
- Track migration files in Git. Keep dependencies in backend/pyproject.toml.

## Security

- Check proposed changes and recommendations for obvious vulnerabilities, especially exposed ports, authentication, authorization, database privileges, secrets, and SQL injection. Report concrete findings and use secure defaults.
- Keep PostgreSQL unpublished when only containers need access. Bind explicitly to loopback if local host access is necessary.
- Use a regular database login for the backend; keep administrator credentials separate.
- Use parameterized queries. Never commit real credentials or expose them in logs or errors. Preserve .env exclusions and use placeholders in examples.
- Check reverse proxy dependencies before changing existing port bindings. Avoid unrelated deployment changes.
- Add authorization and data ownership enforcement before enabling multiple users or expanding access beyond the current single-user scope.

## Application work

- Build category create/list endpoints first, followed by epics and tasks. Prefer n8n calling FastAPI for application operations.
- Sprints, priorities, due dates, reminders, and tags are later enhancements.
- Telegram workflow behavior must be verified before changing it. Planned menu actions are list, add, complete, and remove; acknowledge callback queries and persist pending input state when that flow is implemented.
