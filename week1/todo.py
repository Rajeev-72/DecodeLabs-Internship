"""
DecodeLabs To-Do List Application - Week 1 Project

This application demonstrates Python Data Management fundamentals:
1. Lists: Storing multiple items in a single variable (`tasks = []`).
2. append(): Appending data to the list.
3. Loops: Iterating over the list to display data.
4. Dictionaries: Representing data rows (similar to database rows).
5. IPO Model: Input -> Process -> Output.
"""

import json
import os

# File name for data persistence
DATA_FILE = "tasks.json"

def load_tasks():
    """
    Process (Input from Storage): Load tasks from the JSON file.
    If the file doesn't exist, start with an empty list.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("\n[!] Warning: Data file was corrupted. Starting with an empty task list.")
            return []
    return []

def save_tasks(tasks):
    """
    Process (Output to Storage): Save the current tasks list to a JSON file.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"\n[!] Error saving tasks: {e}")

def display_menu():
    """
    Output: Print the menu options to the user.
    """
    print("\n" + "=" * 40)
    print("      DECODELABS TO-DO LIST MANAGER      ")
    print("=" * 40)
    print("1. View Tasks")
    print("2. Add a New Task")
    print("3. Mark Task as Completed")
    print("4. Delete a Task")
    print("5. Exit")
    print("=" * 40)

def view_tasks(tasks):
    """
    Output: Iterate through the tasks list and print them.
    Fulfills the loop requirement:
        for task in tasks:
            print(task)
    """
    print("\n" + "-" * 40)
    print("               YOUR TASKS               ")
    print("-" * 40)
    
    if not tasks:
        print("No tasks found! Your list is currently empty.")
        print("-" * 40)
        return

    # Loop through the list of tasks. We use enumerate to show a 1-based index.
    for index, task in enumerate(tasks, 1):
        # Determine status marker
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{index}. {status} {task['task']} (ID: {task['id']})")
    
    print("-" * 40)

def add_task(tasks):
    """
    Input: Accept a task title from the user.
    Process: Create a task dictionary (representing a database row) 
             and append it to the tasks list.
    """
    print("\n--- Add a New Task ---")
    task_title = input("Enter task name: ").strip()
    
    if not task_title:
        print("[!] Task name cannot be empty.")
        return

    # Find the next ID (mimicking auto-increment in a database)
    next_id = max([t["id"] for t in tasks], default=0) + 1

    # Dictionary representing a Database Row
    new_task = {
        "id": next_id,
        "task": task_title,
        "completed": False
    }

    # Process: Append the dictionary to the tasks list (mimicking a database table)
    tasks.append(new_task)
    
    # Save the updated list to the JSON file
    save_tasks(tasks)
    
    print(f"\n[SUCCESS] Successfully added task: '{task_title}'")

def mark_task_completed(tasks):
    """
    Input: Accept a task index/ID.
    Process: Update the completion status of the task.
    """
    if not tasks:
        print("\n[!] No tasks to mark as completed.")
        return

    view_tasks(tasks)
    
    try:
        choice = int(input("\nEnter the number of the task to mark as completed: "))
        if 1 <= choice <= len(tasks):
            tasks[choice - 1]["completed"] = True
            save_tasks(tasks)
            print(f"\n[SUCCESS] Task '{tasks[choice - 1]['task']}' marked as completed!")
        else:
            print("[!] Invalid task number.")
    except ValueError:
        print("[!] Please enter a valid number.")

def delete_task(tasks):
    """
    Input: Accept a task index/ID.
    Process: Remove the selected task from the list.
    """
    if not tasks:
        print("\n[!] No tasks to delete.")
        return

    view_tasks(tasks)
    
    try:
        choice = int(input("\nEnter the number of the task to delete: "))
        if 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            save_tasks(tasks)
            print(f"\n[SUCCESS] Deleted task: '{removed['task']}'")
        else:
            print("[!] Invalid task number.")
    except ValueError:
        print("[!] Please enter a valid number.")

def main():
    """
    Main controller coordinating Input, Process, and Output.
    """
    # Initialize the tasks list (mimicking database table structure)
    tasks = load_tasks()

    while True:
        display_menu()
        user_choice = input("Select an option (1-5): ").strip()

        if user_choice == "1":
            view_tasks(tasks)
        elif user_choice == "2":
            add_task(tasks)
        elif user_choice == "3":
            mark_task_completed(tasks)
        elif user_choice == "4":
            delete_task(tasks)
        elif user_choice == "5":
            print("\nThank you for using DecodeLabs To-Do List Manager. Goodbye!")
            break
        else:
            print("\n[!] Invalid selection. Please choose an option between 1 and 5.")

if __name__ == "__main__":
    main()
