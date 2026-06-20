import unittest
import math
import string
import generator

class TestPasswordGenerator(unittest.TestCase):
    def test_calculate_entropy(self):
        """Verify the mathematical entropy calculation is correct."""
        # For a 16-character alphanumeric password (letters + numbers = 62 pool size)
        # E = 16 * log2(62) approx 95.26
        calculated = generator.calculate_entropy(16, 62)
        expected = 16 * math.log2(62)
        self.assertAlmostEqual(calculated, expected, places=5)

        # Edge cases
        self.assertEqual(generator.calculate_entropy(0, 62), 0.0)
        self.assertEqual(generator.calculate_entropy(16, 0), 0.0)

    def test_generate_password_length(self):
        """Verify that the generated password matches the exact requested length."""
        for length in [8, 12, 16, 32, 64]:
            password = generator.generate_secure_password(length)
            self.assertEqual(len(password), length)

    def test_guaranteed_categories(self):
        """Verify that the password contains at least one character from each active pool."""
        # Test letters and digits only
        password = generator.generate_secure_password(8, use_letters=True, use_digits=True, use_symbols=False)
        has_letter = any(c in string.ascii_letters for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        self.assertTrue(has_letter)
        self.assertTrue(has_digit)
        self.assertFalse(has_symbol)

        # Test all active pools
        password = generator.generate_secure_password(15, use_letters=True, use_digits=True, use_symbols=True)
        has_letter = any(c in string.ascii_letters for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        self.assertTrue(has_letter)
        self.assertTrue(has_digit)
        self.assertTrue(has_symbol)

    def test_empty_pool_raises_value_error(self):
        """Verify that disabling all character pools raises a ValueError."""
        with self.assertRaises(ValueError):
            generator.generate_secure_password(16, use_letters=False, use_digits=False, use_symbols=False)

    def test_insufficient_length_raises_value_error(self):
        """Verify that requesting a length smaller than the number of active pools raises a ValueError."""
        # 3 active pools require at least 3 characters length to guarantee inclusion of all
        with self.assertRaises(ValueError):
            generator.generate_secure_password(2, use_letters=True, use_digits=True, use_symbols=True)

if __name__ == '__main__':
    unittest.main()
