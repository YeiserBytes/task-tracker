import json
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import readline

TASK_FILE = Path("tasks.json")


@dataclass
class Task:
    id: int
    description: str
    status: str = "todo"
    createdAt: str = datetime.now().isoformat()
    updatedAt: str = datetime.now().isoformat()

    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.createdAt:
            self.createdAt = now
        self.updatedAt = now


def load_tasks():
    if not TASK_FILE.exists():
        return []
    with TASK_FILE.open("r") as file:
        return json.load(file)


def save_tasks(tasks):
    with TASK_FILE.open("w") as file:
        json.dump(tasks, file, indent=4)


def generate_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(description: str):
    tasks = load_tasks()
    task = Task(id=generate_id(tasks), description=description)
    tasks.append(asdict(task))
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task.id})")


def update_task(task_id: int, description: str):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task updated successfully (ID: {task_id})")
            return
    print(f"Task with ID {task_id} not found")


def delete_task(task_id: int):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task deleted successfully (ID: {task_id})")


def mark_task(task_id: int, status: str):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status} (ID: {task_id})")
            return
    print(f"Task with ID {task_id} not found")


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    if not tasks:
        print("No tasks found")
    else:
        for task in tasks:
            print(f"[{task['id']}] {task['description']} (Status: {task['status']}, Created: {task['createdAt']})")


def main():
    def completer(text, state):
        options = [cmd for cmd in ["add", "update", "delete", "mark", "list"] if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Description of the task")

    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", type=int, help="ID of the task")
    parser_update.add_argument("description", type=str, help="New description of the task")

    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="ID of the task")

    parser_mark = subparsers.add_parser("mark", help="Mark a task as todo, in-progress, or done")
    parser_mark.add_argument("id", type=int, help="ID of the task")
    parser_mark.add_argument("status", type=str, choices=["todo", "in-progress", "done"], help="New status of the task")

    parser_list = subparsers.add_parser("list", help="List all tasks or tasks with a specific status")
    parser_list.add_argument("status", type=str, nargs="?", help="Status of the tasks to list", choices=["todo", "in-progress", "done"])

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark":
        mark_task(args.id, args.status)
    elif args.command == "list":
        list_tasks(args.status)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
