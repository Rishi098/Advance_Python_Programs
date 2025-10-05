import json
from datetime import datetime

FILE_NAME = "tasks.json"

def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

def show_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return
    print("\n Your Tasks:")
    for i, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "⏳ Pending"
        print(f"{i}. {task['title']} - {status} - Due: {task['due_date']}")
    print()

def add_task(tasks):
    title = input("Enter task title: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    tasks.append({"title": title, "due_date": due_date, "done": False})
    save_tasks(tasks)
    print("Task added!\n")

def mark_done(tasks):
    show_tasks(tasks)
    index = int(input("Enter task number to mark done: ")) - 1
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        print(" Task marked as done!\n")

def delete_task(tasks):
    show_tasks(tasks)
    index = int(input("Enter task number to delete: ")) - 1
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
        print(" Task deleted!\n")

def main():
    tasks = load_tasks()
    while True:
        print("\n=== Task Tracker ===")
        print("1. View Tasks\n2. Add Task\n3. Mark Done\n4. Delete Task\n5. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye ")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
