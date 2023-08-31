import unittest
from unittest.mock import patch
from utils.hangman_game import Hangman

class TestCountMadeAttempts(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    @patch("builtins.input", return_value="1")
    def test_count_made_attempts_bad_guess(self, mock_input):
        expected_attempts = int(mock_input.return_value)
        result = self.hang.count_made_attempts(False)
        self.assertEqual(result, expected_attempts)

    @patch("builtins.input", return_value="0")
    def test_count_made_attempts_good_guess(self, mock_input):
        expected_attempts = int(mock_input.return_value)
        result = self.hang.count_made_attempts(True)
        self.assertEqual(result, expected_attempts)

if __name__ == "__main__":
    unittest.main()