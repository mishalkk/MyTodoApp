# Project instructions

## Working agreement

- The project name is MyTodo.

- Default to explaining steps and providing examples. Edit project files when the user authorizes edits.
- Always check proposed changes and recommendations for obvious security vulnerabilities. Explain concrete findings and choose secure defaults without turning routine work into an approval checklist.
- Pay particular attention to published container ports, authentication and authorization, database privileges, secrets in code or logs, SQL injection, and user ownership checks on data access.
- Keep PostgreSQL unpublished to the host when only containers need access. If host access is necessary for local development, bind explicitly to loopback rather than all interfaces, and explain the remaining local access.
- Use a regular application database login for FastAPI. Keep administrator credentials separate from application configuration.
- Use parameterized database queries and never commit real credentials. Preserve .env exclusions and use placeholder values in example configuration.
- Report relevant existing security concerns discovered during work. Do not change unrelated deployment settings without authorization; check reverse proxy dependencies before changing port bindings.

## Current direction

- Build a personal todo application using PostgreSQL, a Python FastAPI backend, and n8n for Telegram integration.
- See docs/backend-plan.md for the agreed backend plan. Use SQLAlchemy models and Alembic migrations to manage schema changes; do not create tables on every API startup.
- Categories contain epics and/or tasks directly. Epics belong to one category. Tasks always belong to a category and optionally to an epic in that same category; preserve database enforcement of this relationship.
- The user created and tested categories, epics, and tasks in PostgreSQL. Verify the live database before migrations and preserve existing data and volumes.
- The user has run the FastAPI health endpoint locally. Next, configure database connectivity and migration baselining, then implement category create/list endpoints before epics and tasks.
- Preserve the current database name unless an explicit migration is planned.

## Telegram integration plan

These are planned behaviors, not a verified description of a deployed workflow. The user previously reported adding a Telegram Trigger; inspect the current workflow and n8n version before implementing changes.

- `/start` or `/menu` introduces MyTodo and sends List, Add, Complete, and Remove buttons.
- Inline keyboard callback values: `todo:list`, `todo:add`, `todo:complete`, `todo:remove`.
- Listen for Message and Callback Query updates. Each incoming update starts a separate workflow execution; acknowledge callback events with Telegram's Answer Query operation.
- List returns the user's open tasks in the current chat, with a friendly empty-list message when there are none.
- Add asks for task text and persists pending conversation state keyed by chat ID and user ID. The next text message creates the task and clears the pending state.
- Complete offers `todo:complete:<id>` buttons and records completion without deleting the task.
- Remove offers `todo:delete:<id>` buttons. Scope deletion by task ID, owning chat ID, and user ID.
- `/cancel` clears the user's pending input state in the current chat.
- Scope reads and mutations by owning chat and user for Telegram personal lists, including in group chats. Shared lists require a separate design. Add ownership fields and authorization before serving multiple users; the initial category/epic/task schema does not yet establish this isolation.
- Prefer n8n calling the FastAPI application endpoints for task operations as the backend is introduced.
- Completion timestamps, due dates, reminders, tags, priorities, and sprints remain future enhancements.
