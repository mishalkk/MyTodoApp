# MyTodo implementation and deployment plan

MyTodo is a general-purpose personal todo bot for Telegram, using n8n and PostgreSQL. This plan covers the application work and deployment checks. Workflow and schema implementation remain pending.

## Application implementation

- [x] Define MyTodo's general-purpose scope and update project documentation.
- [ ] Inspect/export the existing n8n workflow and confirm installed version and node names.
- [ ] Create a tasks table with task ID, Telegram chat ID, Telegram user ID, task text, creation time, and optional completion time.
- [ ] Create a pending-input table keyed by chat ID and user ID for the Add flow.
- [ ] Build `/start` and `/menu` with List, Add, Complete, and Remove buttons.
- [ ] Route Message and Callback Query updates and acknowledge callback queries.
- [ ] Implement List for the current user's open tasks in the current chat, including an empty state.
- [ ] Implement Add: prompt for text, validate nonempty input, insert the task, and clear pending state.
- [ ] Implement Complete: mark a selected task completed and retain its history.
- [ ] Implement Remove for a selected task owned by the requesting user in the current chat.
- [ ] Implement `/cancel` to clear pending state without adding a task.
- [ ] Use parameterized SQL and enforce chat/user ownership on every task read and mutation.
- [ ] Handle stale buttons, missing tasks, repeated completion, and database failures with clear Telegram responses.
- [ ] Verify the full flow with two users, including in a group chat, to check that their lists and input states remain separate.
- Due dates, reminders, tags, priorities, and shared lists are deferred.
- Fresh installations can use `mytodo_db`. Preserve the existing database name and volume until any rename is explicitly planned and backed up.

## 1. Decide how PostgreSQL will be used

- [ ] Confirm whether PostgreSQL stores MyTodo task data only, n8n's internal data, or both.
- Current behavior: n8n stores its internal data in SQLite in `n8n_data`. PostgreSQL provides the application database independently; retain its existing name until a migration is planned.
- For MyTodo task data only, configure an n8n PostgreSQL credential with host `postgres`, port `5432`, the current application database, and a dedicated application user.
- If both applications use PostgreSQL, keep their databases and roles separate.

## 2. Secure database credentials and permissions

- [ ] Replace `sample_password` with a strong generated password.
- [x] Read PostgreSQL credentials from environment variables instead of hardcoding them in `compose.yaml`.
- [ ] Verify the local `.env` contains the correct existing database credentials.
- [ ] Add a `.env.example` containing placeholders and document required variables.
- [x] Ensure `.env` is excluded from version control.
- [ ] Create a dedicated MyTodo application role with only the permissions it needs. Do not use the `root` database superuser in workflow credentials.
- [ ] If n8n uses PostgreSQL for internal storage, create its own database and role with the permissions required for its migrations.
- Existing PostgreSQL volumes retain their original users and passwords: changing `POSTGRES_*` variables does not update an initialized database. Apply role/password changes explicitly and update clients together.

## 3. Configure n8n's PostgreSQL backend, if selected

- [ ] Add `DB_TYPE=postgresdb` and configure `DB_POSTGRESDB_HOST=postgres`, `DB_POSTGRESDB_PORT=5432`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, and `DB_POSTGRESDB_PASSWORD`.
- [ ] If the SQLite instance already contains workflows or credentials, back up and prepare a supported migration before switching databases. Changing the environment variables alone does not migrate existing data.
- [ ] Preserve the existing n8n credential encryption key and `n8n_data` volume.

## 4. Make startup and upgrades predictable

- [ ] Pin n8n to a tested release instead of using the unversioned image.
- [ ] Document the PostgreSQL image update policy; the current `postgres:16` tag remains on major version 16 but can receive minor updates.
- [ ] Add a PostgreSQL healthcheck using `pg_isready` against the configured user and database.
- [ ] If n8n requires PostgreSQL at startup, add `depends_on` with `condition: service_healthy`.
- [ ] Document backup, update, verification, and rollback steps before upgrades.

## 5. Verify HTTPS and proxy routing

- [ ] Confirm the external reverse proxy or tunnel routes `https://n8n.mugenassists.win/` to n8n on port 5678 and provides a valid TLS certificate.
- [ ] Verify `N8N_HOST`, `N8N_PROTOCOL`, `WEBHOOK_URL`, and `N8N_EDITOR_BASE_URL` match the deployed URL.
- [ ] Confirm `N8N_PROXY_HOPS=1` matches the actual number of trusted proxies and that forwarding headers are supplied correctly.
- [ ] Restrict direct access to port 5678 according to the proxy architecture. Use a loopback binding for a proxy on the same host, or a shared Docker network for a containerized proxy where appropriate.
- PostgreSQL currently has no published host port; retain that arrangement unless external database access is needed.

## 6. Back up and test recovery

- [ ] Back up PostgreSQL with a database-aware dump and preserve any roles needed for recovery.
- [ ] Back up `n8n_data`, including the credential encryption key and SQLite database if SQLite remains in use. Take a consistent SQLite backup with n8n stopped or an appropriate database backup method.
- [ ] If setting an explicit `N8N_ENCRYPTION_KEY`, reuse the existing key on an initialized deployment; do not replace it with a new key.
- [ ] Store backups and required secrets securely outside the deployment host, with a documented schedule and retention policy.
- [ ] Test restoring into an isolated deployment and verify workflows, saved credentials, and MyTodo task data.
- [ ] Document that `docker compose down -v` deletes the persistent volumes and must not be used for routine restarts or upgrades.

## 7. Validate the completed setup

- [ ] Run `docker compose config --quiet` to validate the configuration without printing resolved secrets.
- [ ] Start the deployment and confirm PostgreSQL readiness and clean n8n startup logs.
- [ ] Confirm the n8n editor is reachable through HTTPS.
- [ ] Execute an n8n workflow that reads and writes test MyTodo task data using the restricted database role.
- [ ] If PostgreSQL is n8n's backend, verify n8n is actually using it.
- [ ] Test a webhook through the public URL and confirm its generated URL is correct.
- [ ] Restart/recreate containers without deleting volumes and verify data and credentials persist.
- [ ] Complete the isolated restore test before declaring the deployment ready.

## References

- [Official n8n PostgreSQL Compose example](https://github.com/n8n-io/n8n-hosting/blob/main/docker-compose/withPostgres/docker-compose.yml)
- [n8n Docker persistence guidance](https://github.com/n8n-io/n8n/blob/master/docker/images/n8n/README.md)
