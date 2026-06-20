"""
DecodeLabs To-Do List Application - Week 1 Project

This application demonstrates Python Data Management fundamentals:
1. Lists: Storing multiple items in a single variable (`tasks = []`).
2. append(): Appending data to the list.
3. Loops: Iterating over the list to display data.
4. Dictionaries: Representing data rows (similar to database rows).
5. IPO Model: Input -> Process -> Output.
6. Decoupled Architecture (Model-View Separation): 
   - Model (Data Logic): pure functions that modify data structures.
   - View/Controller (User Interface): handles user inputs and printing.
"""

import json
import os

# File name for data persistence
DATA_FILE = "tasks.json"

# =====================================================================
# MODEL: DATA LOGIC (No print or input statements here)
# =====================================================================

def load_tasks(filepath=DATA_FILE):
    """
    Load tasks from a JSON file.
    If the file doesn't exist or is corrupted, return an empty list.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks, filepath=DATA_FILE):
    """
    Save the task list to a JSON file.
    """
    with open(filepath, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task_to_list(tasks, task_title):
    """
    Adds a new task to the list using append().
    Each task is a dictionary representing a Database Row.
    Returns the newly created task.
    """
    if not task_title:
        raise ValueError("Task name cannot be empty.")

    # Auto-incrementing ID (mimics SQL Primary Key)
    next_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "task": task_title,
        "completed": False
    }

    # Fulfills list.append() requirement
    tasks.append(new_task)
    return new_task

def mark_task_status(tasks, index_1based, completed=True):
    """
    Modifies the status of a task at a given 1-based index.
    Returns the modified task.
    """
    if not (1 <= index_1based <= len(tasks)):
        raise IndexError("Invalid task index.")
    
    tasks[index_1based - 1]["completed"] = completed
    return tasks[index_1based - 1]

def delete_task_from_list(tasks, index_1based):
    """
    Removes a task from the list at a given 1-based index.
    Returns the deleted task.
    """
    if not (1 <= index_1based <= len(tasks)):
        raise IndexError("Invalid task index.")
    
    return tasks.pop(index_1based - 1)

# =====================================================================
# VIEW & CONTROLLER: USER INTERFACE (Handles inputs and displays)
# =====================================================================

def display_menu():
    print("\n" + "=" * 40)
    print("      DECODELABS TO-DO LIST MANAGER      ")
    print("=" * 40)
    print("1. View Tasks")
    print("2. Add a New Task")
    print("3. Mark Task as Completed")
    print("4. Delete a Task")
    print("5. Exit")
    print("=" * 40)

def show_tasks(tasks):
    print("\n" + "-" * 40)
    print("               YOUR TASKS               ")
    print("-" * 40)
    
    if not tasks:
        print("No tasks found! Your list is currently empty.")
        print("-" * 40)
        return

    # Fulfills enumerate() requirement (Professional Polish)
    for index, task in enumerate(tasks, 1):
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{index}. {status} {task['task']} (ID: {task['id']})")
    
    print("-" * 40)

def ui_add_task(tasks):
    print("\n--- Add a New Task ---")
    task_title = input("Enter task name: ").strip()
    try:
        new_task = add_task_to_list(tasks, task_title)
        save_tasks(tasks)
        print(f"\n[SUCCESS] Successfully added task: '{new_task['task']}'")
    except ValueError as e:
        print(f"\n[!] Error: {e}")

def ui_mark_task_completed(tasks):
    if not tasks:
        print("\n[!] No tasks to mark as completed.")
        return

    show_tasks(tasks)
    try:
        choice = int(input("\nEnter the task number to mark as completed: "))
        completed_task = mark_task_status(tasks, choice, completed=True)
        save_tasks(tasks)
        print(f"\n[SUCCESS] Task '{completed_task['task']}' marked as completed!")
    except (ValueError, IndexError) as e:
        print(f"\n[!] Error: Please enter a valid task number.")

def ui_delete_task(tasks):
    if not tasks:
        print("\n[!] No tasks to delete.")
        return

    show_tasks(tasks)
    try:
        choice = int(input("\nEnter the task number to delete: "))
        removed_task = delete_task_from_list(tasks, choice)
        save_tasks(tasks)
        print(f"\n[SUCCESS] Deleted task: '{removed_task['task']}'")
    except (ValueError, IndexError) as e:
        print(f"\n[!] Error: Please enter a valid task number.")

def main():
    # Initialize the tasks list (representing a database table)
    tasks = load_tasks()

    while True:
        display_menu()
        user_choice = input("Select an option (1-5): ").strip()

        if user_choice == "1":
            show_tasks(tasks)
        elif user_choice == "2":
            ui_add_task(tasks)
        elif user_choice == "3":
            ui_mark_task_completed(tasks)
        elif user_choice == "4":
            ui_delete_task(tasks)
        elif user_choice == "5":
            print("\nThank you for using DecodeLabs To-Do List Manager. Goodbye!")
            break
        else:
            print("\n[!] Invalid selection. Please choose an option between 1 and 5.")

if __name__ == "__main__":
    main()
