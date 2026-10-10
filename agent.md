# Telegram Todo App — Progress

Updated: 2026-10-10

## Goal
Build a Telegram todo bot for fun using n8n and PostgreSQL.

## Confirmed setup
- n8n is running locally on the user's PC.
- PostgreSQL is running locally on the user's PC.
- A Telegram Trigger has already been added in n8n.
- No workflow or database configuration has been inspected in this chat.

## Planned behavior
- `/start` or `/menu` sends a menu with List, Add, and Remove buttons.
- Inline keyboard callback values: `todo:list`, `todo:add`, `todo:remove`.
- The Telegram Trigger listens for Message and Callback Query updates.
- Each incoming update starts a separate workflow execution.
- Callback events are acknowledged with Telegram's Answer Query operation.
- List reads this chat's todos from PostgreSQL and sends them back.
- Add asks for task text; save pending conversation state in PostgreSQL keyed by chat ID and user ID. The next text message inserts the task and clears the pending state.
- Remove can show a button for each task, using `todo:delete:<id>` as callback data. Delete only where both task ID and owning chat ID match.
- Use parameterized SQL and scope todos by chat ID (and user ID if personal lists in group chats are desired).

## Next step
Configure and test the inline keyboard menu and callback routing before implementing PostgreSQL operations.

## Open implementation details
- Installed n8n version and actual workflow node names.
- PostgreSQL connection credentials and schema.
- Whether todo lists are shared per chat or personal per user.
