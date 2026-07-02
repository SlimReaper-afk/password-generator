import string
import unittest

from password_generator import entropy_bits, generate_password, pool_size


class TestGeneratePassword(unittest.TestCase):
    def test_password_has_requested_length(self):
        self.assertEqual(len(generate_password(20)), 20)

    def test_rejects_length_below_minimum(self):
        with self.assertRaises(ValueError):
            generate_password(8)

    def test_password_contains_all_character_types(self):
        password = generate_password(12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_excludes_symbols_when_disabled(self):
        password = generate_password(30, use_symbols=False)
        self.assertFalse(any(c in string.punctuation for c in password))

    def test_only_digits_when_others_disabled(self):
        password = generate_password(16, use_lower=False, use_upper=False, use_symbols=False)
        self.assertTrue(password.isdigit())
        self.assertEqual(len(password), 16)

    def test_rejects_when_no_type_selected(self):
        with self.assertRaises(ValueError):
            generate_password(16, use_lower=False, use_upper=False,
                              use_digits=False, use_symbols=False)


class TestHelpers(unittest.TestCase):
    def test_pool_size_all_types(self):
        expected = (len(string.ascii_lowercase) + len(string.ascii_uppercase)
                    + len(string.digits) + len(string.punctuation))
        self.assertEqual(pool_size(), expected)

    def test_entropy_increases_with_length(self):
        self.assertGreater(entropy_bits(20, 94), entropy_bits(12, 94))


if __name__ == "__main__":
    unittest.main()
