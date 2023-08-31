import unittest
from utils.hangman_game import Hangman

class TestCheckLoss(unittest.TestCase):

    def setUp(self):
        self.hang = Hangman()

    def test_check_loss(self):
        self.hang.attempts = 5
        self.hang.max_attempts = 5
        result = self.hang.check_loss()
        self.assertTrue(result)

    def test_check_loss_not_reached(self):
        self.hang.attempts = 3
        self.hang.max_attempts = 5
        result = self.hang.check_loss()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()