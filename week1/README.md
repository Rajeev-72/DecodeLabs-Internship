# Week 1 Project: To-Do List Application

A command-line interface (CLI) application in Python designed to demonstrate the fundamentals of in-memory data management, list manipulation, and data structures.

---

## Core Learning Concepts Implemented

### 1. Lists (`tasks = []`)
A **List** in Python is a built-in data type that can hold multiple ordered items in a single variable. In this project, the list `tasks` represents our "database table".
```python
# Initialized as an empty list at start
tasks = []
```

### 2. The `.append()` Method
The `.append()` method adds an element to the end of a list. In our code, when the user inputs a task, it is processed and appended to the `tasks` list.
```python
# Adding a task to the list
tasks.append(new_task)
```

### 3. Iteration Loops
To display the list of tasks back to the user, we iterate through the list using a `for` loop. This avoids hardcoding indices and ensures we can display any number of tasks dynamically.
```python
# Displaying all tasks
for index, task in enumerate(tasks, 1):
    status = "[X]" if task["completed"] else "[ ]"
    print(f"{index}. {status} {task['task']}")
```

### 4. Input-Process-Output (IPO) Model
This application is structured around the classical **IPO model** used in software engineering:
* **Input**: The user inputs options from the menu and details for a new task using `input()`.
* **Process**: The program processes this input by appending it to the `tasks` list, updating a task's status, or removing a task, and then saves it to `tasks.json`.
* **Output**: The program outputs formatted text, lists, and status updates back to the screen.

### 5. Dictionaries as Database Rows
To prepare you for backend and database development, each task is modeled as a Python dictionary. 
* A **Dictionary** behaves like a **Database Row** (storing key-value pairs representing a single record).
* A **List** behaves like a **Database Table** (storing a collection of rows).

**Example Database Table representation in our program:**
```python
tasks = [
    {"id": 1, "task": "Finish Python assignment", "completed": False},
    {"id": 2, "task": "Submit internship report", "completed": True}
]
```

---

## Features
- **Add Tasks**: Enter any task string; the program assigns it an auto-incrementing ID, creates a task dictionary, and appends it to the list.
- **View Tasks**: Display all tasks with their completion status (`[ ]` or `[X]`) in a clean text table.
- **Complete Tasks**: Mark tasks as done.
- **Delete Tasks**: Remove tasks from the list.
- **Persistent Storage**: Saves the task list to `tasks.json` in the background so tasks are preserved across program runs.

---

## How to Run the Program

1. Ensure you have Python 3 installed.
2. Open your terminal or command prompt.
3. Navigate to the project directory:
   ```bash
   cd week1
   ```
4. Run the script:
   ```bash
   python todo.py
   ```
