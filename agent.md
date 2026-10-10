# MyTodo — Progress

Updated: 2026-10-11

## Goal
Build MyTodo, a general-purpose personal todo bot in Telegram using n8n and PostgreSQL. Tasks can cover errands, work, study, projects, or anything else.

## Working agreement
- The project name is MyTodo.
- The user authorized repository edits for this pivot. After this task, default to instructions and examples instead of editing files unless the user authorizes further edits.

## Confirmed setup
- n8n is running locally on the user's PC.
- PostgreSQL is running locally on the user's PC.
- A Telegram Trigger has already been added in n8n.
- No workflow or database configuration has been inspected in this chat.

## Planned behavior
- `/start` or `/menu` introduces MyTodo and sends a menu with List, Add, Complete, and Remove buttons.
- Inline keyboard callback values: `todo:list`, `todo:add`, `todo:complete`, `todo:remove`.
- The Telegram Trigger listens for Message and Callback Query updates.
- Each incoming update starts a separate workflow execution.
- Callback events are acknowledged with Telegram's Answer Query operation.
- List reads the user's open tasks in this chat from PostgreSQL and sends them back, with a friendly empty-list message when there are none.
- Add asks for task text; save pending conversation state in PostgreSQL keyed by chat ID and user ID. The next text message inserts the task and clears the pending state.
- Complete shows a button for each open task using `todo:complete:<id>` and records completion without deleting the task.
- Remove can show a button for each task, using `todo:delete:<id>` as callback data. Delete only where task ID, owning chat ID, and user ID match.
- `/cancel` clears the user's pending input state in this chat.
- Use parameterized SQL and scope reads and mutations by chat ID and user ID. The initial scope is personal lists, including in group chats; shared lists can be added later.
- Store task text, creation time, and optional completion time. Due dates, reminders, tags, and priorities are future enhancements.

## Next step
Configure and test the inline keyboard menu and callback routing before implementing PostgreSQL operations.

## Open implementation details
- Installed n8n version and actual workflow node names.
- PostgreSQL connection credentials and schema.
- Whether to rename the existing PostgreSQL database; retain its current name until an explicit migration is planned.
