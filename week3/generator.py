"""
DecodeLabs Random Password Generator - Week 3 Project

This application demonstrates Python Security and Optimization fundamentals:
1. Cryptographically Secure Randomness: secrets.choice() instead of random.choice().
2. Standard Library Integration: Leveraging the 'string' module.
3. String Allocation Optimization: O(N) "".join(list) pattern instead of password += char.
4. Input Validation & Security Standards: Adhering to NIST SP 800-63-4 (minimum 15 characters).
5. Information Entropy: E = L * log2(R) calculation.
6. Decoupled Architecture: Model (generation and math) separated from View (CLI interface).
"""

import math
import secrets
import string

# =====================================================================
# MODEL: SECURITY & CRYPTOGRAPHY (No printing or input functions)
# =====================================================================

def calculate_entropy(length, pool_size):
    """
    Calculates password entropy in bits using the Shannon Entropy formula:
    E = L * log2(R)
    """
    if length <= 0 or pool_size <= 0:
        return 0.0
    return length * math.log2(pool_size)

def secure_shuffle(lst):
    """
    Shuffles a list in-place using cryptographically secure randomness
    via the Fisher-Yates algorithm and secrets.randbelow.
    """
    n = len(lst)
    for i in range(n - 1, 0, -1):
        # Pick a random index from 0 to i securely
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]

def generate_secure_password(length, use_letters=True, use_digits=True, use_symbols=True):
    """
    Generates a secure password.
    - Guarantees at least one character from each active character pool.
    - Uses secrets.choice for cryptographic security.
    - Uses "".join() for O(N) memory allocation performance.
    """
    required_pools = []
    if use_letters:
        required_pools.append(string.ascii_letters)
    if use_digits:
        required_pools.append(string.digits)
    if use_symbols:
        required_pools.append(string.punctuation)

    if not required_pools:
        raise ValueError("At least one character pool (Letters, Digits, or Symbols) must be selected.")

    if length < len(required_pools):
        raise ValueError(f"For selected pools, password length must be at least {len(required_pools)}.")

    char_list = []

    # 1. Guarantee at least one character from each active pool
    for pool in required_pools:
        char_list.append(secrets.choice(pool))

    # 2. Fill the remaining length from the combined character pool
    combined_pool = "".join(required_pools)
    remaining_length = length - len(char_list)
    for _ in range(remaining_length):
        char_list.append(secrets.choice(combined_pool))

    # 3. Shuffle securely to hide the positions of guaranteed characters
    secure_shuffle(char_list)

    # 4. Join array in O(N) linear time
    return "".join(char_list)

# =====================================================================
# VIEW & CONTROLLER: USER INTERFACE (Handles inputs and displays)
# =====================================================================

def evaluate_strength(entropy):
    """
    Returns a text rating of the password strength based on entropy in bits.
    """
    if entropy < 40:
        return "Very Weak (Easily cracked)"
    elif 40 <= entropy < 60:
        return "Weak (Prone to offline dictionary attacks)"
    elif 60 <= entropy < 80:
        return "Moderate (Decent for non-critical accounts)"
    elif 80 <= entropy < 100:
        return "Strong (NIST standard compliant)"
    else:
        return "Excellent (Cryptographically secure / Passphrase strength)"

def get_boolean_input(prompt):
    """
    Helper function to safely capture yes/no inputs.
    """
    while True:
        val = input(prompt).strip().lower()
        if val in ('y', 'yes', ''):
            return True
        if val in ('n', 'no'):
            return False
        print("[!] Invalid input. Please enter 'y' or 'n'.")

def show_welcome():
    print("\n" + "=" * 55)
    print("      DECODELABS ENTERPRISE PASSWORD GENERATOR       ")
    print("=" * 55)
    print("Security Compliance: NIST SP 800-63-4 Guidelines")
    print("- Recommends absolute length (minimum 15 characters).")
    print("- Uses cryptographically secure 'secrets' engine.")
    print("- Calculates password strength via Shannon Entropy.")
    print("=" * 55)

def main():
    show_welcome()

    while True:
        # 1. Input Validation: Capture length
        try:
            length_input = input("\nEnter password length (8-64, default 16, or 'q' to quit): ").strip()
            if length_input.lower() == 'q':
                print("\nGoodbye!")
                break

            if length_input == "":
                length = 16
            else:
                length = int(length_input)

            if not (8 <= length <= 64):
                print("[!] Error: Length must be between 8 and 64 characters.")
                continue

            if length < 15:
                print("[WARNING] NIST SP 800-63-4 recommends at least 15 characters for high security.")

        except ValueError:
            print("[!] Error: Please enter a valid number.")
            continue

        # 2. Capture Pools Selection
        use_letters = get_boolean_input("Include Letters? (Y/n): ")
        use_digits = get_boolean_input("Include Digits? (Y/n): ")
        use_symbols = get_boolean_input("Include Special Symbols? (Y/n): ")

        # 3. Generate password using decoupled Model logic
        try:
            password = generate_secure_password(length, use_letters, use_digits, use_symbols)
            
            # Determine character pool size for entropy calculation
            pool_size = 0
            if use_letters: pool_size += len(string.ascii_letters)
            if use_digits: pool_size += len(string.digits)
            if use_symbols: pool_size += len(string.punctuation)

            entropy = calculate_entropy(length, pool_size)
            strength = evaluate_strength(entropy)

            # Display Output
            print("\n" + "-" * 55)
            print("                 GENERATED CREDENTIALS                  ")
            print("-" * 55)
            print(f"Password     : {password}")
            print(f"Length       : {length} characters")
            print(f"Pool Size    : {pool_size} characters")
            print(f"Entropy      : {entropy:.2f} bits")
            print(f"Strength     : {strength}")
            print("-" * 55)

        except ValueError as e:
            print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()
