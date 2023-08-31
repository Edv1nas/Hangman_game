import logging.config
from sqlalchemy.orm import Session
from random_word import RandomWords
from datetime import datetime
from models.game import Game
from models.letters import Letters
from crud.account_crud import update_account_stats
from crud.game_crud import get_game, update_game_status, get_account_id_from_game_id
from crud. letter_crud import get_guessed_letters
import string
from schemas.letter_schemas import LetterResponse

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


class Hangman:
    def __init__(self):
        self.game_word = ""
        self.random_words = RandomWords()
        self.letters = []
        self.guessed_letters = set()
        self.attempts = 0
        self.max_attempts = 10

    def get_random_word(self) -> str:
        try:
            random_word = RandomWords()
            self.game_word = random_word.get_random_word()
            return self.game_word
        except Exception as e:
            logger.error("Error occurred while getting a random word.", e)

    def count_made_attempts(self, guessed_correctly: bool) -> int:
        try:
            if not guessed_correctly:
                self.attempts += 1
            return self.attempts
        except Exception as e:
            logger.error("Error occurred while counting made attempts.", e)
            return self.attempts

    def count_left_attempts(self) -> int:
        try:
            remain_attempts = self.max_attempts - self.attempts
            return max(remain_attempts, 0)
        except Exception as e:
            logger.error("Error occurred while counting left attempts.", e)
            return 0

    def split_word(self) -> str:
        try:
            self.letters = list(self.game_word)
            return self.letters
        except Exception as e:
            logger.error("Error occurred while splitting the word.", e)
            return []

    def guess_letter(self, guessed_letter) -> str:
        try:
            self.guessed_letters.add(guessed_letter)
            return guessed_letter in self.letters
        except Exception as e:
            logger.error("Error occurred while guessing a letter.", e)
            return False

    def mask_game_word(self) -> str:
        try:
            masked_word = ""
            for char in self.game_word:
                if char in self.guessed_letters:
                    masked_word += char + " "
                else:
                    masked_word += "_ "
            return masked_word.strip()
        except Exception as e:
            logger.error("Error occurred while masking the game word.", e)
            return ""

    def check_win(self) -> bool:
        try:
            return all(letter in self.guessed_letters for letter in self.letters)
        except Exception as e:
            logger.error("Error occurred while checking if the player won.", e)
            return False

    def check_loss(self) -> bool:
        try:
            return self.attempts >= self.max_attempts
        except Exception as e:
            logger.error("Error occurred while checking if the player lost.", e)
            return False

    def create_game(self, db: Session, account_id: int):
        try:
            self.get_random_word()
            self.split_word()

            game_data = Game(
                account_id=account_id,
                game_date=datetime.now(),
                game_status="in_progress",
                attempts=self.attempts,
                game_word=self.game_word,
            )
            db.add(game_data)
            db.commit()
            db.refresh(game_data)
            return game_data
        except Exception as e:
            logger.error("Error occurred while creating a game.", e)
            return None

    def play_game(self, db: Session, game_id: int, letter: LetterResponse):
        try:
            game_data = get_game(db, game_id)

            account_id = get_account_id_from_game_id(db, game_id)

            self.game_word = game_data.game_word
            self.attempts = game_data.attempts

            self.guessed_letters = get_guessed_letters(db, game_id)


            if len(letter) != 1 or letter not in string.ascii_lowercase:
                raise ValueError("Invalid letter")

            if letter in self.guessed_letters:
                masked_word = self.mask_game_word()
                game_status = game_data.game_status
                entered_letters = list(self.guessed_letters)
                attempts = self.attempts
                return {
                    "masked_word": masked_word,
                    "game_status": game_status,
                    "entered_letters": entered_letters,
                    "attempts": attempts,
                    "message": f"The letter '{letter}' was already used."
                }

            guessed_correctly = self.guess_letter(letter)

            if letter not in self.mask_game_word():
                self.attempts += 1

            entered_letter = Letters(
                game_id=game_id, letter=letter
            )
            db.add(entered_letter)
            db.commit()

            game_message = ""

            masked_word = self.mask_game_word()
            game_word = self.game_word

            game_status = "in_progress"
            if len(game_word) == len([char for char in masked_word if char.isalpha()]):
                game_status = "Victory"
                game_message = "Congratulations! You guessed the word."
                update_account_stats(db, game_data.account_id, game_status)

            else:
                if self.check_loss():
                    game_status = "Defeat"
                    game_message = f"Oops! You've used all attempts. The word was: {self.game_word.upper()} "
                    update_account_stats(db, game_data.account_id, game_status)

            update_game_status(db, game_id, game_status, attempts=self.attempts)

            return {
                "masked_word": masked_word,
                "game_status": game_status,
                "entered_letters": list(self.guessed_letters),
                "attempts": self.attempts,
                "message": game_message,
            }
        except Exception as e:
            logger.error(f"Error occurred while playing the game.", e)
            return {
                "error": "Internal server error",
                "message": "Error occurred while playing the game."
            }