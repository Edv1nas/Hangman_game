import unittest
from utils.hangman_game import Hangman

class TestMaskGameWord(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    def test_mask_game_word(self):
        self.hang.game_word = "example"
        self.hang.guessed_letters = set(["e", "x", "a", "m"])
        result = self.hang.mask_game_word()
        expected_masked_word = "e x a m _ _ e"
        self.assertEqual(result, expected_masked_word)

if __name__ == "__main__":
    unittest.main()