Here's a simple implementation of a Task Tracker CLI application in Python. This application meets the requirements you've outlined, including adding, updating, deleting tasks, and managing their statuses. It uses a JSON file to store tasks and handles user inputs via command-line arguments.

### Task Tracker CLI Implementation

1. **Set Up Your Development Environment**
   - Make sure you have Python installed on your system.
   - Create a new directory for your project.

2. **Create the Python Script**

Create a file named `task_tracker.py` in your project directory and add the following code:

```python
import json
import os
import sys
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')

# Update a task
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

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f'Task {task_id} deleted successfully.')

# Mark a task as in progress
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

# Mark a task as done
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

# List all tasks
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")

# Main function to handle command line arguments
def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Usage: task-cli add <description>")
            return
        add_task(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> <new_description>")
            return
        update_task(int(sys.argv[2]), sys.argv[3])
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            return
        delete_task(int(sys.argv[2]))
    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <id>")
            return
        mark_in_progress(int(sys.argv[2]))
    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <id>")
            return
        mark_done(int(sys.argv[2]))
    elif command == 'list':
        if len(sys.argv) == 3