# Week 3 Project: Enterprise Random Password Generator

A command-line interface (CLI) application in Python designed to demonstrate cryptographic security, string optimization, input validation bounds, and information theory (Shannon Entropy).

---

## Core Learning Concepts Implemented

### 1. Cryptographic Security (`secrets` vs `random`)
The standard Python `random` module uses the **Mersenne Twister** algorithm, which is pseudo-random and deterministic. If an attacker knows the seed (typically based on the system clock), they can predict all outputs. This project uses the **`secrets`** module (`secrets.choice()`), which taps into operating-system-level entropy sources (hardware noise) for cryptographically secure, non-predictable generation.

### 2. Time and Space Complexity in String Creation
In Python, strings are **immutable** objects. When you append a character to a string inside a loop (`password += char`), the interpreter must create a new string object in memory, copy the old content, add the new character, and discard the old object. This leads to quadratic time complexity:
$$\mathcal{O}(N^2)$$
This project optimizes memory allocation by collecting characters in a list and calling:
```python
# Runs in O(N) linear time complexity with single memory allocation
return "".join(char_list)
```

### 3. Math of Information Entropy
The security of a password is mathematically measured by **Information Entropy** (bits of unpredictability) using:
$$E = L \times \log_2(R)$$
Where:
* $L$ = Length of the password.
* $R$ = Size of the character pool (e.g., 62 for alphanumeric, 94 when special symbols are included).

Expanding the character pool size ($R$) increases entropy, but increasing the length ($L$) drives exponential security increases.

### 4. Validation Bounds & NIST SP 800-63-4 Compliance
* **NIST 2024 Standards**: Prioritizes absolute length over forced complexity (legacy policies like requiring uppercase/symbols lead to predictable human patterns). NIST recommends a minimum length of **15 characters** for high-security environments.
* **Validation Guard**: Our code checks length bounds ($8 \le \text{length} \le 64$) and displays warnings if the password falls below the NIST minimum of 15 characters.

---

## How to Run the Program

1. Open your terminal.
2. Navigate to the project directory:
   ```bash
   cd week3
   ```
3. Run the application:
   ```bash
   python generator.py
   ```
4. Run the unit tests:
   ```bash
   python test_generator.py
   ```
