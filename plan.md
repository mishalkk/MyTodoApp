# n8n + PostgreSQL deployment plan

This plan covers the changes and checks identified in the review of `compose.yaml`. Implementation is still pending.

## 1. Decide how PostgreSQL will be used

- [ ] Confirm whether PostgreSQL stores game data only, n8n's internal data, or both.
- Current behavior: n8n stores its internal data in SQLite in `n8n_data`. PostgreSQL provides `game_todo_db` independently.
- For game data only, configure an n8n PostgreSQL credential with host `postgres`, port `5432`, database `game_todo_db`, and a dedicated application user.
- If both applications use PostgreSQL, keep their databases and roles separate.

## 2. Secure database credentials and permissions

- [ ] Replace `sample_password` with a strong generated password.
- [ ] Move deployment secrets out of `compose.yaml` into an untracked `.env` file or Docker secrets.
- [ ] Add a `.env.example` containing placeholders and document required variables.
- [ ] Ensure `.env` is excluded from version control.
- [ ] Create a dedicated game application role with only the permissions it needs. Do not use the `root` database superuser in workflow credentials.
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
- [ ] Test restoring into an isolated deployment and verify workflows, saved credentials, and game data.
- [ ] Document that `docker compose down -v` deletes the persistent volumes and must not be used for routine restarts or upgrades.

## 7. Validate the completed setup

- [ ] Run `docker compose config --quiet` to validate the configuration without printing resolved secrets.
- [ ] Start the deployment and confirm PostgreSQL readiness and clean n8n startup logs.
- [ ] Confirm the n8n editor is reachable through HTTPS.
- [ ] Execute an n8n workflow that reads and writes test game data using the restricted database role.
- [ ] If PostgreSQL is n8n's backend, verify n8n is actually using it.
- [ ] Test a webhook through the public URL and confirm its generated URL is correct.
- [ ] Restart/recreate containers without deleting volumes and verify data and credentials persist.
- [ ] Complete the isolated restore test before declaring the deployment ready.

## References

- [Official n8n PostgreSQL Compose example](https://github.com/n8n-io/n8n-hosting/blob/main/docker-compose/withPostgres/docker-compose.yml)
- [n8n Docker persistence guidance](https://github.com/n8n-io/n8n/blob/master/docker/images/n8n/README.md)
