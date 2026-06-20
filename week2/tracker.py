"""
DecodeLabs Expense Tracker - Week 2 Project

This application demonstrates Python Data Processing and State management:
1. Accumulator Pattern: Running totals initialized outside the loop (`total = total + expense`).
2. Continuous Loop: Running the program on an infinite execution cycle (`while True:`).
3. Defensive Coding (Poka-Yoke): Using try/except blocks to prevent crashes on invalid inputs.
4. Sentinel Values / Kill Switch: Exiting the loop gracefully via a keyword ('quit').
5. Decoupled Architecture: Separating calculation logic (Model) from console display (View).
6. Volatility & Serialization: Persisting totals to a file to prevent data loss.
"""

import json
import os

DATA_FILE = "expenses.json"

# =====================================================================
# MODEL: STATE & CALCULATIONS (No terminal input or print statements)
# =====================================================================

def load_expenses(filepath=DATA_FILE):
    """
    Loads persistent expense data.
    Returns a dictionary: {"total": float, "history": list}
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                # Ensure the dict structure is correct
                if "total" in data and "history" in data:
                    return data
        except json.JSONDecodeError:
            pass
    return {"total": 0.0, "history": []}

def save_expenses(total, history, filepath=DATA_FILE):
    """
    Saves expense data to prevent volatility loss.
    """
    with open(filepath, "w") as file:
        json.dump({"total": total, "history": history}, file, indent=4)

def process_expense(current_total, input_str, history):
    """
    Processes a user-entered string.
    - If the input is 'quit', returns (current_total, True) meaning stop.
    - If it's a valid number, performs float accumulation and appends it to history.
    - If invalid, raises a ValueError.
    """
    cleaned_input = input_str.strip().lower()

    # Check for Sentinel Value (Kill Switch)
    if cleaned_input == "quit":
        return current_total, True

    # Defensive Coding: Validate if input can be converted to float
    try:
        amount = float(input_str)
    except ValueError:
        raise ValueError(f"'{input_str}' is not a valid number. Please enter a numerical expense.")

    if amount < 0:
        raise ValueError("Expense cannot be negative. Please enter a positive amount.")

    # Accumulator Pattern: State(new) = State(old) + Input
    new_total = current_total + amount
    
    # Store history record
    history.append(amount)
    
    return new_total, False

# =====================================================================
# VIEW & CONTROLLER: USER INTERFACE (Handles inputs and displays)
# =====================================================================

def show_welcome(total):
    print("\n" + "=" * 40)
    print("      DECODELABS EXPENSE TRACKER       ")
    print("=" * 40)
    print(f"Current Total Accumulated: ${total:.2f}")
    print("Instructions: Enter your expense amounts one by one.")
    print("Type 'quit' at any time to exit and view the final total.")
    print("=" * 40)

def main():
    # Initialize state outside the loop
    data = load_expenses()
    total = data["total"]
    history = data["history"]

    show_welcome(total)

    # Continuous Loop: The Logic Skeleton
    while True:
        user_input = input("\nEnter expense amount (or 'quit'): ").strip()

        try:
            # Process using Model logic
            total, should_exit = process_expense(total, user_input, history)

            if should_exit:
                print("\n" + "=" * 40)
                print("            FINAL AUDIT REPORT          ")
                print("=" * 40)
                print(f"Total Transactions : {len(history)}")
                print(f"Total Amount Spent : ${total:.2f}")
                print("=" * 40)
                print("Goodbye!")
                break

            # Save state after each successful entry (Defending against RAM volatility)
            save_expenses(total, history)
            print(f"[SUCCESS] Added ${float(user_input):.2f}. Subtotal: ${total:.2f}")

        except ValueError as e:
            # Defensive validation warning
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
