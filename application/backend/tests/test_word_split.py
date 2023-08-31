import unittest
from utils.hangman_game import Hangman


class TestSplitWord(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    def test_split_word(self):
        self.hang.game_word = "example"
        result = self.hang.split_word()
        expected_letters = list(self.hang.game_word)
        self.assertEqual(result, expected_letters)

if __name__ == '__main__':
    unittest.main()