import json
import os
import sys
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    max_id = max((task['id'] for task in tasks), default=0)
    task_id = max_id + 1
    now = datetime.now().isoformat()
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': now,
        'updatedAt': now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} updated successfully.')
            return
    print(f'Task {task_id} not found.')

def delete_task(task_id):
    tasks = load_tasks()
    found = False
    new_tasks = []
    for task in tasks:
        if task['id'] == task_id:
            found = True
        else:
            new_tasks.append(task)
    if not found:
        print(f'Task {task_id} not found.')
    else:
        save_tasks(new_tasks)
        print(f'Task {task_id} deleted successfully.')

def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'in-progress'
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} marked as in progress.')
            return
    print(f'Task {task_id} not found.')

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'done'
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} marked as done.')
            return
    print(f'Task {task_id} not found.')

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        allowed_status = {'todo', 'in-progress', 'done'}
        if status not in allowed_status:
            print(f"Invalid status '{status}'. Valid options: todo, in-progress, done")
            return
        tasks = [task for task in tasks if task['status'] == status]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        return

    command = sys.argv[1]

    def parse_id(s):
        try:
            return int(s)
        except ValueError:
            print("Error: id must be an integer.")
            sys.exit(1)

    if command == 'add':
        if len(sys.argv) < 3:
            print("Usage: task-cli add <description>")
            return
        add_task(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> <new_description>")
            return
        update_task(parse_id(sys.argv[2]), sys.argv[3])
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            return
        delete_task(parse_id(sys.argv[2]))
    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <id>")
            return
        mark_in_progress(parse_id(sys.argv[2]))
    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <id>")
            return
        mark_done(parse_id(sys.argv[2]))
    elif command == 'list':
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print(f"Unknown command: {command}")
        print("Commands: add, update, delete, mark-in-progress, mark-done, list")

if __name__ == '__main__':
    main()

