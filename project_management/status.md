# Project Status

## Task Counter

8

<!-- Reset by architecture health check — 2026-04-02 -->

Project tasks are managed centrally via the personal assistant CLI:

    /home/payson/Documents/repos/self/personal-assistant/scripts/project_tasks_cli.py

To manipulate status as described by a prompt, use the below commands to add/remove/modify a task. Before modification, ensure you have the correct task first via listing all tasks.

Commands:
- `project_tasks_cli.py list floor` — list open tasks
- `project_tasks_cli.py add floor "<name>" [--severity S] [--difficulty D] [--value V]` — add a task
- `project_tasks_cli.py complete floor <task_id>` — mark done
- `project_tasks_cli.py update floor <task_id> [--name N] [--severity S] [--difficulty D]  [--value V]` — update
- `project_tasks_cli.py delete floor <task_id>` — delete

