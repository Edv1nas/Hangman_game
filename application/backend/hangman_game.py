from sqlalchemy.orm import Session
from random_word import RandomWords
from datetime import datetime
from models.game import Game
from models.letters import Letter
from crud.game_crud import get_game


class Base:
    def __init__(self):
        self.game_word = ""
        self.random_words = RandomWords()
        self.letters = None
        self.guessed_letters = set()
        self.attempts = 0
        self.max_attempts = 10

    def get_random_word(self) -> str:
        random_word = RandomWords()
        self.game_word = random_word.get_random_word()
        return self.game_word

    def count_made_attempts(self):
        self.attempts += 1
        return self.attempts

    def count_left_attempts(self):
        remain_attempts = self.max_attempts - self.attempts
        return max(remain_attempts, 0)

    def split_word(self):
        self.letters = list(self.game_word)
        return self.letters

    def guess_letter(self, guessed_letter):
        self.guessed_letters.add(guessed_letter)
        return guessed_letter in self.letters

    def mask_game_word(self):
        masked_word = ""
        for char in self.game_word:
            if char in self.guessed_letters:
                masked_word += char
            else:
                masked_word += "_"
        return masked_word

    def check_win(self):
        return all(letter in self.guessed_letters for letter in self.letters)

    def check_loss(self):
        return self.attempts >= self.max_attempts

    def create_game(self, db: Session, account_id: int):
        self.get_random_word()
        self.split_word()

        game_data = Game(
            account_id=account_id,
            game_date=datetime.now(),
            game_status="in_progress",
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            game_word=self.game_word,

        )
        db.add(game_data)
        db.commit()
        db.refresh(game_data)
        return game_data


class Hangman(Base):
    def play_game(self, db: Session, game_id: int, letter: str):
        game_data = get_game(db, game_id)

        game_word = self.game_word,
        attempts = self.attempts,
        max_attempts = self.max_attempts,
        game_status = game_status

        engine = create_engine("sqlite:///hangman_game.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        self.get_random_word()
        self.split_word()

        while not self.check_win() and not self.check_loss():
            guessed_letter = self.generate_guessed_letter()

            self.attempts += 1
            is_correct_guess = self.guess_letter(guessed_letter)

            entered_letter = Letter(
                game_id=self.current_game.game_id, letter=guessed_letter)
            session.add(entered_letter)
            session.commit()

            if self.check_win():
                game_status = 'Victory'
            elif self.check_loss():
                game_status = 'Defeat'
            else:
                game_status = 'in_progress'

            game_data = Game(
                game_word=self.game_word,
                attempts=self.attempts,
                max_attempts=self.max_attempts,
                game_status=game_status
            )
            session.add(game_data)
            session.commit()

            masked_word = self.mask_game_word()

        session.close()
