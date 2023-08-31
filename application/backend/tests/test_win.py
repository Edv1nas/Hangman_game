import unittest
from utils.hangman_game import Hangman

class TestCheckWin(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    def test_check_win_true(self):
        self.hang.guessed_letters = set(["e", "x", "a", "m", "p", "l"])
        self.hang.letters = ["e", "x", "a", "m", "p", "l", "e"]
        result = self.hang.check_win()
        self.assertTrue(result)

    def test_check_win_False(self):
        self.hang.guessed_letters = set()
        self.hang.letters = ["e", "x", "a", "m", "p", "l", "e"]
        result = self.hang.check_win()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()