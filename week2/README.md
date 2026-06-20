# Week 2 Project: Expense Tracker

A command-line interface (CLI) application in Python designed to demonstrate numerical accumulation, state preservation, error handling, and Sentinel-controlled loop structures.

---

## Core Learning Concepts Implemented

### 1. The Volatile Trap (RAM vs. Disk)
RAM is volatile memory. If your program halts or crashes, all in-memory variables are wiped. To secure "financial truth," this project implements data persistence (serialization) by saving state to `expenses.json` in real-time.
```python
# State loaded at startup
data = load_expenses()
total = data["total"]
```

### 2. The Accumulator Pattern
Accumulating numerical data values across a lifecycle. The `total` state variable must be initialized **outside** the loop, otherwise it would reset on every iteration.
```python
# Initialized outside loop: total = 0.0
# Accumulator inside processing logic:
new_total = current_total + amount
```

### 3. Defensive Programming (Digital Poka-Yoke)
Preventing software crashes due to garbage inputs (e.g. typing `"ten"` instead of `10`). We use `try...except ValueError` blocks to intercept type conversion issues before they bubble up and crash the application thread.
```python
try:
    amount = float(input_str)
except ValueError:
    raise ValueError("Not a valid number.")
```

### 4. Sentinel Value & Graceful Shutdown
Using a specific value (in this case, `'quit'`) as a loop "Kill Switch" to safely exit the continuous execution cycle and display final audit aggregates.
```python
if user_input.lower() == "quit":
    # Break loop and display final total
```

### 5. Decoupling the Architecture
As instructed in the system blueprint:
* **Model**: Handles calculations, float conversions, positive validations, and JSON persistence. Does not contain print statements.
* **View/Controller**: Handles menu rendering, prompt loops, error handling messaging, and outputting report details.

---

## How to Run the Program

1. Open your terminal.
2. Navigate to the project directory:
   ```bash
   cd week2
   ```
3. Run the application:
   ```bash
   python tracker.py
   ```
4. Run the unit tests:
   ```bash
   python test_tracker.py
   ```
