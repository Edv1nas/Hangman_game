import unittest
from utils.hangman_game import Hangman

class TestGuessLetter(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    def test_good_guess(self):
        self.hang.letters = ["e", "x", "a", "m", "p", "l", "e"]
        guessed_letter = "p"
        result = self.hang.guess_letter(guessed_letter)
        self.assertTrue(result)

    def test_bad_guess(self):
        self.hang.letters = ["e", "x", "a", "m", "p", "l", "e"]
        guessed_letter = "h"
        result = self.hang.guess_letter(guessed_letter)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()